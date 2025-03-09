# DnD-RAG

DnD-RAG is a Dungeons & Dragons rules and information retrieval system. It uses a combination of FastAPI, LangChain, and various other libraries to provide answers to user queries based on the context of Dungeons & Dragons rules.

## Features

- Load and process PDF documents containing Dungeons & Dragons rules.
- Generate embeddings for the text chunks from the PDFs.
- Store and retrieve embeddings using Chroma.
- Query the stored embeddings to find relevant information.
- Provide answers to user questions using a language model.

## Setup

### Requirements

- Python 3.8+
- CUDA-compatible GPU (optional, for faster processing)

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/dnd_rag.git
    cd dnd_rag
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Ensure you have the necessary PDF files in the `handbook_by_chapter` directory.

### Running the Application

1. Start the FastAPI server:
    ```sh
    uvicorn main:app --reload
    ```

2. Open your browser and navigate to `http://localhost:8000` to access the web interface.

## Usage

### Updating the Database

To update the database with new PDF content, click the "Reload Database" button on the web interface. This will read the PDFs, generate embeddings, and store them in the vector store.

### Querying

Enter your question in the input field and click "Send". The system will search for relevant information in the stored embeddings and provide an answer based on the context.

## File Structure

- `generate_embeddings.py`: Functions to generate and store embeddings.
- `embedding_function.py`: Defines the embedding function using HuggingFace models.
- `llm_query.py`: Handles querying the language model.
- `main.py`: FastAPI application setup and endpoints.
- `read_pdf.py`: Functions to read and split PDF documents.
- `static/`: Contains static files for the web interface.
- `requirements.txt`: List of required Python packages.
