# BEUlytics v2.0: Result Fetcher & Analyzer 🎓📊

## Enhanced Edition with Official BEU API Integration

**BEUlytics v2.0** is a complete redesign of the original project, now powered by the official Bihar Engineering University (BEU) API. It provides a modern, feature-rich interface for fetching, analyzing, and exporting student exam results with advanced analytics capabilities.

> **What's New in v2.0:**
> - ✅ Official BEU API Integration (no web scraping needed!)
> - ✅ Enhanced Analytics Dashboard with 8+ visualizations
> - ✅ Advanced Filtering & Sorting Options
> - ✅ Subject-wise Performance Analysis
> - ✅ Multi-format Export (CSV, Excel, JSON)
> - ✅ Improved UI/UX with Streamlit
> - ✅ College-wise & Course-wise Analysis
> - ✅ SGPA vs CGPA Correlation Analysis

---

## 📌 Features

### 🎯 Core Features
- **Official API Integration**: Uses the official BEU REST API endpoint for reliable data fetching
- **Multi-threaded Fetching**: 4 parallel workers for fast result retrieval
- **Automatic Lateral Entry Support**: Includes LE students when requested
- **Real-time Progress Tracking**: Visual progress bar during data fetch

### 📊 Analytics Dashboard
1. **Key Metrics Cards**: Display overall statistics at a glance
2. **SGPA Distribution**: Histogram showing student distribution by SGPA
3. **Performance Categories**: Pie chart with grade categories
4. **Top 10 Performers**: Bar chart and detailed student list
5. **College-wise Analysis**: Average SGPA and student count by college
6. **Course-wise Analysis**: Performance metrics by course
7. **Subject-wise Analysis**: Grade distribution for theory and practical subjects
8. **Pass/Fail Analysis**: Pass rates by college and overall statistics
9. **SGPA vs CGPA Correlation**: Scatter plot showing relationship

### 🔍 Advanced Filtering
- Filter by College, Course, and Status (Pass/Fail)
- SGPA Range Slider for fine-grained filtering
- Real-time filtered result count

### 📈 Sorting Options
- By SGPA (Ascending/Descending)
- By CGPA (Ascending/Descending)
- By Student Name (Alphabetically)
- By Registration Number
- By College Name
- By Course

### 💾 Export Formats
- **CSV**: Lightweight, Excel-compatible
- **Excel (XLSX)**: Formatted with openpyxl
- **JSON**: For programmatic access
- All exports include timestamp in filename

---

## 🚀 Quick Start

### 1. Installation

Clone the repository:
```bash
git clone https://github.com/aditya-kr86/BEUlytics---Result-Fetcher-and-Analyzer.git
cd BEUlytics---Result-Fetcher-and-Analyzer
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Run the App

```bash
streamlit run app_v2.py
```

The app will open in your browser at `http://localhost:8501`

### 3. Using the App

1. **Configure in Sidebar**:
   - Select Semester (I-VIII)
   - Choose Exam Month and Year
   - Enter Batch Year (last 2 digits, e.g., 23 for 2023-27)
   - Select Branch and College
   - Enter Registration Number Range
   - Optionally include Lateral Entry students

2. **Fetch Results**:
   - Click "🚀 Fetch Results"
   - Wait for progress bar to complete
   - Results will be displayed with analytics

3. **Analyze Data**:
   - View comprehensive analytics in the Analytics tab
   - Browse raw data in the Data View tab
   - Apply filters and sorting in Filter & Sort tab

4. **Export Results**:
   - Download in CSV, Excel, or JSON format
   - View summary statistics

---

## 📁 Project Structure

```
.
├── app_v2.py                # Main Streamlit application
├── api_scraper.py           # Official BEU API integration
├── data_processor.py        # Data processing & filtering utilities
├── enhanced_analytics.py    # Analytics visualizations module
├── requirements.txt         # Python dependencies
├── beu_logo.jpeg           # Logo for UI
├── README.md               # Original documentation
└── README_V2.md            # This file
```

---

## 🔧 Module Documentation

### `api_scraper.py`
Handles API communication with BEU's official endpoint.

**Key Functions**:
- `fetch_single_result()`: Fetches one student's result
- `fetch_all_results()`: Fetches results for a registration range (multi-threaded)
- `fetch_semester_results()`: Fetches all semesters for a single student

**API Format**:
```
https://www.beu-bih.ac.in/backend/v1/result/get-result?year={batch}&redg_no={registration_no}&semester={semester}&exam_held={exam_month}/{exam_year}
```

