import ChatManager from './components/ChatManager';

export default function Home() {
  return (
    <div className="page">
      <header>
        <h1>D&D Agent</h1>
        <p>Ask a question about Dungeons & Dragons 5th Edition</p>
      </header>
      
      <ChatManager />
    </div>
  );
}
