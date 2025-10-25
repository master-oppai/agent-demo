import streamlit as st
import pandas as pd
import json
from io import BytesIO
from PyPDF2 import PdfReader


def parse_file(uploaded_file):
    filename = uploaded_file.name.lower()

    # CSV
    if filename.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
        return {"type": "csv", "data": df.head().to_dict(orient="records")}

    # Excel
    elif filename.endswith((".xls", ".xlsx")):
        df = pd.read_excel(uploaded_file)
        return {"type": "excel", "data": df.head().to_dict(orient="records")}

    # JSON
    elif filename.endswith(".json"):
        data = json.load(uploaded_file)
        return {"type": "json", "data": data}

    # PDF
    elif filename.endswith(".pdf"):
        pdf = PdfReader(uploaded_file)
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""
        return {"type": "pdf", "data": text[:1000]}  # Preview first 1000 chars

    # Plain text
    elif filename.endswith((".txt", ".log")):
        content = uploaded_file.read().decode("utf-8", errors="ignore")
        return {"type": "text", "data": content[:1000]}

    # Unsupported
    else:
        return {"type": "unknown", "data": None}
