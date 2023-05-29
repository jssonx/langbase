# langbase

LangBase is a highly interactive AI language model interface that incorporates advanced technologies including Python, LangChain, Supabase, Docker, and Streamlit. This interface is not only interactive, but also user-friendly with adjustable settings for facilitating a conversation with GPT based on a user's knowledge base.

LangBase can be deployed via Docker, allowing users to modify prompts. It supports the bulk upload of PDF files, enables the memory function for model dialogue, and allows the selection of Supabase or Chroma for vector data storage. It also features a real-time display of token usage.

## Installation
Ensure that you have Docker installed on your machine before you proceed.

1. Build the Docker Image:
Use the following command to build the Docker image.
```bash
docker build -t langbase .
```
2. Run the Docker Container Interactively:
Use the following command to run the Docker container interactively. This mounts your current directory (the host) to /app (the container).
```bash
docker run -it -v $(pwd):/app -p 8501:8501 langbase bash
```
3. Run the Application Locally:
If you want to run the application locally, you can do it with Streamlit.
```bash
streamlit run ./src/main.py
```

## Usage
Once you've launched LangBase, you can customize it according to your needs. Upload PDF files in bulk, modify dialogue prompts, and choose between Supabase and Chroma for your vector data storage. Keep track of your token usage with the real-time display feature.