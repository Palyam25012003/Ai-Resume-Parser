import os
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from pyresparser import ResumeParser

# Set Streamlit page config
st.set_page_config(page_title="Resume Parser", layout="wide")

# Sidebar menu
with st.sidebar:
    option = option_menu(
        "Select the stage", 
        ["About The App", "Single Resume File", "Bulk Resume Files"], 
        menu_icon='list', 
        icons=["info", "file-earmark-person", "files"], 
        default_index=0
    )

# About The App Section
if option == "About The App":
    st.title("📄 Resume Parser App")
    st.write(
        """
        This application helps to extract important information from resumes. 
        - Upload a **single resume file** or **multiple resumes** for batch processing.
        - Extract **name, email, phone number, skills, education, experience**, etc.
        - Supports **PDF & DOCX** resume files.
        """
    )

# Single Resume File Section
elif option == "Single Resume File":
    st.title("📌 Upload a Single Resume")
    uploaded_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])

    if uploaded_file is not None:
        with open("temp_resume."+uploaded_file.name.split('.')[-1], "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Parse the resume
        data = ResumeParser(f.name).get_extracted_data()

        # Display extracted information
        if data:
            st.subheader("Extracted Resume Details:")
            st.write(f"**Name:** {data.get('name', 'N/A')}")
            st.write(f"**Email:** {data.get('email', 'N/A')}")
            st.write(f"**Phone:** {data.get('mobile_number', 'N/A')}")
            st.write(f"**Skills:** {', '.join(data.get('skills', [])) if data.get('skills') else 'N/A'}")
            st.write(f"**Education:** {data.get('degree', 'N/A')}")
            st.write(f"**Experience:** {data.get('total_experience', 'N/A')} years")

# Bulk Resume Files Section
elif option == "Bulk Resume Files":
    st.title("📌 Upload Multiple Resumes")
    uploaded_files = st.file_uploader("Upload Multiple Resumes (PDF/DOCX)", type=["pdf", "docx"], accept_multiple_files=True)

    if uploaded_files:
        results = []
        for uploaded_file in uploaded_files:
            file_path = "temp_" + uploaded_file.name
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Parse the resume
            data = ResumeParser(file_path).get_extracted_data()

            if data:
                results.append({
                    "Name": data.get("name", "N/A"),
                    "Email": data.get("email", "N/A"),
                    "Phone": data.get("mobile_number", "N/A"),
                    "Skills": ', '.join(data.get("skills", [])) if data.get("skills") else "N/A",
                    "Education": data.get("degree", "N/A"),
                    "Experience": f"{data.get('total_experience', 'N/A')} years"
                })
            
            os.remove(file_path)  # Clean up after parsing

        # Convert results to DataFrame and display
        if results:
            df = pd.DataFrame(results)
            st.dataframe(df)

            # Option to download the results as a CSV file
            csv_file = df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download CSV", data=csv_file, file_name="parsed_resumes.csv", mime="text/csv")

