import streamlit as st
import random
from dotenv import load_dotenv
from file_helper import parse_file

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Plan Management",
    page_icon="📁",
    layout="centered"
)

# App title and description
st.title("📁 Plan Management")
st.markdown("Upload a file to process and analyze it.")

# File uploader
uploaded_file = st.file_uploader(
    "Choose a file",
    type=None,  # Accept all file types
    help="Upload any file to process"
)

# Process uploaded file
if uploaded_file is not None:
    st.subheader("📄 File Details")
    st.write(f"**File Name:** {uploaded_file.name}")
    file_size = uploaded_file.size / 1024  # Convert to KB
    size_text = f"{file_size/1024:.2f} MB" if file_size > 1024 else f"{file_size:.2f} KB"
    st.write(f"**File Size:** {size_text}")

    # Add helpful instructions
    st.info("✅ Click **Process File** below to parse and analyze your uploaded file with AI.")

    # Highlighted button
    st.markdown(
        """
        <style>
        div.stButton > button:first-child {
            background-color: #2563eb;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.6em 1.2em;
            font-weight: 600;
        }
        div.stButton > button:hover {
            background-color: #1d4ed8;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    if st.button("Process File"):
        # Step 1 — File Parsing
        with st.spinner("📂 Parsing the uploaded file..."):
            import time
            time.sleep(1.5)
            result = parse_file(uploaded_file)

        st.divider()
        st.subheader("📊 Parsed Information")

        if result["type"] in ["csv", "excel"]:
            st.dataframe(result["data"])
        elif result["type"] == "json":
            st.json(result["data"])
        elif result["type"] in ["pdf", "text"]:
            st.text(result["data"])
        else:
            st.warning("⚠️ Unsupported file type. Please upload CSV, Excel, JSON, PDF, or TXT.")

        # Step 2 — Simulated AI Agent Analysis
        st.divider()
        with st.spinner("🤖 AI Agent analyzing data and applying business rules..."):
            time.sleep(5)  # Simulate agent processing

        # Step 3 — Show analysis result
        st.success("✅ AI Agent has completed the analysis!")
        result_message = random.choice([
            "All rules passed successfully ✅",
            "Some values need manual review ⚠️",
            "Data inconsistencies detected ❌"
        ])
        st.info(f"**Result:** {result_message}")

else:
    st.info("👆 Please upload a file to get started.")

# Footer
st.divider()
st.caption("Plan Management v1.0")
