import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent } from '@/components/ui/card';

const ConversationHistory = () => {
  const [messages, setMessages] = useState([
    { id: 1, sender: 'User', content: 'Write a Python function to calculate factorial.', editable: false },
    { id: 2, sender: 'Coder', content: 'Here\'s a Python function to calculate factorial:', editable: false },
    { id: 3, sender: 'Coder', content: 'def factorial(n):\n    if n == 0 or n == 1:\n        return 1\n    else:\n        return n * factorial(n-1)', editable: false },
    { id: 4, sender: 'User', content: 'Execution result: Success', editable: false },
    { id: 5, sender: 'Coder', content: 'Great! The factorial function has been implemented successfully. You can now use this function to calculate factorials. For example, factorial(5) would return 120.', editable: false },
  ]);

  const [editingId, setEditingId] = useState(null);
  const [editContent, setEditContent] = useState('');

  const handleEdit = (id, content) => {
    setEditingId(id);
    setEditContent(content);
  };

  const handleSave = (id) => {
    setMessages(messages.map(msg => 
      msg.id === id ? { ...msg, content: editContent } : msg
    ));
    setEditingId(null);
  };

  const handleDelete = (id) => {
    setMessages(messages.filter(msg => msg.id !== id));
  };

  return (
    <div className="max-w-2xl mx-auto p-4">
      <h2 className="text-2xl font-bold mb-4">Conversation History</h2>
      {messages.map((message) => (
        <Card key={message.id} className="mb-4">
          <CardContent className="p-4">
            <div className="flex justify-between items-center mb-2">
              <span className="font-semibold">{message.sender}</span>
              <div>
                {editingId !== message.id && (
                  <>
                    <Button variant="ghost" size="sm" onClick={() => handleEdit(message.id, message.content)}>
                      ✏️ Edit
                    </Button>
                    <Button variant="ghost" size="sm" onClick={() => handleDelete(message.id)}>
                      🗑️ Delete
                    </Button>
                  </>
                )}
              </div>
            </div>
            {editingId === message.id ? (
              <div>
                <Input
                  value={editContent}
                  onChange={(e) => setEditContent(e.target.value)}
                  className="mb-2"
                />
                <Button onClick={() => handleSave(message.id)} className="mr-2">
                  💾 Save
                </Button>
                <Button variant="outline" onClick={() => setEditingId(null)}>
                  ❌ Cancel
                </Button>
              </div>
            ) : (
              <pre className="whitespace-pre-wrap">{message.content}</pre>
            )}
          </CardContent>
        </Card>
      ))}
    </div>
  );
};

export default ConversationHistory;
