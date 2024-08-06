import streamlit as st
import pandas as pd
import json
import os

# File to store the conversation history
HISTORY_FILE = "conversation_history.json"

@st.cache_data
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
    ]

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)

def main():
    st.set_page_config(page_title="Conversation History", layout="wide")
    st.title("Conversation History")

    history = load_history()

    # Display and manage messages
    for i, message in enumerate(history):
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            new_content = st.text_area(f"Message {message['id']} - {message['sender']}", 
                                       value=message['content'], 
                                       key=f"message_{message['id']}", 
                                       height=100)
            if new_content != message['content']:
                message['content'] = new_content
                save_history(history)
                st.experimental_rerun()
        
        with col2:
            if st.button("✏️ Save", key=f"save_{message['id']}"):
                save_history(history)
                st.success("Changes saved!")
        
        with col3:
            if st.button("🗑️ Delete", key=f"delete_{message['id']}"):
                del history[i]
                save_history(history)
                st.experimental_rerun()
        
        st.markdown("---")

    # Add new message
    st.subheader("Add New Message")
    new_sender = st.selectbox("Sender", ["User", "Coder"])
    new_content = st.text_area("Content")
    if st.button("➕ Add Message"):
        new_id = max([m['id'] for m in history], default=0) + 1
        history.append({
            "id": new_id,
            "sender": new_sender,
            "content": new_content
        })
        save_history(history)
        st.experimental_rerun()

    # Export to CSV
    if st.button("📁 Export to CSV"):
        df = pd.DataFrame(history)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download CSV",
            data=csv,
            file_name="conversation_history.csv",
            mime="text/csv",
        )

if __name__ == "__main__":
    main()
