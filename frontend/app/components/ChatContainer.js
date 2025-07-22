'use client';

import React, { useState, useRef, useEffect, useCallback, forwardRef, useImperativeHandle } from 'react';
import ChatMessage from './ChatMessage';
import ChatForm from './ChatForm';

const ChatContainer = forwardRef(({ initialMessages = [], onMessagesChange }, ref) => {
  const [messages, setMessages] = useState(initialMessages);
  const [isLoading, setIsLoading] = useState(false);
  const messagesRef = useRef(null);
  const abortControllerRef = useRef(null);

  // Auto-scroll on new messages
  useEffect(() => {
    const el = messagesRef.current;
    if (el) el.scrollTop = el.scrollHeight;
  }, [messages]);

  // Update messages when switching chats
  useEffect(() => {
    setMessages(initialMessages);
  }, [initialMessages]);

  // Notify parent of message changes
  useEffect(() => {
    if (onMessagesChange && messages.length > 0) {
      const timeoutId = setTimeout(() => onMessagesChange(messages), 100);
      return () => clearTimeout(timeoutId);
    }
  }, [messages, onMessagesChange]);

  // Stream abort functionality
  const abortStream = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
      setIsLoading(false);
    }
  }, []);

  // Expose abort function to parent
  useImperativeHandle(ref, () => ({ abortStream }), [abortStream]);

  // Cleanup on unmount
  useEffect(() => () => abortStream(), [abortStream]);

  const streamResponse = async (question) => {
    abortStream();
    abortControllerRef.current = new AbortController();
    
    const responseId = Date.now().toString();
    
    // Add user message and placeholder
    setMessages(prev => [
      ...prev,
      { content: question, isUser: true },
      { id: responseId, content: '⏳ Thinking...', isUser: false }
    ]);
    
    setIsLoading(true);
    
    try {
      const response = await fetch('/api/ask/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question }),
        signal: abortControllerRef.current.signal
      });
      
      if (!response.ok) throw new Error(`Error ${response.status}`);
      
      // Stream the response
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let text = '';
      
      while (true) {
        if (abortControllerRef.current?.signal.aborted) {
          reader.cancel();
          break;
        }
        
        const { done, value } = await reader.read();
        if (done) break;
        
        text += decoder.decode(value, { stream: true });
        setMessages(prev => prev.map(msg => 
          msg.id === responseId ? { ...msg, content: text } : msg
        ));
      }
    } catch (error) {
      const content = error.name === 'AbortError' 
        ? '🛑 Response cancelled' 
        : `⚠️ Error: ${error.message}`;
        
      setMessages(prev => prev.map(msg => 
        msg.id === responseId ? { ...msg, content } : msg
      ));
    } finally {
      setIsLoading(false);
      abortControllerRef.current = null;
    }
  };

  return (
    <div id="chat-container">
      <div id="messages" ref={messagesRef}>
        {messages.map((msg, index) => (
          <ChatMessage 
            key={index} 
            message={msg.content} 
            isUser={msg.isUser} 
          />
        ))}
      </div>
      <ChatForm onSubmit={streamResponse} isLoading={isLoading} onCancel={abortStream} />
    </div>
  );
});

ChatContainer.displayName = 'ChatContainer';

export default ChatContainer;
