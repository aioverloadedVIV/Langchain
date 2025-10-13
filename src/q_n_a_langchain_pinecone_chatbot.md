# Q&A Chatbot with RAG (Retrieval-Augmented Generation)

A production-ready conversational AI chatbot that answers questions based on your custom documents using OpenAI's GPT models and vector similarity search.

## Overview

This chatbot implements RAG architecture to provide accurate, context-aware answers from uploaded documents (PDF, DOCX, CSV). It combines semantic search with large language models to deliver intelligent responses grounded in your specific knowledge base.

## Key Features

- **Multi-format Support**: Processes PDF, DOCX, and CSV files
- **Intelligent Chunking**: Splits documents into optimized segments for retrieval
- **Vector Search**: Uses Pinecone for fast, semantic similarity matching
- **Conversational Interface**: Interactive CLI for natural Q&A sessions
- **Persistent Storage**: Embeddings stored in Pinecone for reuse across sessions

## Tech Stack

- **LLM**: OpenAI GPT-4o
- **Embeddings**: OpenAI text-embedding-3-small (1536 dimensions)
- **Vector Database**: Pinecone (Serverless, AWS us-east-1)
- **Framework**: LangChain
- **Language**: Python 3.x

## Architecture

1. **Document Processing**: Loads and chunks documents into 256-character segments
2. **Embedding Generation**: Converts text chunks into vector embeddings
3. **Vector Storage**: Stores embeddings in Pinecone with cosine similarity indexing
4. **Retrieval**: Fetches top-5 most relevant chunks for each query
5. **Response Generation**: GPT-4o synthesizes answers from retrieved context

## Usage

1. Enter an index name (creates new or uses existing)
2. Provide document file path
3. Ask questions - the bot retrieves relevant context and generates answers
4. Type `quit`, `exit`, or `bye` to end session

## Use Cases

- Internal knowledge base Q&A
- Customer support automation
- Document analysis and research
- Training material assistant

## Future Enhancements

- Web interface (Streamlit/Gradio)
- Conversation memory for multi-turn dialogues
- Support for additional file formats
- Query refinement and follow-up questions

---

**Note**: Requires active OpenAI and Pinecone API subscriptions.
