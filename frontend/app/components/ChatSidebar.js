'use client';

import React from 'react';

const ChatSidebar = ({ chats, activeChat, onChatSelect, onNewChat, onDeleteChat }) => {
  return (
    <div className="chat-sidebar">
      <div className="sidebar-header">
        <h3>Chat Sessions</h3>
        <button 
          className="new-chat-btn"
          onClick={onNewChat}
          title="Start New Chat"
        >
          + New Chat
        </button>
      </div>
      
      <div className="chat-list">
        {chats.map((chat) => (
          <div 
            key={chat.id}
            className={`chat-item ${activeChat === chat.id ? 'active' : ''}`}
            onClick={() => onChatSelect(chat.id)}
          >
            <div className="chat-item-content">
              <div className="chat-title">
                {chat.title || `Chat ${chat.id.slice(0, 8)}...`}
              </div>
              <div className="chat-preview">
                {chat.messages.length > 0 
                  ? chat.messages[0].content.slice(0, 50) + '...'
                  : 'New conversation'
                }
              </div>
              <div className="chat-timestamp">
                {new Date(chat.lastUpdated).toLocaleDateString()}
              </div>
            </div>
            <button 
              className="delete-chat-btn"
              onClick={(e) => {
                e.stopPropagation();
                onDeleteChat(chat.id);
              }}
              title="Delete Chat"
            >
              ×
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ChatSidebar;