### `data_processor.py`
Transforms raw API responses into structured DataFrames.

**Key Functions**:
- `process_student_results()`: Converts JSON to DataFrame with flattened structure
- `sort_dataframe()`: Applies various sorting options
- `filter_dataframe()`: Advanced filtering by multiple criteria
- `add_grade_category()`: Categorizes performance levels
- `get_statistics_summary()`: Calculates key statistics

### `enhanced_analytics.py`
Provides rich visualization functions using Plotly.

**Key Functions**:
- `show_key_metrics()`: Displays metric cards
- `show_sgpa_distribution()`: SGPA histogram
- `show_grade_distribution()`: Performance category pie chart
- `show_top_performers()`: Top 10 students visualization
- `show_college_wise_analysis()`: College performance metrics
- `show_subject_analysis()`: Subject-wise grade distribution
- `show_complete_analytics()`: Full dashboard

### `app_v2.py`
Main Streamlit application with UI and orchestration.

---

## 📊 Analytics Metrics

### Statistics Calculated
- **Total Students**: Count of records
- **Pass Rate**: Percentage of passing students
- **Average SGPA**: Mean current semester GPA
- **Highest/Lowest SGPA**: Range of semester performance
- **Average/Highest/Lowest CGPA**: Cumulative GPA statistics
- **Grade Categories**: Distribution across performance brackets

### Grade Categories
- 🌟 **Outstanding** (9.0+)
- ⭐ **Excellent** (8.0-8.9)
- 👍 **Very Good** (7.0-7.9)
- ✅ **Good** (6.0-6.9)
- ⚠️ **Average** (5.0-5.9)
- ❌ **Below Average** (<5.0)

---

## 🔐 Data Privacy

- Data is fetched directly from the official BEU API
- No data is stored on servers
- All processing happens locally in the browser
- Export files are generated on-demand and not retained

---

## 🐛 Troubleshooting

### Issue: "No results found"
- Verify registration number range is correct
- Check if the exam date is available on BEU results portal
- Ensure batch year and semester are correctly entered

### Issue: "API connection failed"
- Check your internet connection
- Verify BEU server is accessible
- Try again after a few minutes

### Issue: "Slow performance with large ranges"
- Reduce the registration number range
- Close other applications consuming network bandwidth

---

## 📈 Future Enhancements

- [ ] Semester-wise trend analysis across multiple exams
- [ ] Individual student transcript generation
- [ ] Comparative analysis between branches/colleges
- [ ] PDF export with formatting
- [ ] Downloadable reports with charts
- [ ] Historical data comparison
- [ ] Predictive analytics for performance trends

---

## 📝 API Response Format

The official BEU API returns JSON in this format:

```json
{
  "status": 200,
  "message": "Report retrieved successfully.",
  "data": {
    "semester": "III",
    "exam_held": "July/2025",
    "redg_no": "23105110005",
    "name": "STUDENT NAME",
    "father_name": "FATHER NAME",
    "mother_name": "MOTHER NAME",
    "college_code": "110",
    "college_name": "COLLEGE NAME",
    "course_code": "105",
    "course": "COURSE NAME",
    "theorySubjects": [
      {
        "code": "100302",
        "name": "SUBJECT NAME",
        "ese": "31",
        "ia": "27",
        "total": "58",
        "grade": "D",
        "credit": "3.00"
      }
    ],
    "practicalSubjects": [...],
    "sgpa": ["7.42", "7.63", "7.92", null, null, null, null, null],
    "cgpa": "7.67",
    "fail_any": "PASS"
  }
}
```

---

## 📄 License

This project is open-source under the MIT License.

---

## 👨‍💻 Author

**Aditya Kumar**
- Department of Computer Science & Engineering
- Gaya College of Engineering, under BEU Patna
- [Portfolio](https://adityakr.me)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

---

## ⚡ Performance Tips

1. **Optimal Range**: Fetch 50-100 records at a time for best performance
2. **Parallel Workers**: Default is 4 workers; adjust based on your internet speed
3. **Filtering**: Use filters to reduce data size before export
4. **Browser**: Use a modern browser (Chrome, Firefox, Edge) for best experience

---

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Verify your inputs are correct
3. Ensure BEU results portal is accessible
4. Open an issue on GitHub

---

**Last Updated**: November 2025
**Version**: 2.0
**Status**: Production Ready ✅
