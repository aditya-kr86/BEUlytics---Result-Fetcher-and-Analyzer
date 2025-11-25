from data_processor import process_student_results

sample = {
  "semester": "III",
  "exam_held": "July/2025",
  "redg_no": 24101110916,
  "name": "MANOJ KUMAR",
  "father_name": "MEWA PRASAD",
  "mother_name": "PRAMILA DEVI",
  "college_code": 110,
  "college_name": "GAYA COLLEGE OF ENGINEERING, GAYA",
  "course_code": 101,
  "course": "CIVIL ENGINEERING",
  "examYear": 2024,
  "theorySubjects": [
    {
      "code": "100301",
      "name": "BIOLOGY FOR ENGINEERS",
      "ese": "41",
      "ia": "23",
      "total": "64",
      "grade": "C",
      "credit": "2.00"
    }
  ],
  "practicalSubjects": [
    {
      "code": "100399P",
      "name": "Internship",
      "ese": "64",
      "ia": "25",
      "total": "89",
      "grade": "A",
      "credit": "4.00"
    }
  ],
  "sgpa": ["NULL", "NULL", "7.67", None, None, None, None, None],
  "cgpa": "NULL",
  "fail_any": "PASS"
}

if __name__ == '__main__':
    df = process_student_results([sample])
    result = df.to_dict(orient='records')[0]
    
    print("TEST RESULT:")
    print(f"  Student: {result['Student Name']}")
    print(f"  Current SGPA: {result['Current SGPA']}")
    print(f"  CGPA (filled from SGPA): {result['CGPA']}")
    
    if result['Current SGPA'] == 7.67 and result['CGPA'] == 7.67:
        print("\nSUCCESS! CGPA is now filled with latest SGPA when NULL")
    else:
        print(f"\nFAILED: Expected both to be 7.67")
