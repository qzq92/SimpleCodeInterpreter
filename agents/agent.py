from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.agents import create_react_agent, AgentExecutor
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_experimental.tools import PythonREPLTool
from langchain.tools import Tool
from textwrap import dedent
from langchain import hub
from typing import Any
import os

def get_csv_agent_executor() -> AgentExecutor:
    """Function which returns a CSV AgentExecutor based on ChatOpenAI llm
    and defined relative csv filepath.

    Returns:
        AgentExecutor: LangChain CSV Agent Executor.
    """
    # CSV agent declaration and instantiation. Due to it being an experimental stuff
    csv_agent_executor = create_csv_agent(
        llm = ChatOpenAI(temperature=0,
                model=os.environ.get("OPENAI_MODEL")
            ),
        path=os.environ.get("CSV_FILEPATH"),
        verbose=True,
        allow_dangerous_code=True,
        
    )
    return csv_agent_executor

def get_python_agent_executor() -> AgentExecutor:
    
    
    print("Creating a ReAct based Python agent experimentations")
    prompt_instructions = dedent("""\
        You are an agent designed to always write and execute python code to answer questions. Answer should be based on python code output. You have access to python REPL for executing python code. Should you get an error, perform code debugging and try again. If you are unable to write code to answer the question, return "I do not know" as the answer."""
        )

    # Get hub template and set partial variables using fixed prompt
    base_prompt = hub.pull(os.environ.get("HUB_TEMPLATE"))
    react_prompt = base_prompt.partial(instructions=prompt_instructions)

    # Define tool list, containing tools to use, should be Tool object with docstring. Custom function can be converted to a tool with @tool decorator.
    tools_lists = [PythonREPLTool()]

    # Create agent as recipe with react prompt to reason and act based on outputs obtained from tools used.
    python_agent = create_react_agent(
        llm = ChatOpenAI(temperature=0,
                model=os.environ.get("OPENAI_MODEL")
            ),
        tools=tools_lists,
        prompt=react_prompt
    )

    # Orchestrator for agent with verbose enabled to track its inner workings
    python_agent_executor = AgentExecutor(
        agent=python_agent,
        tools=tools_lists,
        verbose=True
    )

    return python_agent_executor


if __name__ == "__main__":
    load_dotenv()

    # Pythonic Agent
    python_input_prompt = dedent(
        """\
            Generate and save in current working directory, under a folder 'qrcodes' the following:\n\n
            1 QR codes pointing to provided url: {qr_code_url_1} with the filename labelled as the website name of {qr_code_url_1} with any . replace by _ in png format.; and 1 QR code pointing to the provided url: {qr_code_url_2} with the filename labelled as the website name of {qr_code_url_2}  with any . replace by _ in png format. You have 'qrcode' package installed and available for use. DO NOT GENERATE IF THE PROVIDED URL IS INVALID.""")
    
    python_input_prompt_template = PromptTemplate.from_template(template=python_input_prompt)
    python_input_prompt_val = python_input_prompt_template.format_prompt(
        qr_code_url_1 = os.environ.get("QR_CODE_URL_1"),
        qr_code_url_2 = os.environ.get("QR_CODE_URL_2")
    )
    
    python_agent_executor = get_python_agent_executor()
    python_agent_executor.invoke(
        input = {"input": python_input_prompt_val}
    )

    print("--------------------------CSV Agent Executor------------------")

    # Define template for csv agent executor
    csv_input_template = "How many columns are there in provided csv file, {csv_file}"
    csv_prompt_template_input = PromptTemplate.from_template(template=csv_input_template)

    csv_prompt_template_val = csv_prompt_template_input.format_prompt(
        csv_file = os.environ.get("CSV_FILEPATH")
    )

    csv_agent_executor = get_csv_agent_executor()

    # CSV Executor invocation
    csv_agent_executor.invoke(
        input = {"input": csv_prompt_template_val}
    )