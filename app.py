"""
BEUlytics - Unified App (v1 Legacy + v2 API)
Author: Aditya Kumar
Description: Single Streamlit app with toggle between legacy scraper and new API version
"""

import streamlit as st
import pandas as pd
import os
import io
from datetime import datetime
from PIL import Image

# ============================================================================
# PAGE CONFIG & INITIALIZATION
# ============================================================================

st.set_page_config(
    page_title="BEUlytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Initialize session state
if "version" not in st.session_state:
    st.session_state.version = "v2"  # Default to v2 (API)

# ============================================================================
# COMMON CONFIGURATION
# ============================================================================

branch_codes = {
    "105": "Computer Science Engineering (CSE)",
    "101": "Civil Engineering (CE)",
    "102": "Mechanical Engineering (ME)",
    "103": "Electrical Engineering (EE)",
    "110": "Electrical and Electronics Engineering (EEE)",
    "155": "CSE (IoT)"
}

college_codes = {
    "110": "Gaya College of Engineering, Gaya",
    "108": "Bhagalpur College of Engineering, Bhagalpur",
    "107": "Muzaffarpur Institute of Technology, Muzaffarpur",
    "109": "Nalanda College of Engineering, Nalanda",
    "111": "Darbhanga College of Engineering, Darbhanga",
    "113": "Motihari College Of Engineering, Mothihari",
    "117": "Lok Nayak Jai Prakash Institute of Technology, Chhapra",
    "124": "Sershah Engineering College, Sasaram, Rohtas",
    "125": "Rashtrakavi Ramdhari Singh Dinkar College of Engineering, Begusarai",
    "126": "Bakhtiyarpur College of Engineering, Patna",
    "127": "Sitamarhi Institute of Technology, Sitamarhi",
    "128": "B.P. Mandal College of Engineering, Madhepura",
    "129": "Katihar Engineering of College, Katihar",
    "130": "Supaul College of Engineering, Supaul",
    "131": "Purnea College of Engineering, Purnea",
    "132": "Saharsa College of Engineering, Saharsa",
    "133": "Government Engineering College, Jamui",
    "134": "Government Engineering College, Banka",
    "135": "Government Engineering College, Vaishali",
    "141": "Government Engineering College, Nawada",
    "142": "Government Engineering College, Kishanganj",
    "144": "Government Engineering College, Munger",
    "145": "Government Engineering College, Sheohar",
    "146": "Government Engineering College, West Champaran",
    "147": "Government Engineering College, Aurangabad",
    "148": "Government Engineering College, Kaimur",
    "149": "Government Engineering College, Gopalganj",
    "150": "Government Engineering College, Madhubani",
    "151": "Government Engineering College, Siwan",
    "152": "Government Engineering College, Jehanabad",
    "153": "Government Engineering College, Arwal",
    "154": "Government Engineering College, Khagaria",
    "155": "Government Engineering College, Buxar",
    "156": "Government Engineering College, Bhojpur",
    "157": "Government Engineering College, Sheikhpura",
    "158": "Government Engineering College, Lakhisarai",
    "159": "Government Engineering College, Samastipur",
    "165": "Shri Phanishwar Nath Renu Engineering College, Araria",
    "102": "Vidya Vihar Institute of Technology, Purnia",
    "103": "Netaji Subhash Institute of Technology, Patna",
    "106": "Sityog Institute of Technology, Aurangabad",
    "115": "Azmet Institute of Technology, Kishanganj",
    "118": "Buddha Institute of Technology, Gaya",
    "119": "Adwaita Mission Institute of Technology, Banka",
    "121": "Moti Babu Institute of Technology, Forbesganj",
    "122": "Exalt College of Engineering & Technology, Vaishali",
    "123": "Siwan Engineering & Technical Institute, Siwan",
    "136": "Mother's Institute of Technology, Bihta, Patna",
    "139": "R.P. Sharma Institute of Technology, Patna",
    "140": "Maulana Azad College of Engineering & Technology, Patna"
}

sem_words = {
    1: "1st", 2: "2nd", 3: "3rd", 4: "4th",
    5: "5th", 6: "6th", 7: "7th", 8: "8th"
}

sem_romans = {
    1: "I", 2: "II", 3: "III", 4: "IV",
    5: "V", 6: "VI", 7: "VII", 8: "VIII"
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_statistics_summary(df):
    """Get statistics summary for v2 results"""
    total_students = len(df)
    passed = len(df[df["Status"] == "PASS"])
    failed = total_students - passed
    pass_rate = f"{(passed/total_students*100):.1f}%" if total_students > 0 else "0%"
    avg_sgpa = f"{df['Current SGPA'].mean():.2f}" if "Current SGPA" in df.columns else "N/A"
    avg_cgpa = f"{df['CGPA'].mean():.2f}" if "CGPA" in df.columns else "N/A"
    
    return {
        "Total Students": total_students,
        "Passed": passed,
        "Failed": failed,
        "Pass Rate": pass_rate,
        "Avg SGPA": avg_sgpa,
        "Avg CGPA": avg_cgpa
    }

# ============================================================================
# HEADER
# ============================================================================

col1, col2 = st.columns([2, 5])

with col1:
    logo = Image.open("beu_logo.jpeg")
    st.image(logo, width=180)

with col2:
    st.markdown(
        "<div style='font-size: 48px; font-weight: bold; padding-top: 20px;'>BEUlytics</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        """<p style='color: grey; font-size: 16px; margin-top: -10px;'>
        Visualize. Analyze. Automate. — A Data Project by 
        <a href='https://adityakr.me' target='_blank' style='text-decoration: none;'>
            <span style='font-size: 16px;'><b>Aditya Kumar</b> </span>
        </a></p>""",
        unsafe_allow_html=True
    )

# ============================================================================
# HOME TAB - VERSION SELECTOR
# ============================================================================

st.markdown("---")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("### 🔄 Select Version")
    version = st.radio(
        "Choose between legacy scraper (v1) or new API-based version (v2):",
        options=["v1 (Legacy Scraper)", "v2 (Official API)"],
        index=1,
        key="version_selector"
    )
    
    if "v1" in version:
        st.session_state.version = "v1"
    else:
        st.session_state.version = "v2"

st.markdown("---")

# ============================================================================
# VERSION 1: LEGACY SCRAPER
# ============================================================================

if st.session_state.version == "v1":
    from scraper import fetch_all_results
    from analytics import show_analytics
    
    st.header("📊 BEU Result Fetcher & Analyzer (v1 - Legacy)")
    
    with st.form("result_form_v1"):
        col1, col2 = st.columns(2)
        
        with col1:
            semester = st.selectbox("Semester", options=list(range(1, 9)), format_func=lambda x: f"{x} ({sem_words[x]})", key="sem_v1")
            batch = st.number_input("Batch Year (Last two digits)", min_value=20, max_value=30, value=23, key="batch_v1")
            branch = st.selectbox("Branch", options=list(branch_codes.keys()), format_func=lambda x: branch_codes[x], key="branch_v1")
        
        with col2:
            college = st.selectbox("College", options=list(college_codes.keys()), format_func=lambda x: college_codes[x], key="college_v1")
            start_reg = st.number_input("Start Reg No.", min_value=1, max_value=999, value=1, key="start_reg_v1")
            end_reg = st.number_input("End Reg No.", min_value=1, max_value=999, value=10, key="end_reg_v1")
        
        is_lateral = st.selectbox("Include LE Students?", options=["No", "Yes"], key="lateral_v1")
        view_mode = st.selectbox("View Mode", options=["regno", "cgpa", "semester"], key="view_v1")
        submitted_v1 = st.form_submit_button("Fetch Results (v1)")
    
    if submitted_v1:
        if start_reg > end_reg:
            st.error("Start Reg No. cannot be greater than End Reg No.")
        else:
            with st.spinner("Fetching results..."):
                reg_batch = batch
                year = int(2000 + batch + (0.5 * semester))
                
                start_full_reg_no = f"{reg_batch}{branch}{college}{start_reg:03d}"
                end_full_reg_no = f"{reg_batch}{branch}{college}{end_reg:03d}"
                
                url_primary = f"https://results.beup.ac.in/ResultsBTech{sem_words[semester]}Sem{year}_B20{batch}Pub.aspx?Sem={sem_romans[semester]}&RegNo="
                url_secondary = f"https://results.beup.ac.in/ResultsBTech{sem_words[semester]}Sem{year}Pub.aspx?Sem={sem_romans[semester]}&RegNo="
                
                test_end_no = min(int(start_full_reg_no) + 4, int(end_full_reg_no))
                test_results = fetch_all_results(url_primary, int(start_full_reg_no), test_end_no)
                
                if test_results:
                    results = fetch_all_results(url_primary, int(start_full_reg_no), int(end_full_reg_no))
                    if semester > 2 and is_lateral == "Yes":
                        le_start_full_reg_no = f"{reg_batch+1}{branch}{college}901"
                        le_end_full_reg_no = f"{reg_batch+1}{branch}{college}930"
                        le_results = fetch_all_results(url_primary, int(le_start_full_reg_no), int(le_end_full_reg_no))
                else:
                    results = fetch_all_results(url_secondary, int(start_full_reg_no), int(end_full_reg_no))
                    if semester > 2 and is_lateral == "Yes":
                        le_start_full_reg_no = f"{reg_batch+1}{branch}{college}901"
                        le_end_full_reg_no = f"{reg_batch+1}{branch}{college}930"
                        le_results = fetch_all_results(url_secondary, int(le_start_full_reg_no), int(le_end_full_reg_no))
                
                if results:
                    df = pd.DataFrame(results)
                    if semester > 2 and is_lateral == "Yes":
                        le_df = pd.DataFrame(le_results)
                        df = pd.concat([df, le_df], ignore_index=True)
                    
                    if view_mode == "cgpa":
                        df["Sem Cur. CGPA"] = pd.to_numeric(df["Sem Cur. CGPA"], errors='coerce')
                        df = df.sort_values(by="Sem Cur. CGPA", ascending=False)
                    elif view_mode == "semester":
                        df["Current SGPA"] = pd.to_numeric(df["Current SGPA"], errors="coerce")
                        df = df.sort_values(by="Current SGPA", ascending=False)
                    
                    st.session_state.df_v1 = df
                    st.success("Results fetched successfully!")
                else:
                    st.error("Data Not Found. Please verify your inputs.")
    
    if "df_v1" in st.session_state:
        st.dataframe(st.session_state.df_v1)
        show_analytics(st.session_state.df_v1)

# ============================================================================
# VERSION 2: OFFICIAL API
# ============================================================================

else:
    from api_scraper import fetch_semester_results
    from data_processor import process_api_response
    from enhanced_analytics import show_enhanced_analytics
    
    st.header("📊 BEU Results Analyzer (v2 - Official API)")
    st.markdown("*Fetches results from the official BEU API*")
    
    with st.form("result_form_v2"):
        col1, col2 = st.columns(2)
        
        with col1:
            reg_start = st.number_input("Start Reg No. (e.g., 1)", min_value=1, max_value=999, value=1, key="reg_start_v2")
            reg_end = st.number_input("End Reg No. (e.g., 50)", min_value=1, max_value=999, value=50, key="reg_end_v2")
            branch = st.selectbox("Branch", options=list(branch_codes.keys()), format_func=lambda x: branch_codes[x], key="branch_v2")
            exam_month = st.selectbox("Exam Month", options=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], index=6, key="exam_month_v2")
        
        with col2:
            college = st.selectbox("College", options=list(college_codes.keys()), format_func=lambda x: college_codes[x], key="college_v2")
            # Default to semester 3 (index 2 in 1..8 list)
            semester = st.selectbox("Semester", options=list(range(1, 9)), format_func=lambda x: f"{x} ({sem_words[x]})", index=2, key="sem_v2")
            batch = st.number_input("Batch (e.g., 23 for 2023-27)", min_value=20, max_value=30, value=23, key="batch_v2")
            exam_year = st.number_input("Exam Year", min_value=2020, max_value=2030, value=2025, key="exam_year_v2")
        
        include_le = st.checkbox("Include LE (Lateral Entry) Students", value=False, key="include_le_v2")
        submitted_v2 = st.form_submit_button("🔍 Fetch Results")
    
    if submitted_v2:
        if reg_start > reg_end:
            st.error("Start Reg No. cannot be greater than End Reg No.")
        else:
            with st.spinner("Fetching results from official BEU API..."):
                try:
                    results = fetch_semester_results(
                        reg_start, 
                        reg_end, 
                        branch, 
                        college, 
                        semester, 
                        batch, 
                        include_lateral=include_le,
                        exam_month=exam_month,
                        exam_year=exam_year
                    )
                    
                    if results and len(results) > 0:
                        df = process_api_response(results)
                        st.session_state.df_v2 = df
                        st.success(f"✅ Fetched {len(df)} student records successfully!")
                    else:
                        st.warning("⚠️ No results found. Please verify your inputs.")
                except Exception as e:
                    st.error(f"❌ Error fetching results: {str(e)}")
    
    # Display results if available
    if "df_v2" in st.session_state:
        df = st.session_state.df_v2
        
        # Tabs for different views
        tab1, tab2, tab3, tab4 = st.tabs(["📈 Analytics", "📋 Data View", "🔍 Filter & Sort", "📥 Export"])
        
        # TAB 1: ANALYTICS
        with tab1:
            st.subheader("📊 Analytics Dashboard")
            show_enhanced_analytics(df)
        
        # TAB 2: DATA VIEW
        with tab2:
            st.subheader("📋 Full Data View")
            
            cols_to_display = st.multiselect(
                "Select columns to display",
                options=df.columns.tolist(),
                default=["Registration No.", "Student Name", "College Name", "Current SGPA", "CGPA", "Status"],
                key="v2_display_cols"
            )
            
            if cols_to_display:
                st.dataframe(df[cols_to_display], use_container_width=True, hide_index=True)
            else:
                st.info("Please select at least one column to display.")
        
        # TAB 3: FILTER & SORT
        with tab3:
            st.subheader("🔍 Filter & Sort")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Filters")
                
                selected_colleges = st.multiselect(
                    "Filter by College",
                    options=df["College Name"].unique().tolist() if "College Name" in df.columns else [],
                    default=None,
                    key="college_filter_v2"
                )
                
                selected_status = st.multiselect(
                    "Filter by Status",
                    options=["PASS", "FAIL"],
                    default=["PASS", "FAIL"],
                    key="status_filter_v2"
                )
                
                sgpa_range = st.slider(
                    "SGPA Range",
                    min_value=float(df["Current SGPA"].min()),
                    max_value=float(df["Current SGPA"].max()),
                    value=(float(df["Current SGPA"].min()), float(df["Current SGPA"].max())),
                    key="sgpa_filter_v2"
                )
            
            with col2:
                st.markdown("### Sort Options")
                
                sort_option = st.selectbox(
                    "Sort by",
                    options=["SGPA High to Low", "SGPA Low to High", "CGPA High to Low", "CGPA Low to High", "Name (A-Z)", "Registration No."],
                    key="sort_option_v2"
                )
            
            # Apply filters and sorting (outside columns for proper reactivity)
            filtered_df = df.copy()
            
            if selected_colleges:
                filtered_df = filtered_df[filtered_df["College Name"].isin(selected_colleges)]
            
            if selected_status:
                filtered_df = filtered_df[filtered_df["Status"].isin(selected_status)]
            
            filtered_df = filtered_df[
                (filtered_df["Current SGPA"] >= sgpa_range[0]) &
                (filtered_df["Current SGPA"] <= sgpa_range[1])
            ]
            
            # Sort (handle NaN values properly)
            if sort_option == "SGPA High to Low":
                filtered_df = filtered_df.sort_values(by="Current SGPA", ascending=False, na_position='last').reset_index(drop=True)
            elif sort_option == "SGPA Low to High":
                filtered_df = filtered_df.sort_values(by="Current SGPA", ascending=True, na_position='last').reset_index(drop=True)
            elif sort_option == "CGPA High to Low":
                filtered_df = filtered_df.sort_values(by="CGPA", ascending=False, na_position='last').reset_index(drop=True)
            elif sort_option == "CGPA Low to High":
                filtered_df = filtered_df.sort_values(by="CGPA", ascending=True, na_position='last').reset_index(drop=True)
            elif sort_option == "Name (A-Z)":
                filtered_df = filtered_df.sort_values(by="Student Name", ascending=True).reset_index(drop=True)
            elif sort_option == "Registration No.":
                filtered_df = filtered_df.sort_values(by="Registration No.", ascending=True).reset_index(drop=True)
            
            st.markdown(f"### Results: {len(filtered_df)} records")
            st.dataframe(
                filtered_df[["Registration No.", "Student Name", "College Name", "Current SGPA", "CGPA", "Status"]],
                use_container_width=True,
                hide_index=True
            )
        
        # TAB 4: EXPORT
        with tab4:
            st.subheader("📥 Export Options")
            
            st.markdown("### Download Formats")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                csv_data = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv_data,
                    file_name=f"beu_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True,
                    key="download_csv_v2"
                )
            
            with col2:
                # Generate Excel file in memory
                excel_buffer = io.BytesIO()
                with pd.ExcelWriter(excel_buffer, engine='openpyxl') as excel_writer:
                    df.to_excel(excel_writer, sheet_name='Results', index=False)
                excel_data = excel_buffer.getvalue()
                
                st.download_button(
                    label="📥 Download Excel",
                    data=excel_data,
                    file_name=f"beu_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                    key="download_excel_v2"
                )
            
            with col3:
                json_data = df.to_json(orient='records', indent=2)
                st.download_button(
                    label="📥 Download JSON",
                    data=json_data,
                    file_name=f"beu_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True,
                    key="download_json_v2"
                )
            
            st.markdown("---")
            st.markdown("### Summary Statistics")
            
            stats = get_statistics_summary(df)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Students", stats["Total Students"])
                st.metric("Passed", stats["Passed"])
            
            with col2:
                st.metric("Failed", stats["Failed"])
                st.metric("Pass Rate", stats["Pass Rate"])
            
            with col3:
                st.metric("Avg SGPA", stats["Avg SGPA"])
                st.metric("Avg CGPA", stats["Avg CGPA"])

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: grey; margin-top: 20px;'>"
    "Made with ❤️ by <b>Aditya Kumar</b><br>"
    "Department of Computer Science & Engineering<br>"
    "Gaya College of Engineering (GCE), under BEU Patna"
    "</div>",
    unsafe_allow_html=True
)


