import React, { useState } from 'react';
import { X, Edit2, Save, MessageSquare, Code, Terminal, Database } from 'lucide-react';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';

const ConversationHistory = () => {
  const [messages, setMessages] = useState([
    { id: 1, type: 'user', content: 'Write a function to calculate factorial.' },
    { id: 2, type: 'coder', content: 'Here\'s a Python function to calculate factorial:\n\ndef factorial(n):\n    if n == 0 or n == 1:\n        return 1\n    else:\n        return n * factorial(n-1)' },
    { id: 3, type: 'execution', content: 'Function defined successfully.' },
    { id: 4, type: 'user', content: 'Can you modify it to handle negative numbers?' },
    { id: 5, type: 'coder', content: 'Certainly! Here\'s an updated version:\n\ndef factorial(n):\n    if n < 0:\n        return "Factorial is not defined for negative numbers"\n    elif n == 0 or n == 1:\n        return 1\n    else:\n        return n * factorial(n-1)' },
    { id: 6, type: 'execution', content: 'Function updated successfully.' },
  ]);

  const [editingId, setEditingId] = useState(null);
  const [editContent, setEditContent] = useState('');
  const [isSaving, setIsSaving] = useState(false);

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

  const getIcon = (type) => {
    switch(type) {
      case 'user': return <MessageSquare className="w-5 h-5" />;
      case 'coder': return <Code className="w-5 h-5" />;
      case 'execution': return <Terminal className="w-5 h-5" />;
      default: return null;
    }
  };

  const saveToDynamoDB = async () => {
    setIsSaving(true);
    try {
      const response = await fetch('/api/save-conversation', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ messages }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to save conversation');
      }
      
      alert('Conversation saved successfully!');
    } catch (error) {
      console.error('Error saving conversation:', error);
      alert('Failed to save conversation. Please try again.');
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-4 space-y-4">
      <h1 className="text-2xl font-bold mb-4">Conversation History</h1>
      {messages.map((message) => (
        <Alert key={message.id} className={`flex items-start ${message.type === 'user' ? 'bg-blue-50' : message.type === 'coder' ? 'bg-green-50' : 'bg-yellow-50'}`}>
          <div className="flex-shrink-0 mr-2">
            {getIcon(message.type)}
          </div>
          <AlertDescription className="flex-grow">
            {editingId === message.id ? (
              <textarea
                value={editContent}
                onChange={(e) => setEditContent(e.target.value)}
                className="w-full p-2 border rounded"
                rows={3}
              />
            ) : (
              <pre className="whitespace-pre-wrap">{message.content}</pre>
            )}
          </AlertDescription>
          <div className="flex-shrink-0 ml-2">
            {editingId === message.id ? (
              <Save onClick={() => handleSave(message.id)} className="w-5 h-5 cursor-pointer text-green-600" />
            ) : (
              <Edit2 onClick={() => handleEdit(message.id, message.content)} className="w-5 h-5 cursor-pointer text-blue-600" />
            )}
            <X onClick={() => handleDelete(message.id)} className="w-5 h-5 cursor-pointer text-red-600 mt-2" />
          </div>
        </Alert>
      ))}
      <Button 
        onClick={saveToDynamoDB} 
        disabled={isSaving}
        className="flex items-center"
      >
        <Database className="w-5 h-5 mr-2" />
        {isSaving ? 'Saving...' : 'Save to DynamoDB'}
      </Button>
    </div>
  );
};

export default ConversationHistory;
