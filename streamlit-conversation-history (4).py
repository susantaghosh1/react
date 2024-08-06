import streamlit as st
import pandas as pd
import json
import os
import math
import time

# File to store the conversation history
HISTORY_FILE = "conversation_history.json"
MESSAGES_PER_PAGE = 5  # Number of messages to display per page

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return [
        {"id": 1, "sender": "User", "content": "Write a Python function to calculate factorial."},
        {"id": 2, "sender": "Coder", "content": "Here's a Python function to calculate factorial:"},
        {"id": 3, "sender": "Coder", "content": "def factorial(n):\n    if n == 0 or n == 1:\n        return 1\n    else:\n        return n * factorial(n-1)"},
        {"id": 4, "sender": "User", "content": "Execution result: Success"},
        {"id": 5, "sender": "Coder", "content": "Great! The factorial function has been implemented successfully. You can now use this function to calculate factorials. For example, factorial(5) would return 120."},
        # ... (the rest of the 15 messages you added previously)
    ]

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)

def save_application(history, app_name):
    app_data = {
        "appName": app_name,
        "conversation": history
    }
    filename = f"{app_name.replace(' ', '_')}_application.json"
    with open(filename, "w") as f:
        json.dump(app_data, f, indent=2)
    return filename

def main():
    st.set_page_config(page_title="Conversation History", layout="wide")
    st.title("Conversation History")

    if 'history' not in st.session_state:
        st.session_state.history = load_history()

    # Pagination
    total_pages = math.ceil(len(st.session_state.history) / MESSAGES_PER_PAGE)
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if "page" not in st.session_state:
            st.session_state.page = 1
        if st.button("Previous"):
            st.session_state.page = max(1, st.session_state.page - 1)
    with col2:
        st.write(f"Page {st.session_state.page} of {total_pages}")
    with col3:
        if st.button("Next"):
            st.session_state.page = min(total_pages, st.session_state.page + 1)

    start_idx = (st.session_state.page - 1) * MESSAGES_PER_PAGE
    end_idx = start_idx + MESSAGES_PER_PAGE
    page_history = st.session_state.history[start_idx:end_idx]

    # Display and manage messages
    for message in page_history:
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            new_content = st.text_area(f"Message {message['id']} - {message['sender']}", 
                                       value=message['content'], 
                                       key=f"message_{message['id']}", 
                                       height=100)
        
        with col2:
            if st.button("✏️ Save", key=f"save_{message['id']}"):
                message['content'] = new_content
                save_history(st.session_state.history)
                st.success("Changes saved!")
        
        with col3:
            if st.button("🗑️ Delete", key=f"delete_{message['id']}"):
                st.session_state.history = [m for m in st.session_state.history if m['id'] != message['id']]
                save_history(st.session_state.history)
                st.success("Message deleted!")
                st.experimental_rerun()

    st.markdown("---")

    # Add new message
    st.subheader("Add New Message")
    new_sender = st.selectbox("Sender", ["User", "Coder"])
    new_content = st.text_area("Content")
    if st.button("➕ Add Message"):
        new_id = max([m['id'] for m in st.session_state.history], default=0) + 1
        st.session_state.history.append({
            "id": new_id,
            "sender": new_sender,
            "content": new_content
        })
        save_history(st.session_state.history)
        st.session_state.page = total_pages + 1  # Move to the new last page
        st.success("New message added!")
        st.experimental_rerun()

    # Export to CSV
    if st.button("📁 Export to CSV"):
        df = pd.DataFrame(st.session_state.history)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download CSV",
            data=csv,
            file_name="conversation_history.csv",
            mime="text/csv",
        )

    # Application button and functionality
    st.markdown("---")
    st.subheader("Save as Application")
    
    # Initialize session state variables
    if 'show_popup' not in st.session_state:
        st.session_state.show_popup = False
    if 'app_name' not in st.session_state:
        st.session_state.app_name = ""

    # Button to show pop-up
    if st.button("📄 Create Application"):
        st.session_state.show_popup = True

    # Pop-up for application name input
    if st.session_state.show_popup:
        with st.form(key='app_name_form'):
            st.session_state.app_name = st.text_input("Enter Application Name", key="app_name_input")
            submit_button = st.form_submit_button(label='Submit')

            if submit_button:
                if st.session_state.app_name:
                    with st.spinner('Creating application...'):
                        filename = save_application(st.session_state.history, st.session_state.app_name)
                        time.sleep(2)  # Simulating some processing time
                    st.success(f"Application saved as {filename}")
                    st.session_state.show_popup = False
                    st.session_state.app_name = ""
                else:
                    st.error("Please enter an application name")

if __name__ == "__main__":
    main()
