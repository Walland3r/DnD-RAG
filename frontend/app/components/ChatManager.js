'use client';

import React, { useState, useEffect, useCallback, useRef } from 'react';
import ChatContainer from './ChatContainer';
import ChatSidebar from './ChatSidebar';


const useLocalStorage = (key, defaultValue) => {
    const [value, setValue] = useState(defaultValue);
    
    // Load from localStorage on mount
    useEffect(() => {
        if (typeof window === 'undefined') return;
        
        try {
            const saved = localStorage.getItem(key);
            if (saved) setValue(JSON.parse(saved));
        } catch (error) {
            console.error(`Error loading ${key}:`, error);
        }
    }, [key]);
    
    // Save to localStorage when value changes
    useEffect(() => {
        if (typeof window === 'undefined' || value === defaultValue) return;
        localStorage.setItem(key, JSON.stringify(value));
    }, [key, value, defaultValue]);
    
    return [value, setValue];
};

const createNewChat = () => ({
    id: `chat-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
    title: '',
    messages: [],
    lastUpdated: new Date().toISOString(),
});


const ChatManager = () => {
    
    const [chats, setChats] = useLocalStorage('dnd-chats', [createNewChat()]);
    const [activeChat, setActiveChat] = useLocalStorage('dnd-active-chat', null);
    const [sidebarOpen, setSidebarOpen] = useState(true);
    const chatContainerRef = useRef(null);

    // Set initial active chat if none selected
    useEffect(() => {
        if (!activeChat && chats.length > 0) {
            setActiveChat(chats[0].id);
        }
    }, [activeChat, chats, setActiveChat]);


    const handleNewChat = useCallback(() => {
        const newChat = createNewChat();
        setChats(prev => [newChat, ...prev]);
        setActiveChat(newChat.id);
    }, [setChats, setActiveChat]);

    const handleChatSelect = useCallback((chatId) => {
        chatContainerRef.current?.abortStream();
        setActiveChat(chatId);
    }, [setActiveChat]);

    const handleDeleteChat = useCallback((chatId) => {
        chatContainerRef.current?.abortStream();
        
        if (chats.length <= 1) {
            // Replace last chat with new one
            const newChat = createNewChat();
            setChats([newChat]);
            setActiveChat(newChat.id);
        } else {
            // Remove chat and switch to another if needed
            setChats(prev => prev.filter(chat => chat.id !== chatId));
            if (activeChat === chatId) {
                const remainingChats = chats.filter(chat => chat.id !== chatId);
                setActiveChat(remainingChats[0]?.id || null);
            }
        }
    }, [chats, activeChat, setChats, setActiveChat]);

    const updateChatMessages = useCallback((chatId, messages) => {
        setChats(prev => prev.map(chat =>
            chat.id === chatId ? {
                ...chat,
                messages,
                lastUpdated: new Date().toISOString(),
                title: chat.title || (messages[0]?.content.slice(0, 30) || '')
            } : chat
        ));
    }, [setChats]);


    const currentChat = chats.find(chat => chat.id === activeChat);

    return (
        <div className="chat-manager">
            <button
                className="sidebar-toggle"
                onClick={() => setSidebarOpen(!sidebarOpen)}
                title={sidebarOpen ? 'Hide Sidebar' : 'Show Sidebar'}
            >
                ☰
            </button>

            <div className={`chat-layout ${sidebarOpen ? 'sidebar-open' : 'sidebar-closed'}`}>
                {sidebarOpen && (
                    <ChatSidebar
                        chats={chats}
                        activeChat={activeChat}
                        onChatSelect={handleChatSelect}
                        onNewChat={handleNewChat}
                        onDeleteChat={handleDeleteChat}
                    />
                )}

                <div className="chat-main">
                    {currentChat ? (
                        <ChatContainer
                            ref={chatContainerRef}
                            key={currentChat.id}
                            initialMessages={currentChat.messages}
                            onMessagesChange={(messages) => updateChatMessages(currentChat.id, messages)}
                        />
                    ) : (
                        <div className="no-chat-selected">
                            <p>No chat selected</p>
                            <button onClick={handleNewChat}>Start New Chat</button>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default ChatManager;
