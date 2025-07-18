import React from 'react';
import { marked } from 'marked';

const ChatMessage = ({ message, isUser }) => {
  // Function to parse markdown
  const renderMarkdown = (content) => {
    if (!content) return '';
    try {
      return { __html: marked.parse(content) };
    } catch (error) {
      console.error('Error parsing markdown:', error);
      return { __html: content };
    }
  };

  
  return (
    <div className={`message ${isUser ? 'user' : 'api'}`}>
      <span className="tag">{isUser ? 'User' : 'D&D Agent'}</span>
      {isUser ? (
        <div className="message-content">
          {message}
        </div>
      ) : (
        <div 
          className="message-content"
          dangerouslySetInnerHTML={renderMarkdown(message)}
        />
      )}
    </div>
  );
};

export default ChatMessage;
