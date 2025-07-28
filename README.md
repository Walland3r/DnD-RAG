# 🐉 D&D RAG Assistant

An intelligent chat application that answers questions about Dungeons & Dragons 5th Edition. Uses AI and vector search to provide accurate, contextual responses.

## ✨ Features

- **Smart Q&A**: Get accurate answers about D&D 5e rules, spells, and mechanics
- **Real-time Chat**: Streaming responses with persistent chat history
- **User Authentication**: Secure login with Keycloak
- **Web Search**: Automatically finds additional D&D content

##  Quick Start

### Prerequisites
- Docker and Docker Compose

### 1. Clone and Setup
```bash
git clone <repository-url>
cd DnD-RAG
```

### 2. Start with Docker
```bash
docker-compose up -d
```

### 3. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Keycloak Admin**: http://localhost:8080 (admin/admin)

That's it! The application will be running with all dependencies.

## �️ Technology Stack

- **Frontend**: Next.js 15 + React 19
- **Backend**: FastAPI + Pydantic AI
- **Database**: MongoDB + Qdrant (vector search)
- **Authentication**: Keycloak
- **AI Model**: Qwen 3:1.7B
- **Deployment**: Docker + Docker Compose


## 🐳 Deployment

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```