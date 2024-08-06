import streamlit as st
import pandas as pd

def main():
    st.set_page_config(page_title="Conversation History", layout="wide")
    st.title("Conversation History")

    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = [
            {"id": 1, "sender": "User", "content": "Write a Python function to calculate factorial."},
            {"id": 2, "sender": "Coder", "content": "Here's a Python function to calculate factorial:"},
            {"id": 3, "sender": "Coder", "content": "def factorial(n):\n    if n == 0 or n == 1:\n        return 1\n    else:\n        return n * factorial(n-1)"},
            {"id": 4, "sender": "User", "content": "Execution result: Success"},
            {"id": 5, "sender": "Coder", "content": "Great! The factorial function has been implemented successfully. You can now use this function to calculate factorials. For example, factorial(5) would return 120."},
        ]

    # Display and manage messages
    for i, message in enumerate(st.session_state.messages):
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        
        with col1:
            st.text_area(f"Message {message['id']} - {message['sender']}", 
                         value=message['content'], 
                         key=f"message_{message['id']}", 
                         height=100)
        
        with col2:
            if st.button("✏️ Edit", key=f"edit_{message['id']}"):
                st.session_state.editing = message['id']
                st.session_state.edit_content = message['content']
        
        with col3:
            if st.button("💾 Save", key=f"save_{message['id']}"):
                if st.session_state.get('editing') == message['id']:
                    st.session_state.messages[i]['content'] = st.session_state[f"message_{message['id']}"]
                    st.session_state.editing = None
                    st.success("Message updated!")
                    st.experimental_rerun()
        
        with col4:
            if st.button("🗑️ Delete", key=f"delete_{message['id']}"):
                st.session_state.messages.pop(i)
                st.experimental_rerun()
        
        st.markdown("---")

    # Add new message
    st.subheader("Add New Message")
    new_sender = st.selectbox("Sender", ["User", "Coder"])
    new_content = st.text_area("Content")
    if st.button("➕ Add Message"):
        new_id = max([m['id'] for m in st.session_state.messages]) + 1
        st.session_state.messages.append({
            "id": new_id,
            "sender": new_sender,
            "content": new_content
        })
        st.success("New message added!")
        st.experimental_rerun()

    # Export to CSV
    if st.button("📁 Export to CSV"):
        df = pd.DataFrame(st.session_state.messages)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download CSV",
            data=csv,
            file_name="conversation_history.csv",
            mime="text/csv",
        )

if __name__ == "__main__":
    main()
