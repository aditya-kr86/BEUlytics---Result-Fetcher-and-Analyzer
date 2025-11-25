"""
Data Processing Module - Transforms API responses into structured DataFrames
Author: Aditya Kumar
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional


def process_student_results(results: List[Dict]) -> pd.DataFrame:
    """
    Converts API result data into a structured DataFrame.
    
    Args:
        results: List of student result dictionaries from API
    
    Returns:
        DataFrame with flattened student data
    """
    processed_data = []

    def safe_int(value, default=None):
        try:
            if value is None:
                return default
            s = str(value).strip()
            if s.upper() in {"NULL", "NE", "N/A", "-", ""}:
                return default
            return int(float(s))
        except Exception:
            return default

    def safe_float(value, default=None):
        try:
            if value is None:
                return default
            s = str(value).strip()
            if s.upper() in {"NULL", "NE", "N/A", "-", ""}:
                return default
            return float(s)
        except Exception:
            return default

    def latest_numeric_sgpa(sgpa_list: Optional[List]) -> float:
        """Return the latest numeric SGPA from the list or NaN if none."""
        if not sgpa_list:
            return float("nan")
        # iterate reversed and find first value that can be converted to float
        for v in reversed(sgpa_list):
            if v is None:
                continue
            s = str(v).strip()
            if s.upper() in {"NULL", "NE", "N/A", "-", ""}:
                continue
            try:
                return float(s)
            except Exception:
                continue
        return float("nan")

    for student_data in results:
        try:
            # Calculate GPA from theory and practical subjects
            theory_subjects = student_data.get("theorySubjects", []) or []
            practical_subjects = student_data.get("practicalSubjects", []) or []
            all_subjects = theory_subjects + practical_subjects

            sgpa_list = student_data.get("sgpa") or []
            current_sgpa = latest_numeric_sgpa(sgpa_list)

            # If CGPA is NULL/None, use the latest SGPA value
            cgpa_val = safe_float(student_data.get("cgpa"), default=float("nan"))
            if pd.isna(cgpa_val):
                cgpa_val = current_sgpa

            row = {
                "Registration No.": str(student_data.get("redg_no", "")),
                "Student Name": student_data.get("name", ""),
                "Father's Name": student_data.get("father_name", ""),
                "Mother's Name": student_data.get("mother_name", ""),
                "College Code": str(student_data.get("college_code", "")),
                "College Name": student_data.get("college_name", ""),
                "Course Code": str(student_data.get("course_code", "")),
                "Course": student_data.get("course", ""),
                "Semester": student_data.get("semester", ""),
                "Exam Held": student_data.get("exam_held", ""),
                "Current SGPA": current_sgpa,
                "CGPA": cgpa_val,
                "Status": student_data.get("fail_any", "PASS"),
                "Total Subjects": len(all_subjects),
                "Theory Subjects": len(theory_subjects),
                "Practical Subjects": len(practical_subjects),
            }

            # Add subject details as separate columns (safe parsing)
            for idx, subject in enumerate(theory_subjects):
                row[f"Theory_{idx+1}_Name"] = subject.get("name", "")
                row[f"Theory_{idx+1}_Grade"] = subject.get("grade", "")
                row[f"Theory_{idx+1}_Total"] = safe_int(subject.get("total"), default=None)
                row[f"Theory_{idx+1}_Credit"] = safe_float(subject.get("credit"), default=None)

            for idx, subject in enumerate(practical_subjects):
                row[f"Practical_{idx+1}_Name"] = subject.get("name", "")
                row[f"Practical_{idx+1}_Grade"] = subject.get("grade", "")
                row[f"Practical_{idx+1}_Total"] = safe_int(subject.get("total"), default=None)
                row[f"Practical_{idx+1}_Credit"] = safe_float(subject.get("credit"), default=None)

            processed_data.append(row)

        except Exception as e:
            print(f"Error processing student {student_data.get('name', 'Unknown')}: {e}")
            continue

    df = pd.DataFrame(processed_data)
    # Ensure numeric columns are proper dtype
    if "Current SGPA" in df.columns:
        df["Current SGPA"] = pd.to_numeric(df["Current SGPA"], errors="coerce")
    if "CGPA" in df.columns:
        df["CGPA"] = pd.to_numeric(df["CGPA"], errors="coerce")

    return df


def get_sorting_options() -> Dict[str, str]:
    """Returns available sorting options."""
    return {
        "sgpa_desc": "SGPA (High to Low)",
        "sgpa_asc": "SGPA (Low to High)",
        "cgpa_desc": "CGPA (High to Low)",
        "cgpa_asc": "CGPA (Low to High)",
        "name": "Student Name (A-Z)",
        "regno": "Registration No.",
        "college": "College Name",
        "course": "Course",
    }


def sort_dataframe(df: pd.DataFrame, sort_by: str) -> pd.DataFrame:
    """
    Sorts DataFrame based on the selected option.
    
    Args:
        df: DataFrame to sort
        sort_by: Sorting option key
    
    Returns:
        Sorted DataFrame
    """
    if sort_by == "sgpa_desc":
        return df.sort_values(by="Current SGPA", ascending=False, na_position='last')
    elif sort_by == "sgpa_asc":
        return df.sort_values(by="Current SGPA", ascending=True, na_position='last')
    elif sort_by == "cgpa_desc":
        return df.sort_values(by="CGPA", ascending=False, na_position='last')
    elif sort_by == "cgpa_asc":
        return df.sort_values(by="CGPA", ascending=True, na_position='last')
    elif sort_by == "name":
        return df.sort_values(by="Student Name", na_position='last')
    elif sort_by == "regno":
        return df.sort_values(by="Registration No.", na_position='last')
    elif sort_by == "college":
        return df.sort_values(by="College Name", na_position='last')
    elif sort_by == "course":
        return df.sort_values(by="Course", na_position='last')
    else:
        return df


def filter_dataframe(
    df: pd.DataFrame,
    college: Optional[str] = None,
    course: Optional[str] = None,
    status: Optional[str] = None,
    sgpa_min: Optional[float] = None,
    sgpa_max: Optional[float] = None
) -> pd.DataFrame:
    """
    Filters DataFrame based on multiple criteria.
    
    Args:
        df: DataFrame to filter
        college: Filter by college name
        course: Filter by course
        status: Filter by result status (PASS/FAIL)
        sgpa_min: Minimum SGPA
        sgpa_max: Maximum SGPA
    
    Returns:
        Filtered DataFrame
    """
    result = df.copy()
    
    if college:
        result = result[result["College Name"] == college]
    
    if course:
        result = result[result["Course"] == course]
    
    if status:
        result = result[result["Status"] == status]
    
    if sgpa_min is not None:
        result = result[result["Current SGPA"] >= sgpa_min]
    
    if sgpa_max is not None:
        result = result[result["Current SGPA"] <= sgpa_max]
    
    return result


def get_grade_category(sgpa: float) -> str:
    """Categorizes SGPA into performance brackets."""
    if sgpa >= 9.0:
        return "Outstanding (9.0+)"
    elif sgpa >= 8.0:
        return "Excellent (8.0-8.9)"
    elif sgpa >= 7.0:
        return "Very Good (7.0-7.9)"
    elif sgpa >= 6.0:
        return "Good (6.0-6.9)"
    elif sgpa >= 5.0:
        return "Average (5.0-5.9)"
    else:
        return "Below Average (<5.0)"


def add_grade_category(df: pd.DataFrame) -> pd.DataFrame:
    """Adds grade category column based on SGPA."""
    df_copy = df.copy()
    df_copy["Grade Category"] = df_copy["Current SGPA"].apply(get_grade_category)
    return df_copy


def get_subject_performance(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extracts and aggregates subject performance across all students.
    
    Args:
        df: Student results DataFrame
    
    Returns:
        DataFrame with subject-wise performance metrics
    """
    subject_stats = []
    
    # Extract theory subjects
    theory_cols = [col for col in df.columns if col.startswith("Theory_") and col.endswith("_Grade")]
    for col in theory_cols:
        subject_name_col = col.replace("_Grade", "_Name")
        if subject_name_col in df.columns:
            subject_name = df[subject_name_col].iloc[0] if len(df) > 0 else "Unknown"
            grades = df[col].dropna()
            
            subject_stats.append({
                "Subject": subject_name,
                "Type": "Theory",
                "Students": len(grades),
                "A+ Count": (grades == "A+").sum(),
                "A Count": (grades == "A").sum(),
                "B Count": (grades == "B").sum(),
                "C Count": (grades == "C").sum(),
                "D Count": (grades == "D").sum(),
                "F Count": (grades == "F").sum(),
            })
    
    # Extract practical subjects
    practical_cols = [col for col in df.columns if col.startswith("Practical_") and col.endswith("_Grade")]
    for col in practical_cols:
        subject_name_col = col.replace("_Grade", "_Name")
        if subject_name_col in df.columns:
            subject_name = df[subject_name_col].iloc[0] if len(df) > 0 else "Unknown"
            grades = df[col].dropna()
            
            subject_stats.append({
                "Subject": subject_name,
                "Type": "Practical",
                "Students": len(grades),
                "A+ Count": (grades == "A+").sum(),
                "A Count": (grades == "A").sum(),
                "B Count": (grades == "B").sum(),
                "C Count": (grades == "C").sum(),
                "D Count": (grades == "D").sum(),
                "F Count": (grades == "F").sum(),
            })
    
    return pd.DataFrame(subject_stats)


def get_statistics_summary(df: pd.DataFrame) -> Dict:
    """
    Calculates comprehensive statistics for the results.
    
    Args:
        df: Student results DataFrame
    
    Returns:
        Dictionary with statistics
    """
    return {
        "Total Students": len(df),
        "Passed": (df["Status"] == "PASS").sum(),
        "Failed": (df["Status"] == "FAIL").sum(),
        "Pass Rate": f"{(df['Status'] == 'PASS').sum() / len(df) * 100:.2f}%" if len(df) > 0 else "0%",
        "Average SGPA": f"{df['Current SGPA'].mean():.2f}",
        "Highest SGPA": f"{df['Current SGPA'].max():.2f}",
        "Lowest SGPA": f"{df['Current SGPA'].min():.2f}",
        "Average CGPA": f"{df['CGPA'].mean():.2f}",
        "Highest CGPA": f"{df['CGPA'].max():.2f}",
        "Lowest CGPA": f"{df['CGPA'].min():.2f}",
    }


def process_api_response(results: List[Dict]) -> pd.DataFrame:
    """Compatibility wrapper: process API response into DataFrame.

    Keeps older app imports working: `from data_processor import process_api_response`.
    Internally delegates to `process_student_results`.
    """
    return process_student_results(results)
