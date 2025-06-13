import os
import json
import warnings
import streamlit as st
import pandas as pd

from agents.classifier_agent import ClassifierAgent
from agents.json_agent import JSONAgent
from agents.email_agent import EmailAgent
from memory.memory_manager import MemoryManager
from utils.file_loader import detect_format, load_file

# Suppress unnecessary warnings
os.environ["TORCH_SHOW_CPP_STACKTRACES"] = "0"
warnings.filterwarnings("ignore", category=UserWarning)

# App Title
st.title(" Intelligent Document Routing System")

# File Upload
uploaded_file = st.file_uploader("Upload a document (PDF / JSON / Email)", type=["pdf", "json", "txt", "eml"])

if uploaded_file:
    file_name = uploaded_file.name
    file_ext = file_name.split(".")[-1].lower()

    # Save input to data/input/
    os.makedirs("data/input", exist_ok=True)
    input_path = os.path.join("data/input", file_name)
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Load file content safely
    try:
        file_content = load_file(input_path)
    except Exception as e:
        st.error(f"Failed to read file: {e}")
        st.stop()

    # Initialize agents
    memory = MemoryManager()
    classifier = ClassifierAgent(memory)
    email_agent = EmailAgent(memory)
    json_agent = JSONAgent(memory)

    # Classify and route
    format_type, intent = classifier.classify_and_route(file_content, file_ext, file_name)
    st.success(" Document successfully classified.")

    # Show classification
    st.write(f"**Detected Format:** `{format_type}`")
    st.write(f"**Detected Intent:** `{intent}`")

    # Process by agent
    result = {}
    if format_type == "Email":
        st.subheader(" Extracted Email Metadata")
        result = email_agent.process_email(file_content, file_name)
        st.json(result)

    elif format_type == "JSON":
        st.subheader(" Parsed JSON Content")
        result = json_agent.process_json(file_content, file_name)
        st.json(result)

    # Save agent output
    os.makedirs("data/output", exist_ok=True)
    output_path = os.path.join("data/output", f"{file_name}.out.json")
    with open(output_path, "w", encoding="utf-8") as out_f:
        json.dump(result, out_f, indent=4)

    # Show log specific to this file
    latest_log = next(
        (entry for entry in reversed(memory.get_memory()) if entry["source"] == file_name),
        None
    )

    st.subheader(" Memory Log")
    if latest_log:
        st.json(latest_log)
    else:
        st.warning(" No memory log found for this document.")

    # Download memory CSV
    if os.path.exists("memory/memory_export.csv"):
        df = pd.read_csv("memory/memory_export.csv")
        st.download_button("⬇ Download Memory Log (CSV)", df.to_csv(index=False), file_name="memory_log.csv")
    else:
        st.warning("No memory log available for download yet.")

    st.success(" Document processed and logged successfully!")

else:
    st.info(" Please upload a document to begin.")
