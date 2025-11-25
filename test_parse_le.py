from data_processor import process_student_results

le_sample = {
  "semester": "III",
  "exam_held": "July/2025",
  "redg_no": 24105110901,
  "name": "SMRITI KUMARI",
  "father_name": "SANTOSH KUMAR",
  "mother_name": "SANJU DEVI",
  "college_code": 110,
  "college_name": "GAYA COLLEGE OF ENGINEERING, GAYA",
  "course_code": 105,
  "course": "COMPUTER SCIENCE & ENGINEERING",
  "examYear": 2024,
  "theorySubjects": [
    {"code": "100302", "name": "ANALOG ELECTRONIC CIRCUITS", "ese": "30", "ia": "27", "total": "57", "grade": "D", "credit": "3.00"},
    {"code": "100304", "name": "DATA STRUCTURE & ALGORITHMS", "ese": "56", "ia": "18", "total": "74", "grade": "B", "credit": "3.00"},
    {"code": "100311", "name": "MATHEMATICS-III (DIFFERENTIAL CALCULUS)", "ese": "28", "ia": "30", "total": "58", "grade": "D", "credit": "2.00"},
    {"code": "100313", "name": "OBJECT ORIENTED PROGRAMMING USING C++", "ese": "48", "ia": "26", "total": "74", "grade": "B", "credit": "3.00"},
    {"code": "100314", "name": "TECHNICAL WRITING", "ese": "55", "ia": "25", "total": "80", "grade": "A", "credit": "3.00"}
  ],
  "practicalSubjects": [
    {"code": "100302P", "name": "Analog Electronics Circuits Laboratory", "ese": "27", "ia": "17", "total": "44", "grade": "A", "credit": "2.00"},
    {"code": "100304P", "name": "DATA STRUCTURE & ALGORITHMS", "ese": "26", "ia": "17", "total": "43", "grade": "A", "credit": "2.00"},
    {"code": "100313P", "name": "OBJECT ORIENTED PROGRAMMING USING C++", "ese": "25", "ia": "17", "total": "42", "grade": "A", "credit": "2.00"},
    {"code": "100399P", "name": "Internship", "ese": "55", "ia": "23", "total": "78", "grade": "B", "credit": "4.00"}
  ],
  "sgpa": ["NULL","NULL","7.96", None, None, None, None, None],
  "cgpa": "NULL",
  "fail_any": "PASS"
}

if __name__ == '__main__':
    df = process_student_results([le_sample])
    print(df.to_dict(orient='records'))
