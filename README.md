🔎 LangChain Search Agent

A Streamlit chat app where an AI research assistant answers your questions by searching the web, Wikipedia, and arXiv. It is built with LangChain's agent framework (on top of LangGraph) and runs on a Groq-hosted LLM.

Features
Chat interface built with Streamlit, with conversation history kept for the session
Three search tools the agent picks from automatically:
web_search: general and current information via DuckDuckGo
wikipedia_search: background summaries from Wikipedia
arxiv_search: academic papers from arXiv
Tool-calling agent that can run multiple search steps before answering
Bring your own key: enter your Groq API key in the sidebar, nothing is hard-coded
How It Works
You type a question in the chat box.
The agent (created with create_agent) sends the conversation and tool definitions to the Groq model.
The model either calls one or more tools or writes a final answer.
Tool results are fed back to the model, which summarizes them for you.
Tech Stack
Component	Library
UI	Streamlit
Agent framework	LangChain + LangGraph
LLM provider	Groq (langchain-groq) with openai/gpt-oss-120b
Web search	ddgs (DuckDuckGo)
Encyclopedia	wikipedia
Papers	arxiv
Getting Started
Prerequisites
Python 3.10+
A Groq API key from console.groq.com
Installation
bash
# Clone or download the project, then:
cd SearchEngine

# Create and activate a virtual environment (Windows)
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install streamlit python-dotenv langchain langchain-groq langgraph ddgs wikipedia arxiv

On macOS/Linux, activate with source .venv/bin/activate instead.

Run
bash
streamlit run app.py

Open the URL Streamlit prints (usually http://localhost:8501), paste your Groq API key into the sidebar, and start asking questions.

Optional: .env file

The app calls load_dotenv(), so you can keep other environment variables in a .env file. The Groq key itself is entered through the sidebar.
