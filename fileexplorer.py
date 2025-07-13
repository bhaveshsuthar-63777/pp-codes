import os
import shutil
import streamlit as st
import datetime
from google.generativeai import configure, GenerativeModel


configure(api_key="AIzaSyAahVHydAs0DFICM-DjWezaTWG6CzCkkog")
model = GenerativeModel("gemini-1.5-flash")
def list_files(directory):
    try:
        entries = []
        for file in os.listdir(directory):
            path = os.path.join(directory, file)
            size = os.path.getsize(path)
            modified = datetime.datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y-%m-%d %H:%M:%S')
            file_type = "Folder" if os.path.isdir(path) else "File"
            entries.append({
                "Name": file,
                "Size (KB)": round(size / 1024, 2),
                "Type": file_type,
                "Modified": modified
            })
        return entries
    except Exception as e:
        return f"Error: {e}"

def rename_file(directory, old_name, new_name):
    try:
        os.rename(os.path.join(directory, old_name), os.path.join(directory, new_name))
        return "✅ Renamed successfully."
    except Exception as e:
        return f"❌ Error: {e}"

def delete_path(directory, name):
    try:
        full_path = os.path.join(directory, name)
        if os.path.isfile(full_path):
            os.remove(full_path)
        elif os.path.isdir(full_path):
            shutil.rmtree(full_path)
        else:
            return "⚠️ Invalid file or folder name."
        return "🗑️ Deleted successfully."
    except Exception as e:
        return f"❌ Error: {e}"

def create_dir(directory, folder_name):
    try:
        os.makedirs(os.path.join(directory, folder_name), exist_ok=True)
        return "📁 Directory created successfully."
    except Exception as e:
        return f"❌ Error: {e}"

def interpret_query(query, file_info_list):
    file_names = [item["Name"] for item in file_info_list]
    prompt = f"""
    Given this list of files and folders:
    {file_names}
    Respond to this query: "{query}"
    Return only relevant file/folder names.
    """
    response = model.generate_content(prompt)
    return response.text


st.set_page_config(page_title="SmartFile AI", layout="wide")
st.title("📁 SmartFile AI - Intelligent File Manager")

# User input
directory = st.text_input("📂 Enter the directory path you want to manage")

st.sidebar.header("⚙️ Choose an Action")
action = st.sidebar.radio("Select Operation", [
    "List Files", "Rename File", "Delete File/Folder", 
    "Create Directory", "AI File Search", "Folder Summary"
])

if directory:
    if action == "List Files":
        result = list_files(directory)
        if isinstance(result, list):
            sort_by = st.selectbox("Sort by", ["Name", "Size (KB)", "Type", "Modified"])
            sort_order = st.radio("Order", ["Ascending", "Descending"], horizontal=True)

            result.sort(key=lambda x: x[sort_by], reverse=(sort_order == "Descending"))
            st.dataframe(result)
        else:
            st.error(result)

    elif action == "Rename File":
        old_name = st.text_input("🔤 Old file/folder name")
        new_name = st.text_input("🆕 New name")
        if st.button("Rename"):
            st.success(rename_file(directory, old_name, new_name))

    elif action == "Delete File/Folder":
        name = st.text_input("🗑️ Enter name to delete")
        if st.button("Delete"):
            st.warning(delete_path(directory, name))

    elif action == "Create Directory":
        folder_name = st.text_input("📂 New folder name")
        if st.button("Create"):
            st.success(create_dir(directory, folder_name))

    elif action == "AI File Search":
        query = st.text_input("💬 Ask about files (e.g., 'Show all PDFs')")
        files = list_files(directory)
        if st.button("Search") and isinstance(files, list):
            response = interpret_query(query, files)
            st.info(response)

    elif action == "Folder Summary":
        files = list_files(directory)
        if st.button("Summarize") and isinstance(files, list):
            summary_prompt = f"Summarize the contents of the following files and folders:\n{[f['Name'] for f in files]}"
            response = model.generate_content(summary_prompt)
            st.write(response.text)
else:
    st.info("👆 Enter a valid directory path to begin.")

st.markdown("---")
st.caption("🚀 Built with by Bhavesh Suthar")