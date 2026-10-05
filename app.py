import streamlit as st
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain.agents import create_agent

from ddgs import DDGS
import wikipedia
import arxiv


# --------------------------------------------------
# Configuration
# --------------------------------------------------

load_dotenv()

st.set_page_config(
    page_title="LangChain Search Agent",
    page_icon="🔎",
)

st.title("🔎 LangChain Search Agent")


# --------------------------------------------------
# Groq API Key
# --------------------------------------------------

api_key = st.sidebar.text_input(
    "Enter your Groq API Key:",
    type="password",
)

if not api_key:
    st.info("Enter your Groq API key in the sidebar to start.")
    st.stop()


# --------------------------------------------------
# Tools
# --------------------------------------------------

@tool
def web_search(query: str) -> str:
    """Search the web using DuckDuckGo."""

    results = DDGS().text(
        query,
        max_results=5
    )

    if not results:
        return "No web results found."

    output = []

    for result in results:
        title = result.get("title", "")
        body = result.get("body", "")
        url = result.get("href", "")

        output.append(
            f"Title: {title}\n"
            f"Description: {body}\n"
            f"URL: {url}"
        )

    return "\n\n".join(output)


@tool
def wikipedia_search(query: str) -> str:
    """Search Wikipedia and return a short summary."""

    try:
        search_results = wikipedia.search(query)

        if not search_results:
            return "No Wikipedia results found."

        page = wikipedia.page(
            search_results[0],
            auto_suggest=False
        )

        return (
            f"Title: {page.title}\n\n"
            f"Summary:\n{page.summary[:3000]}"
        )

    except Exception as e:
        return f"Wikipedia search failed: {e}"


@tool
def arxiv_search(query: str) -> str:
    """Search arXiv for academic papers."""

    client = arxiv.Client()

    search = arxiv.Search(
        query=query,
        max_results=3,
        sort_by=arxiv.SortCriterion.Relevance,
    )

    results = []

    for paper in client.results(search):
        results.append(
            f"Title: {paper.title}\n"
            f"Authors: {', '.join(str(a) for a in paper.authors)}\n"
            f"Published: {paper.published}\n"
            f"Summary: {paper.summary[:1500]}\n"
            f"URL: {paper.entry_id}"
        )

    if not results:
        return "No arXiv papers found."

    return "\n\n".join(results)


tools = [
    web_search,
    wikipedia_search,
    arxiv_search,
]


# --------------------------------------------------
# LLM
# --------------------------------------------------

llm = ChatGroq(
    api_key=api_key,
    model="openai/gpt-oss-120b",
    temperature=0,
    reasoning_effort="low",
)


# --------------------------------------------------
# Agent
# --------------------------------------------------

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=(
        "You are a helpful research assistant. "
        "Use web_search for general or current information. "
        "Use wikipedia_search when Wikipedia information "
        "is useful. "
        "Use arxiv_search when the user asks about "
        "research papers or academic topics."
    ),
)


# --------------------------------------------------
# Chat history
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hi! I'm a research assistant. "
                "I can search the web, Wikipedia, "
                "and arXiv. How can I help you?"
            ),
        }
    ]


# --------------------------------------------------
# Display previous messages
# --------------------------------------------------

for message in st.session_state.messages:
    st.chat_message(
        message["role"]
    ).write(
        message["content"]
    )


# --------------------------------------------------
# User input
# --------------------------------------------------

if prompt := st.chat_input(
    "What would you like to search?"
):

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):

        with st.spinner("Researching..."):

            result = agent.invoke(
                {
                    "messages": st.session_state.messages
                }
            )

            response = result["messages"][-1].content

        st.write(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )