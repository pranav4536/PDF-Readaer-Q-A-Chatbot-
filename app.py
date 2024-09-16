import streamlit as st
import os
import cohere
import faiss
import numpy as np
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings.base import Embeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import Cohere
from dotenv import load_dotenv

# Step 1: Load environment variables (for Cohere API key)
load_dotenv()

# Step 2: Initialize Cohere client
co = cohere.Client(os.getenv("COHERE_API_KEY"))  # Replace with your environment variable or key

# Streamlit UI
st.title("Document QA with Cohere and FAISS")
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file is not None:
    # Step 3: Save the uploaded file temporarily
    with open("temp_pdf.pdf", "wb") as f:
        f.write(uploaded_file.read())
    
    # Step 4: PDF Reader function to load and process the PDF
    def read_pdf(file_path):
        file_loader = PyPDFLoader(file_path)
        documents = file_loader.load()
        return documents
    
    # Load the saved PDF file
    doc = read_pdf("temp_pdf.pdf")
    st.write(f"Total Pages in the document: {len(doc)}")
    
    # Step 5: Chunk the document using a Recursive Text Splitter
    def chunk_data(docs, chunk_size=800, chunk_overlap=50):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        docs_chunked = text_splitter.split_documents(docs)
        return docs_chunked

    # Chunk the PDF document into smaller parts
    documents = chunk_data(docs=doc)
    st.write(f"Total Chunks Created: {len(documents)}")
    
    # Step 6: Cohere Embedding Function
    class CohereEmbeddings(Embeddings):
        def embed_documents(self, texts: list[str]) -> list[list[float]]:
            response = co.embed(texts=texts)
            return response.embeddings
        
        def embed_query(self, text: str) -> list[float]:
            response = co.embed(texts=[text])
            return response.embeddings[0]
    
    # Step 7: Store embeddings in FAISS
    def store_faiss_embeddings(embeddings, documents):
        dimension = len(embeddings[0])
        index = faiss.IndexFlatL2(dimension)  # Create FAISS index with L2 distance
        index.add(np.array(embeddings))  # Add embeddings to FAISS index
        return index

    # Generate Cohere embeddings for the document chunks
    texts = [doc.page_content for doc in documents]
    cohere_embedder = CohereEmbeddings()
    embeddings = cohere_embedder.embed_documents(texts)

    # Store embeddings in FAISS
    faiss_index = store_faiss_embeddings(embeddings, documents)

    # Optionally, save the FAISS index to disk
    faiss.write_index(faiss_index, "faiss_index.idx")
    st.write("FAISS Index has been created and saved.")
    
    # Step 8: Search FAISS for relevant documents based on query
    def search_faiss_index(query):
        # Embed the query using Cohere
        query_embedding = cohere_embedder.embed_query(query)
        query_vector = np.array([query_embedding])  # Reshape for FAISS
        # Search the FAISS index for the top 5 similar chunks
        D, I = faiss_index.search(query_vector, k=5)
        return I  # Return indices of matching documents

    # Accept a query input from the user
    query = st.text_input("Enter your query:")
    
    if query:
        result_indices = search_faiss_index(query)
        st.write(f"Matching Chunk Indices: {result_indices}")
        
        # Step 9: Run Question Answering Chain on matched documents
        llm = Cohere(cohere_api_key=os.getenv("COHERE_API_KEY"))  # Initialize Cohere LLM
        qa_chain = load_qa_chain(llm, chain_type="stuff")

        # Get the matching documents based on FAISS search results
        matching_documents = [documents[i] for i in result_indices[0]]

        # Run QA chain
        answer = qa_chain.run(input_documents=matching_documents, question=query)
        st.write(f"Answer: {answer}")

