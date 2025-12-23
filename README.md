# Adaptive Taxonomy Mapper

A Streamlit application that uses RAG (Retrieval-Augmented Generation) to map stories to an internal taxonomy system.

## Features

- **Story Analysis**: Analyzes story content and user-provided tags to determine appropriate genre and subgenre
- **RAG Integration**: Uses FAISS vector store and HuggingFace embeddings for semantic search
- **LLM Inference**: Leverages Groq's LLaMA model for intelligent categorization
- **Rule-based Fallback**: Provides fallback logic when LLM is unavailable
- **Interactive UI**: Clean Streamlit interface for easy story input and taxonomy mapping

## Supported Taxonomy

- **Romance**: Slow-burn, Enemies-to-Lovers, Second Chance
- **Thriller**: Espionage, Psychological, Legal Thriller  
- **Sci-Fi**: Hard Sci-Fi, Space Opera, Cyberpunk
- **Horror**: Psychological Horror, Gothic, Slasher

## Installation

1. Clone the repository:
```bash
git clone https://github.com/loki07-07/adaptive_taxanomy_mapper.git
cd adaptive_taxanomy_mapper
```

2. Create a virtual environment:
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the project root and add your Groq API key:
```
GROQ_API_KEY=your_groq_api_key_here
```

## Usage

Run the Streamlit application:
```bash
streamlit run app.py
```

Then open your browser and navigate to the displayed URL (typically `http://localhost:8501`).

## How it Works

1. **Input**: Enter user tags and story description
2. **Vector Search**: The system searches the taxonomy using semantic similarity
3. **LLM Processing**: Groq's LLaMA model analyzes the context and makes predictions
4. **Validation**: Results are validated against the predefined taxonomy
5. **Fallback**: If LLM fails, rule-based logic provides categorization

## Project Structure

```
├── app.py              # Streamlit web interface
├── mapping.py          # Core taxonomy mapping logic
├── requirements.txt    # Python dependencies
├── .gitignore         # Git ignore rules
└── README.md          # Project documentation
```

## Dependencies

- `streamlit` - Web interface
- `langchain` - LLM framework
- `langchain-groq` - Groq integration
- `faiss-cpu` - Vector database
- `sentence-transformers` - Text embeddings
- `python-dotenv` - Environment variable management

## Author

By Lokesh D
