import streamlit as st
import random

from agents.standard import StandardAgent
from helpers.file_helper import parse_file
from dotenv import load_dotenv

from helpers.steamlist_helper import NIDSAgent
from agents.ichi import IchiAgent

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(page_title="Plan Management", page_icon="📁", layout="centered")

# App title and description
st.title("📁 Plan Management")
st.markdown("Upload a file that you want to process and analyze it.")

# File uploader
uploaded_file = st.file_uploader(
    "Choose a file",
    type=None,  # Accept all file types
    help="Upload any file to process",
)

agent_list: list[NIDSAgent] = [
    NIDSAgent(name="Standard Agent", description="Agent that will check line by line", agent=StandardAgent),
    NIDSAgent(name="Ichi Agent", description="Basic Fraud for NIDS invoices", agent=IchiAgent)
]

selected_agents = []
if uploaded_file is not None:
    st.subheader("🤖 Choose agent")
    label_to_meta = {f"{meta.name} — {meta.description}": meta for meta in agent_list}
    choice = st.selectbox(
        "Pick one agent",
        options=list(label_to_meta.keys()),
        index=0,
        key="agent_select",
    )
    selected_agents = [label_to_meta[choice]] if choice else []

# Process uploaded file
if uploaded_file is not None:
    st.subheader("📄 File Details")
    st.write(f"**File Name:** {uploaded_file.name}")
    file_size = uploaded_file.size / 1024  # Convert to KB
    size_text = (
        f"{file_size/1024:.2f} MB" if file_size > 1024 else f"{file_size:.2f} KB"
    )
    st.write(f"**File Size:** {size_text}")

    # Add helpful instructions
    st.info(
        "✅ Click **Process File** below to parse and analyze your uploaded file with AI."
    )

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
        unsafe_allow_html=True,
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
            st.warning(
                "⚠️ Unsupported file type. Please upload CSV, Excel, JSON, PDF, or TXT."
            )

        # Step 2 — Simulated AI Agent Analysis
        st.divider()
        if not selected_agents:
            st.warning("Select at least one agent")
        else:
            for meta in selected_agents:
                with st.spinner(f"Running {meta.name}..."):
                    try:
                        agent_instance = meta.agent(model="gpt-4o-mini")
                        analysis = agent_instance.process(result["data"])
                        st.subheader(f"🤖 Analysis by {meta.name}")
                        st.write(f"**Is Valid:** {analysis.is_valid}")
                        st.write(f"**Reason:** {analysis.reason}")
                    except Exception as e:
                        st.error(f"Error running {meta.name}: {e}")

else:
    st.info("👆 Please upload a file to get started.")

# Footer
st.divider()
st.caption("Plan Management v1.0")
