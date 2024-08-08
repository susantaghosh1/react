import chainlit as cl
from chainlit.action import Action
import json
from datetime import datetime

# Function to handle the save action
async def save_conversation(action):
    # Get the current conversation
    conversation = cl.user_session.get("conversation")
    
    # Create a filename with current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"conversation_{timestamp}.json"
    
    # Save the conversation to a file
    with open(filename, "w") as f:
        json.dump(conversation, f, indent=2)
    
    # Send a message to the user
    await cl.Message(f"Conversation saved as {filename}").send()

# Define the custom action
save_action = Action(
    name="save_conversation",
    label="Save Conversation",
    description="Save the current conversation to a file",
)

@cl.on_chat_start
async def start():
    # Add the custom action to the interface
    await cl.Action(save_action).send()

@cl.action_callback("save_conversation")
async def on_action(action):
    await save_conversation(action)

@cl.on_message
async def main(message: str):
    # Your main chat logic here
    response = f"You said: {message}"
    await cl.Message(response).send()

    # Store the conversation in the user session
    if "conversation" not in cl.user_session:
        cl.user_session.set("conversation", [])
    cl.user_session.get("conversation").append({"user": message, "assistant": response})
