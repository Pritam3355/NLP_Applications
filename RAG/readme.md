# Financial News Analysis with LangChain

This notebook demonstrates how to use LangChain to analyze financial news and records to answer investment-related questions.

## Functionality

- Imports financial news and records datasets.
- Processes and prepares the data for analysis.
- Creates embeddings using HuggingFace Embeddings and stores them in a FAISS vector database.
- Implements an EnsembleRetriever for efficient information retrieval.
- Answers investment questions using a Together LLM and retrieved context.
- Augments queries to enhance context retrieval.
- Reranks retrieved context using a Cross-Encoder for improved relevance.


## Usage

**Ask Questions:** Modify the `query` variable in the relevant cells to ask your own investment questions.


## Requirements

- A Together API key (`together_api_key`).


