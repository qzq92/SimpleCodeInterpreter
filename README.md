# SimpleCodeInterpreter
Simple Code Interpreter

## Warning
This should not be placed in PRODUCTION environment as the use of PythonREPL library facilitates remote code execution.

## Installation and Execution

1. Please use Anaconda distribution to install the necessary libraries with the following command

```
conda env create -f environment.yml
```

## Programming languages/tools involved

- Python
- Langchain
    - ChatOpenAI
    - Experimental tools: PythonREPLTool
    - Agents: create_react_agent, AgentExecutor

## Acknowledgement and Credits

The codebase developed are in reference to *Section 6: Building a documentation assistant(Embeddings, VectorDBs, Retrieval, Memory)* of Udemy course titled "LangChain- Develop LLM powered applications with LangChain" available via https://www.udemy.com/course/langchain.

- Wget setup for Windows: Download and install wget : https://phoenixnap.com/kb/wget-command-with-examples
- *download_docs.py*: Originated from Udemy course author, with some code amendment to process from .env file