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
from agents.agent import get_python_agent_executor, get_csv_agent_executor
import os

load_dotenv()

def main():

    csv_agent_executor = get_csv_agent_executor()


    def python_agent_executor_wrapper(original_prompt: str) -> dict[str, Any]:
        """Wrapper function take takes in a string prompt and calls an AgentExecutor's invoke method with arbitrary dictionary containing the input string passed to 'input' key. 

        Args:
            original_prompt (str): Prompt in string type.

        Returns:
            dict[str, Any]: Agent Executor response.
        """
        python_agent_executor = get_python_agent_executor()

        return python_agent_executor.invoke({"input": original_prompt})
    
    router_agent_tools_list = [
        Tool(
            name = "Python Agent",
            func = python_agent_executor_wrapper,
            description = """Useful when you need to transform natural language to Python, execute the Python code and return the results from code execution. DOES NOT ACCPEPT CODE AS INPUT""",
        ),
        Tool(
            name = "CSV Agent",
            func = csv_agent_executor.invoke,
            description = """Useful when you need to answer question over a .csv file, takes an input the entire question and returns the answer after running Python's pandas calculations""",
        ),
    ]

    base_prompt = hub.pull(os.environ.get("HUB_TEMPLATE"))
    # No instruction is to be fed to router agent
    prompt = base_prompt.partial(instructions="")

    # Instantiate react agent
    router_agent = create_react_agent(
        prompt = prompt,
        llm = ChatOpenAI(temperature=0,
                model=os.environ.get("OPENAI_MODEL")
            ),
        tools = router_agent_tools_list,
    )

    router_agent_executor = AgentExecutor(
        agent=router_agent,
        tools=router_agent_tools_list,
        verbose=True
    )

    # Test prompt #1
    prompt_1 = "Which season has the most episodes?"
    print(router_agent_executor.invoke({"input": prompt_1}))

    prompt_2 = "Generate and save in current working directory, under a folder 'qrcodes' the following:\n\n 1 QR code pointing to provided url: https://www.techtarget.com/ and save as techtarget.png "
    
    print(router_agent_executor.invoke({"input": prompt_2}))

# Main function
if __name__ == "__main__":
    main()