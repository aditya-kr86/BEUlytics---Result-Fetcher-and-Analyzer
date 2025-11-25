# BUG FIXES - November 26, 2025

## Issues Fixed

### 1. ✅ ValueError: Unknown format code 'f' for object of type 'str'
**Location**: `app.py` (formerly `app_unified.py`), line 453-454

**Problem**: 
```python
st.metric("Avg SGPA", f"{stats['Average SGPA']:.2f}")
st.metric("Avg CGPA", f"{stats['Average CGPA']:.2f}")
```

The `get_statistics_summary()` function in `data_processor.py` returns values as **already-formatted strings** (e.g., `"7.96"`), but the app tried to format them again with `:.2f` which only works on numeric types.

**Solution**: Use the pre-formatted values directly
```python
st.metric("Avg SGPA", stats['Average SGPA'])
st.metric("Avg CGPA", stats['Average CGPA'])
```

---

### 2. ✅ Multiselect Not Updating Display
**Location**: `app.py`, line 328-335 (v2 Tab 2: Data View)

**Problem**: 
```python
display_cols = st.multiselect(
    "Select columns to display",
    options=df.columns.tolist(),
    default=[...]
)
```

Missing `key` parameter caused Streamlit to not properly track selection changes.

**Solution**: Added unique key to multiselect
```python
display_cols = st.multiselect(
    "Select columns to display",
    options=df.columns.tolist(),
    default=[...],
    key="v2_display_cols"  # ← Added this
)
```

Also added fallback message when no columns selected:
```python
if display_cols:
    st.dataframe(df[display_cols], use_container_width=True, hide_index=True)
else:
    st.info("Please select at least one column to display.")
```

---

### 3. ✅ File Renaming
**Before**:
- `app.py` (old v1 legacy scraper)
- `app_v2.py` (API-based version)
- `app_unified.py` (new combined version)

**After**:
- `app.py` (NEW - unified version with toggle)
- `app_v1.py` (old v1 code - for reference)
- `app_v2.py` (old v2 code - removed, kept only references)

**Command executed**:
```bash
mv app.py app_v1.py
mv app_unified.py app.py
```

---

## Current Status

✅ **All bugs fixed!**

- Formatting error resolved
- Multiselect now updates properly
- Files renamed as requested
- App running at: `http://localhost:8502`

### To Start the App
```bash
streamlit run app.py
```

### Features Working
- ✅ Version toggle (v1 and v2)
- ✅ v2 simplified input form
- ✅ v1 legacy access
- ✅ Data view with column selection
- ✅ Filter & Sort functionality
- ✅ Analytics and exports
- ✅ All statistics displaying correctly

---

## Technical Notes

**Stats Return Type Change**: 
- The `get_statistics_summary()` function in `data_processor.py` pre-formats numeric values as strings for display
- Values like `Average SGPA` are returned as `"7.96"` (string), not `7.96` (float)
- This is intentional for consistent display across all metrics

**Streamlit Async Warnings**:
- Python 3.13 has known compatibility issues with Streamlit's event loop
- These are background warnings, not app-breaking errors
- App still functions correctly despite the exception messages
