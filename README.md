# 🐉 D&D RAG Assistant

An intelligent chat application that answers questions about Dungeons & Dragons 5th Edition. Uses AI and vector search to provide accurate, contextual responses.

![Docker](https://img.shields.io/badge/Docker-Ready-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-Framework-green) ![Next.js](https://img.shields.io/badge/Next.js-Frontend-lightgrey)

---

## ✨ Features

- **Smart Q&A**: Get accurate answers about D&D 5e rules, spells, and mechanics.
- **Real-time Chat**: Streaming responses with persistent chat history.
- **User Authentication**: Secure login with Keycloak.
- **Web Search**: Automatically finds additional D&D content.

---

## 🚀 Quick Start

### Prerequisites

Ensure you have the following installed:
- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/)
- [Ollama](https://ollama.ai/)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd DnD-RAG
```

### 2. Set Up AI Model

Install and configure the AI model:

```bash
ollama serve
ollama pull qwen3:1.7b
```

### 3. Start the Application

Use Docker Compose to build and start all services:

```bash
docker-compose up -d
```

### 4. Access the Application

- **Frontend**: [http://localhost:3000](http://localhost:3000)
- **Backend API**: [http://localhost:8000](http://localhost:8000)
- **Keycloak Admin**: [http://localhost:8080](http://localhost:8080) (default credentials: `admin/admin`)

---

## 🛠️ Technology Stack

- **Frontend**: [Next.js](https://nextjs.org/) 15 + React 19
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) + Pydantic AI
- **Database**: MongoDB + Qdrant (vector search)
- **Authentication**: [Keycloak](https://www.keycloak.org/)
- **AI Model**: Qwen 3:1.7B
- **Deployment**: Docker + Docker Compose

---

## 🐳 Deployment

### Build and Start Services

```bash
docker-compose up -d
```

### View Logs

```bash
docker-compose logs -f
```

### Stop Services

```bash
docker-compose down
```