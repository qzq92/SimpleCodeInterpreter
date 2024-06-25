# SimpleCodeInterpreter

Simple Code interpreter built using LLM model, Agents with ReAct paradigm to decide on which defined tools is to be used based on input prompts set via the *ROUTER_AGENT_PROMPT*-prefixed environment variables in *.env* file.
- QR code generation based on prompts containing url fed into Agents and LLM model
- CSV analyzer based on sample *episode_info.csv* csv file representing "Seinfield" TV series, using langchain experimental agent involving *create_csv_agent*.

Note that the use of Agents do not necessary guarantee result accuracy as they are flaky in nature.
Generated QR codes samples

Channelnewsasia:

![Channelnewsasia](qrcodes/www_channelnewsasia_com.png)

Straits Times Singapore:
![Straits Times Singapore](qrcodes/www_straitstimes_com.png)

**Security Reminder: Please note that these generated codes are generated via the use of LLM prompts as part of exploration work. Care must be taken in validating the link when using any scanning device to scan the QR codes before accessing the links to reduce the risk of your device being compromised**

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

Without setting such parameter, an exception would be raised as follows: 

```ValueError: This agent relies on access to a python repl tool which can execute arbitrary code. This can be dangerous and requires a specially sandboxed environment to be safely used. Please read the security notice in the doc-string of this function. You must opt-in to use this functionality by setting allow_dangerous_code=True.For general security guidelines, please see: https://python.langchain.com/v0.2/docs/security/**
```

## Environment file to edit

Please create an *.env* file with the following parameters.

```
OPENAI_API_KEY = <YOUR API KEY>
HUB_TEMPLATE = "langchain-ai/react-agent-template"
OPENAI_MODEL = "gpt-4-turbo" # Or any other OPENAI offered models
CSV_FILEPATH = "data/episode_info.csv"

# QR Code urls of interest for prompt template (only if you are running *agent.py* script directly in *agents* directory)
QR_CODE_URL_1 = "https://www.straitstimes.com"
QR_CODE_URL_2 = "https://www.channelnewsasia.com"

# Router prompts used by main.py script
ROUTER_AGENT_PROMPT_1 = <YOUR 1st Example prompt for Router Agent>
ROUTER_AGENT_PROMPT_2 = <YOUR 2nd Example prompt for Router Agent>

# Optional if you are not using LangSmith for tracking llm utilisation related metrics
LANGCHAIN_API_KEY=<YOUR API KEY>
LANGCHAIN_TRACING_V2=true
```

For more information on Langsmith, refer to [here](https://www.langchain.com/langsmith).

### **Customising to other csv files**

You may include other csv file of interest in the *data/* subfolder of this repository. However, changes to prompt maybe needed as the schema and content of your csv file would likely be different from the example episode_info.csv provided.

## Installation and Execution

1. Please use Anaconda distribution to install the necessary libraries with the following command

```
conda env create -f environment.yml
```

2. Run the main.py or agents/agent.py file with either of the following commands directly from the repo main directory.

```
python main.py;

python agents/agent.py
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
    - Tools
    - ReAct template: "langchain-ai/react-agent-template"

## Acknowledgement and Credits

The codebase developed are in reference to *Section 7: Building a slim ChatGPT Code-Interpreter(Advanced Agents, OpenAI Functions)* of Udemy course titled "LangChain- Develop LLM powered applications with LangChain" available via https://www.udemy.com/course/langchain.
