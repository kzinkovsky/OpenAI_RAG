# AI Assistant for Answering Questions about Texts Using OpenAI with Retrieval-Augmented Generation (RAG)

This AI assistant allows you to:
* Upload a text (in PDF format) that you're interested in.
* Get AI-generated answers to your questions based on the relevant context from the uploaded text.
* Customize the default parameters for the RAG and OpenAI models if desired.

The AI assistant utilizes OpenAI models and a simple RAG system based on FAISS. The code is provided as Python scripts, as well as a Jupyter notebook for experimentation. In both cases, a minimal user interface is implemented.

The AI assistant runs on your local machine and interacts with OpenAI via API. To obtain a personal API key, you need an OpenAI account. After signing up, you can generate your key at this link: https://platform.openai.com/account/api-keys

## Installation and Launch

Clone this repository
```bash
git clone [repository-link] [target-directory]
```

Install the required packages
Ensure Python is installed and activate the appropriate virtual environment (if applicable) before running the command. Otherwise, dependencies might be installed in the global environment instead of the local one.
```bash
pip install -r requirements.txt
```

Create a .env file in the project root directory with the following variable:
```bash
OPENAI_API_KEY=your_openai_api_key
```

To run the AI assistant
```bash
python main.py
```

