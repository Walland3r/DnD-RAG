'use client';

import React from 'react';
import { useKeycloak } from '../contexts/KeycloakContext';

const ChatSidebar = ({ chats, activeChat, onChatSelect, onNewChat, onDeleteChat }) => {
  const { userInfo, logout } = useKeycloak();
  return (
    <div className="chat-sidebar">
      <div className="sidebar-header">
        <div className="header-top">
          {userInfo && (
            <div className="user-profile">
              <span className="user-name">
                Hello {userInfo.username}!
              </span>
              <button onClick={logout} className="logout-button">
                Sign Out
              </button>
            </div>
          )}
        </div>
        <div className="header-bottom">
          <span>Chat Sessions</span>
          <button 
            className="new-chat-btn"
            onClick={onNewChat}
            title="Start New Chat"
          >
            + New Chat
          </button>
        </div>
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
                {chat.title || `New chat`}
              </div>
              <div className="chat-preview">
                {chat.messages.length > 0 
                  ? chat.messages[0].content.slice(0, 100) + '...'
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
