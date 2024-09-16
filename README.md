# Streamlit Cohere PDF QA Bot

This project is a **Streamlit application** that allows users to upload a PDF document, extract text from it, and ask questions about the content. The app utilizes **Cohere's language model** to generate embeddings for document chunks and store them in a **FAISS** index for efficient retrieval. Users can then query the document, and the most relevant parts are fetched to answer their questions.

## Features

- Upload PDF files to extract and process text
- Chunk large documents into smaller parts for efficient processing
- Generate document embeddings using **Cohere API**
- Store embeddings in a **FAISS** index for similarity search
- Ask questions about the document and receive answers based on relevant document chunks

## Tech Stack

- **Streamlit**: For the front-end and interaction
- **Cohere**: Used for generating embeddings for document and query
- **FAISS**: For efficient similarity search of document embeddings
- **LangChain**: Manages the chain of embedding, query processing, and QA
- **PyPDF2**: For PDF reading and extraction
- **Docker**: Containerized deployment of the application

## Setup Instructions

### Prerequisites

Make sure you have the following installed:

- Python 3.9 or higher
- Docker (optional for containerization)

### Steps to Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/streamlit-cohere-pdf-bot.git
   cd streamlit-cohere-pdf-bot
