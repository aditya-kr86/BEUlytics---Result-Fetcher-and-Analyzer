"""
BEU API Scraper Module - Fetches student results using the official BEU API
Author: Aditya Kumar
"""

import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Optional
import json

BASE_URL = "https://www.beu-bih.ac.in/backend/v1/result/get-result"

def fetch_single_result(
    registration_no: str,
    semester: str,
    batch: int,
    exam_month: str,
    exam_year: int,
    retries: int = 3,
    timeout: int = 15
) -> Optional[Dict]:
    """
    Fetches a single student's result from the BEU API.
    
    Args:
        registration_no: Full registration number (e.g., "23105110005")
        semester: Semester in Roman numerals (e.g., "III")
        batch: Batch year (e.g., 2023)
        exam_month: Month of exam (e.g., "July")
        exam_year: Year of exam (e.g., 2025)
        retries: Number of retry attempts
        timeout: Request timeout in seconds
    
    Returns:
        Dictionary with student result data or None if failed
    """
    url = f"{BASE_URL}?year={batch}&redg_no={registration_no}&semester={semester}&exam_held={exam_month}/{exam_year}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
    }
    
    for attempt in range(retries):
        try:
            # Polite delay to avoid overwhelming the server
            time.sleep(0.5)
            
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            
            data = response.json()
            
            # Check if response is successful
            if data.get("status") == 200 and data.get("data"):
                return data["data"]
            else:
                return None
                
        except requests.exceptions.RequestException as e:
            if attempt < retries - 1:
                time.sleep(1 * (2 ** attempt))  # Exponential backoff
            else:
                print(f"Failed to fetch registration {registration_no} after {retries} attempts: {e}")
                return None
        except json.JSONDecodeError:
            print(f"Invalid JSON response for {registration_no}")
            return None


def fetch_all_results(
    start_reg: str,
    end_reg: str,
    semester: str,
    batch: int,
    branch: str,
    college: str,
    exam_month: str,
    exam_year: int,
    include_lateral: bool = False,
    max_workers: int = 4
) -> List[Dict]:
    """
    Fetches results for a range of registration numbers using multi-threading.
    Format: BB(2) + RRR(3) + CCC(3) + SSS(3) = 11 digits total
    Example: 23105110003 = 23(batch) + 105(CSE) + 110(Gaya) + 003(student)
    For LE: batch year is +1 (e.g., normal=23, LE=24)
    
    Args:
        start_reg: Starting student number (e.g., "1")
        end_reg: Ending student number (e.g., "100")
        semester: Semester in Roman numerals
        batch: Batch year (2 digits, e.g., 23 for 2023)
        branch: Branch code (3 digits, e.g., "105" for CSE)
        college: College code (3 digits, e.g., "110" for Gaya)
        exam_month: Month of exam
        exam_year: Year of exam
        include_lateral: Whether to include lateral entry students
        max_workers: Number of parallel threads
    
    Returns:
        List of student result dictionaries
    """
    results = []
    registration_numbers = []
    
    # Generate regular student registration numbers: BB + RRR + CCC + SSS(3 digits)
    for reg in range(int(start_reg), int(end_reg) + 1):
        full_reg = f"{batch}{branch}{college}{reg:03d}"  # Exactly 11 digits total
        registration_numbers.append(full_reg)
    
    # Add lateral entry students if requested (batch year +1, student numbers 901-930)
    if include_lateral:
        le_batch = batch + 1
        for reg in range(901, 931):  # LE students 901-930
            full_reg = f"{le_batch}{branch}{college}{reg:03d}"
            registration_numbers.append(full_reg)
    
    # Fetch results using thread pool
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(
                fetch_single_result,
                reg_no,
                semester,
                batch,
                exam_month,
                exam_year
            ): reg_no for reg_no in registration_numbers
        }
        
        for future in as_completed(futures):
            result = future.result()
            if result:
                results.append(result)
    
    return results


def fetch_semester_results(
    reg_start: int,
    reg_end: int,
    branch: str,
    college: str,
    semester: int,
    batch: int,
    include_lateral: bool = False,
    exam_month: str = "July",
    exam_year: int = 2025,
    max_workers: int = 4
) -> List[Dict]:
    """
    Fetches results for a range of students in a specific semester.
    Registration format: BB(2) + RRR(3) + CCC(3) + SSS(3) = 11 digits
    Example: 23105110003 = 23(batch) + 105(CSE) + 110(Gaya) + 003(student)
    For LE: batch year is +1 (e.g., normal=23, LE=24)
    
    Args:
        reg_start: Start student number (e.g., 1)
        reg_end: End student number (e.g., 100)
        branch: Branch code (3 digits, e.g., "105" for CSE)
        college: College code (3 digits, e.g., "110" for Gaya)
        semester: Semester number (1-8)
        batch: Batch year (2 digits, e.g., 23 for 2023)
        include_lateral: Whether to include lateral entry students
        exam_month: Month of exam
        exam_year: Year of exam
        max_workers: Number of parallel threads
    
    Returns:
        List of semester results
    """
    sem_romans = {
        1: "I", 2: "II", 3: "III", 4: "IV",
        5: "V", 6: "VI", 7: "VII", 8: "VIII"
    }
    
    results = []
    
    # Fetch results using thread pool
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {}
        
        # Regular students use batch year
        for reg in range(int(reg_start), int(reg_end) + 1):
            full_reg = f"{batch}{branch}{college}{reg:03d}"
            futures[executor.submit(
                fetch_single_result,
                full_reg,
                sem_romans[semester],
                batch,
                exam_month,
                exam_year
            )] = full_reg
        
        # LE students use batch+1 year and start from 901
        if include_lateral:
            le_batch = batch + 1
            for reg in range(901, 931):  # LE students 901-930
                full_reg = f"{le_batch}{branch}{college}{reg:03d}"
                futures[executor.submit(
                    fetch_single_result,
                    full_reg,
                    sem_romans[semester],
                    le_batch,  # Use LE batch year for API call
                    exam_month,
                    exam_year
                )] = full_reg
        
        for future in as_completed(futures):
            result = future.result()
            if result:
                results.append(result)
    
    return results
