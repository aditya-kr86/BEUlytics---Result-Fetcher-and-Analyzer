# BEUlytics v2.0 - Quick Start Guide

## Installation & Setup

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
streamlit run app_v2.py
```

The app will automatically open in your browser at `http://localhost:8501`

---

## How to Use

### First Time Setup
1. The sidebar on the left contains all configuration options
2. Scroll down to see the form (it's collapsible)
3. Fill in the required fields

### Configuration Fields

#### Exam Details Section
- **Semester**: Select from 1st to 8th semester
- **Exam Month**: Choose the month when exam was held
- **Exam Year**: Year of exam (usually 2024 or 2025)

#### Academic Details Section
- **Batch Year**: Enter last 2 digits of batch (e.g., 23 for 2023-27 batch)
- **Branch**: Select your engineering branch (CSE, Mechanical, Civil, etc.)
- **College**: Select your college from the dropdown list

#### Registration Range Section
- **Start Reg No.**: Starting registration number (e.g., 1)
- **End Reg No.**: Ending registration number (e.g., 50)
- **Include Lateral Entry**: Check if you want to include LE students

> **Example**: To fetch 50 students' results, set Start=1 and End=50

### Fetching Results

1. Click the **"🚀 Fetch Results"** button
2. Wait for the progress bar to complete (usually 30-60 seconds depending on range)
3. You'll see "✅ Successfully fetched X results!" message

---

## Understanding the Results

### Tab 1: 📊 Analytics
Comprehensive dashboard with 9 different visualizations:

1. **Key Metrics**: Total students, pass rate, average SGPA
2. **SGPA Distribution**: Histogram showing how students are distributed
3. **Performance Categories**: Pie chart showing Outstanding/Excellent/Very Good etc.
4. **Top 10 Performers**: Students with highest SGPA
5. **College-wise Analysis**: Performance metrics by college
6. **Course-wise Analysis**: Performance metrics by course
7. **Subject-wise Analysis**: Grade distribution for each subject
8. **Pass/Fail Analysis**: Overall and college-wise pass rates
9. **SGPA vs CGPA Correlation**: Scatter plot showing relationship

### Tab 2: 🔍 Data View
Raw data table with ability to:
- Select which columns to display
- Download as CSV or Excel
- Scroll through all records

### Tab 3: ⚙️ Filter & Sort
Advanced filtering and sorting:

**Filters Available**:
- College (multi-select)
- Course (multi-select)
- Status (Pass/Fail)
- SGPA Range (slider)

**Sorting Options**:
- SGPA (High to Low or Low to High)
- CGPA (High to Low or Low to High)
- Student Name (A-Z)
- Registration Number
- College Name
- Course Name

**Example Workflow**:
1. Filter by College = "Gaya College of Engineering"
2. Filter SGPA Range = 7.0 to 9.0
3. Sort by SGPA (High to Low)
4. View top performers from your college

### Tab 4: 📥 Export
Download your results:

**Available Formats**:
- **CSV**: Universal format, works with Excel
- **Excel**: Formatted spreadsheet file (.xlsx)
- **JSON**: For programmatic use

**Features**:
- Files automatically timestamped
- All data included in export
- Choose format and click to download

---

## Tips & Tricks

### ⚡ Performance Tips
- **Smaller ranges**: Fetch 50-100 students at a time for faster results
- **Use filters**: Filter data before exporting to reduce file size
- **Lateral entry**: Only check "Include Lateral Entry" if needed (adds more API calls)

### 📊 Analytics Tips
- **Hover over charts**: Hover over any chart to see exact values
- **Click legend items**: Click legend items to toggle visibility
- **Expand charts**: Charts can be expanded by clicking the expand icon

### 🔍 Search Tips
- **Use multiple filters**: Combine college + SGPA range for precise results
- **Reset filters**: Use filter interface to reset to all data
- **Export filtered data**: Filters apply to exported files too

---

## Example Use Cases

### Use Case 1: Find Top Students in Your College
1. Go to **Tab 3: Filter & Sort**
2. Select your college in the College filter
3. Sort by SGPA (High to Low)
4. Top students appear first

### Use Case 2: Analyze Subject Performance
1. Go to **Tab 1: Analytics**
2. Scroll to "Subject-wise Grade Distribution"
3. Select a subject to see grade breakdown
4. Analyze which grades are most common

### Use Case 3: Compare Pass Rates
1. Go to **Tab 1: Analytics**
2. Scroll to "Pass/Fail Analysis"
3. View college-wise pass rates
4. Identify which colleges have highest/lowest pass rates

### Use Case 4: Export Results for Report
1. Apply desired filters in **Tab 3**
2. Go to **Tab 4: Export**
3. Select format (recommend Excel for reports)
4. Click download button

---

## Common Questions

### Q: How long does it take to fetch results?
**A**: 
- 10-20 students: ~10-20 seconds
- 50-100 students: ~30-60 seconds
- 100+ students: 1-2 minutes

Depends on your internet speed and server response time.

### Q: Can I fetch results for multiple semesters?
**A**: Currently, the app fetches one semester at a time. For multiple semesters, run the app multiple times and export each separately.

### Q: What if a student appears in the "No results found"?
**A**: This usually means:
- Student registration number is incorrect
- Results haven't been published yet for that semester
- Student may have dropped out

### Q: Can I modify the exported data?
**A**: Yes! Exported Excel/CSV files can be edited in Excel or any spreadsheet application.

### Q: Where is my data stored?
**A**: Data is processed locally in your browser and is NOT stored anywhere. Each session starts fresh.

---

## Troubleshooting

### Problem: "No results found"
**Solution**:
1. Double-check registration number range
2. Verify semester and batch year are correct
3. Check if results are published on BEU portal
4. Try a smaller range first (e.g., just 1-5 students)

### Problem: App is running slowly
**Solution**:
1. Reduce the registration number range
2. Close other applications
3. Check your internet connection
4. Try again in a few minutes (server might be busy)

### Problem: Downloaded file is empty or corrupted
**Solution**:
1. Try exporting in a different format
2. Use a smaller range and try again
3. Check available disk space
4. Refresh the page and try again

### Problem: Can't see the sidebar
**Solution**:
1. Click the hamburger menu (☰) in top left
2. Or widen your browser window
3. Or use a desktop instead of mobile

---

## Advanced Usage

### Batch Processing
To process multiple ranges:

1. Fetch first batch (e.g., 1-50)
2. Export results
3. Clear browser cache or refresh page
4. Fetch next batch (e.g., 51-100)
5. Combine exports in Excel

### Data Analysis
After exporting to Excel, you can:
- Create pivot tables
- Generate your own charts
- Create custom reports
- Perform statistical analysis

### Integration
Exported JSON format can be integrated into:
- Your own data analysis tools
- Database systems
- Web applications
- Data visualization platforms

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+R` | Refresh page |
| `Ctrl+S` | Open save dialog (for downloads) |
| `F11` | Full screen mode |
| `Ctrl+Q` | Exit Streamlit app |

---

## Getting Help

1. **Check README_V2.md** for detailed documentation
2. **Use the Filter & Sort** to verify your data
3. **Check BEU portal** to verify exam dates
4. **Open an issue** on GitHub with:
   - Semester and batch details
   - Exact error message
   - Steps to reproduce

---

## Next Steps

- ✅ Try fetching your own results
- ✅ Explore all 4 tabs and understand the data
- ✅ Export results in different formats
- ✅ Share with your classmates!

---

**Happy Analyzing! 📊**

For more information, see README_V2.md
