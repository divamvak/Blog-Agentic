# Blog-Agentic: End-to-End Blog Generation with Translation

This project is an agentic AI application built with **LangGraph** and **FastAPI** to generate blog posts on any topic and optionally translate them into different languages (e.g., Greek). It leverages **Groq** for fast LLM inference and **LangSmith** for observability and debugging.

## Features
- Generate blog posts based on a given topic.
- Translate blog content into multiple languages (e.g., Greek, English).
- Built with a modular LangGraph architecture for agentic workflows.
- Exposes a REST API via FastAPI for easy interaction.
- Integrated with LangSmith for tracing and debugging.

## Prerequisites
- Python 3.10 or higher
- A Groq API key (sign up at [console.groq.com](https://console.groq.com))
- A LangChain API key for LangSmith (optional, for tracing)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/divamvak/Blog-Agentic.git
   cd Blog-Agentic
