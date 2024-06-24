# SimpleCodeInterpreter
Simple Code Interpreter

## Warning and Risks
This should not be placed in PRODUCTION environment as the use of PythonREPL library facilitates remote code execution. This is due to the use of following code shown in code snippet, where *allow_dangerous_code* is set to True.

```
    csv_agent = create_csv_agent(
        llm=llm,
        path=os.environ.get("CSV_FILEPATH"),
        verbose=True,
        allow_dangerous_code=True
    )
```

Without setting such parameter, , an exception would be raised with the following: 

```ValueError: This agent relies on access to a python repl tool which can execute arbitrary code. This can be dangerous and requires a specially sandboxed environment to be safely used. Please read the security notice in the doc-string of this function. You must opt-in to use this functionality by setting allow_dangerous_code=True.For general security guidelines, please see: https://python.langchain.com/v0.2/docs/security/**
```



## Installation and Execution

1. Please use Anaconda distribution to install the necessary libraries with the following command

```
conda env create -f environment.yml
```


## Errors encountered due to incompatibility of Python version with

1. The use of Python==3.12.4 library results in the error "TypeError: ForwardRef._evaluate() missing 1 required keyword-only argument: 'recursive_guard'" appearing when executing main.py. Please downgrade to 3.12.3 instead as a workaround
- Reference : https://github.com/pydantic/pydantic/issues/9637

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