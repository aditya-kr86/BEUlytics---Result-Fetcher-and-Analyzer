import requests
from bs4 import BeautifulSoup
import time
from concurrent.futures import ThreadPoolExecutor
import pandas as pd

def fetch_and_parse_result(session, base_url, registration_no, retries=5, backoff_factor=1):
    """Fetches and parses a single student's result using a shared session object."""
    url = f"{base_url}{registration_no}"
    
    # Add a polite delay to avoid overwhelming the server
    time.sleep(1)

    for attempt in range(retries):
        try:
            # Use the session to make the request, which includes headers
            response = session.get(url, timeout=15)
            response.raise_for_status()  # Raise an error for bad status codes (4xx or 5xx)

            soup = BeautifulSoup(response.text, "html.parser")
            
            # Check if student name exists to validate the page
            student_name_tag = soup.select_one("#ContentPlaceHolder1_DataList1_StudentNameLabel_0")
            if not student_name_tag:
                print(f"No valid data found for Registration No: {registration_no}")
                return None

            result = {
                "Registration No.": soup.select_one("#ContentPlaceHolder1_DataList1_RegistrationNoLabel_0").text.strip(),
                "Student Name": student_name_tag.text.strip(),
                "Father's Name": soup.select_one("#ContentPlaceHolder1_DataList1_FatherNameLabel_0").text.strip(),
                "Mother's Name": soup.select_one("#ContentPlaceHolder1_DataList1_MotherNameLabel_0").text.strip(),
                "Current SGPA": soup.select_one("#ContentPlaceHolder1_DataList5_GROSSTHEORYTOTALLabel_0").text.strip()
            }
            table = soup.select_one("#ContentPlaceHolder1_GridView3")
            if table:
                headers = [th.text.strip() for th in table.select("tr")[0].find_all("th")]
                values = [td.text.strip() for td in table.select("tr")[1].find_all("td")]
                for header, value in zip(headers, values):
                    result[f"Sem {header}"] = value
            return result
        
        except (requests.exceptions.RequestException, AttributeError) as e:
            print(f"Attempt {attempt + 1} failed for {registration_no} - {e}")
            if attempt < retries - 1:
                time.sleep(backoff_factor * (2 ** attempt)) # Exponential backoff
            else:
                print(f"All retries failed for Registration No: {registration_no}.")
                return None

def fetch_all_results(base_url, start_reg, end_reg):
    """Fetches all results using a thread pool and a single, shared session."""
    results = []
    
    # Headers to mimic a real browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
    }

    # Create one session object for all requests
    with requests.Session() as session:
        session.headers.update(headers) # Add headers to the session

        # Use a safe number of workers
        with ThreadPoolExecutor(max_workers=4) as executor:
            # Pass the session object to each thread
            futures = [executor.submit(fetch_and_parse_result, session, base_url, reg_no) 
                       for reg_no in range(start_reg, end_reg + 1)]
            
            for future in futures:
                result = future.result()
                if result:
                    results.append(result)
    return results

# Your sorting functions remain exactly the same
def sort_by_current_cgpa(df):
    df["Sem Cur. CGPA"] = pd.to_numeric(df["Sem Cur. CGPA"], errors="coerce")
    return df.sort_values(by="Sem Cur. CGPA", ascending=False)

def sort_by_latest_semester_grade(df):
    sem_columns = [col for col in df.columns if col.startswith("Sem ")]

    def get_latest_grade(row):
        for col in reversed(sem_columns):
            try:
                val = float(row[col])
                return val
            except (ValueError, TypeError):
                continue
        return -1

    df["Latest Semester Grade"] = df.apply(get_latest_grade, axis=1)
    sorted_df = df.sort_values(by="Latest Semester Grade", ascending=False).drop(columns=["Latest Semester Grade"])
    return sorted_df
