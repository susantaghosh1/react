from fastui import FastUI, AnyComponent, components as c
from fastui.components.display import DisplayMode, DisplayLookup
from fastui.events import GoToEvent, BackEvent
from fastui.forms import FastUIForm
from fastui.components.links import navigate
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import csv
from io import StringIO

app = FastAPI()
ui = FastUI(app)

class Message(BaseModel):
    id: int
    sender: str
    content: str

class ConversationState(BaseModel):
    messages: List[Message] = [
        Message(id=1, sender="User", content="Write a Python function to calculate factorial."),
        Message(id=2, sender="Coder", content="Here's a Python function to calculate factorial:"),
        Message(id=3, sender="Coder", content="def factorial(n):\n    if n == 0 or n == 1:\n        return 1\n    else:\n        return n * factorial(n-1)"),
        Message(id=4, sender="User", content="Execution result: Success"),
        Message(id=5, sender="Coder", content="Great! The factorial function has been implemented successfully. You can now use this function to calculate factorials. For example, factorial(5) would return 120."),
    ]

state = ConversationState()

@ui.page('/')
def conversation_history() -> List[AnyComponent]:
    return [
        c.Page(
            components=[
                c.Heading(text="Conversation History", level=1),
                c.Table(
                    data=state.messages,
                    columns=[
                        DisplayLookup(field='sender', header='Sender'),
                        DisplayLookup(field='content', header='Content'),
                    ],
                    actions=[
                        c.Button(
                            text="✏️ Edit",
                            on_click=navigate(f'/edit/{{item.id}}'),
                        ),
                        c.Button(
                            text="🗑️ Delete",
                            on_click=c.FireEvent(name='delete', payload={'id': '{{item.id}}'}),
                        ),
                    ],
                ),
                c.Button(text="➕ Add New Message", on_click=navigate('/add')),
                c.Button(text="📁 Export to CSV", on_click=navigate('/export')),
            ]
        )
    ]

@ui.page('/edit/{id:int}')
def edit_message(id: int) -> List[AnyComponent]:
    message = next((m for m in state.messages if m.id == id), None)
    if not message:
        return [c.Paragraph(text="Message not found")]
    
    return [
        c.Page(
            components=[
                c.Heading(text=f"Edit Message {id}", level=2),
                c.Form(
                    form_fields=[
                        c.TextInput(name="sender", label="Sender", initial=message.sender),
                        c.TextArea(name="content", label="Content", initial=message.content),
                    ],
                    submit_url=f"/api/edit/{id}",
                    submit_button_text="💾 Save Changes",
                ),
                c.Button(text="↩️ Back", on_click=BackEvent()),
            ]
        )
    ]

@ui.page('/add')
def add_message() -> List[AnyComponent]:
    return [
        c.Page(
            components=[
                c.Heading(text="Add New Message", level=2),
                c.Form(
                    form_fields=[
                        c.Select(name="sender", label="Sender", options=["User", "Coder"]),
                        c.TextArea(name="content", label="Content"),
                    ],
                    submit_url="/api/add",
                    submit_button_text="➕ Add Message",
                ),
                c.Button(text="↩️ Back", on_click=BackEvent()),
            ]
        )
    ]

@ui.page('/export')
def export_csv() -> List[AnyComponent]:
    csv_content = generate_csv()
    return [
        c.Page(
            components=[
                c.Heading(text="Export Conversation History", level=2),
                c.Paragraph(text="Click the button below to download the conversation history as a CSV file."),
                c.DownloadButton(
                    text="⬇️ Download CSV",
                    filename="conversation_history.csv",
                    data=csv_content,
                    mime="text/csv",
                ),
                c.Button(text="↩️ Back to Conversation", on_click=navigate('/')),
            ]
        )
    ]

@app.post("/api/edit/{id}")
def edit_message_api(id: int, form: FastUIForm):
    message = next((m for m in state.messages if m.id == id), None)
    if message:
        message.sender = form.data.get("sender", message.sender)
        message.content = form.data.get("content", message.content)
    return GoToEvent(url='/')

@app.post("/api/add")
def add_message_api(form: FastUIForm):
    new_id = max(m.id for m in state.messages) + 1
    new_message = Message(
        id=new_id,
        sender=form.data.get("sender", ""),
        content=form.data.get("content", "")
    )
    state.messages.append(new_message)
    return GoToEvent(url='/')

@app.post("/api/delete")
def delete_message_api(id: int):
    state.messages = [m for m in state.messages if m.id != id]
    return GoToEvent(url='/')

def generate_csv():
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['id', 'sender', 'content'])
    for message in state.messages:
        writer.writerow([message.id, message.sender, message.content])
    return output.getvalue()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
