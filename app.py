import streamlit as st
import os
import subprocess
from pathlib import Path


def frontend():

    st.set_page_config()
    folder = st.file_uploader("upload PDF file",accept_multiple_files=True)
    if folder:
        dir = Path("./uploaded_pdfs")
        os.makedirs(dir,exist_ok=True)
        for i in folder:
            print(i.name)
            path = os.path.join(dir, i.name)
        
            with open(path, "wb") as f:
                    f.write(i.getvalue())
        st.success("pdf uploaded ✅")

        if st.button("start pipeline."):
            with st.spinner("summarizing and extracting keywords.."):
                args = ["python", "main.py", "-folder", dir]
                result = subprocess.run(args, capture_output=True, text=True)
                st.success("summary and keyword extracted and uploaded to mongodb sucessfully  ✅")



if __name__ == "__main__":
    frontend()
