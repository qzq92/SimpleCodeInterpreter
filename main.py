from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_experimental.tools import PythonREPLTool
from textwrap import dedent
from langchain import hub
import os

load_dotenv()

def main():
    print("Start...")

    prompt_instructions = dedent("""\
        You are an agent designed to always write and execute python code to answer questions. Answer should be based on python code output. You have access to python REPL for executing python code. Should you get an error, perform code debugging and try again. If you are unable to write code to answer the question, return "I do not know" as the answer."""
        )

    base_prompt = hub.pull(os.environ.get("HUB_TEMPLATE"))
    react_prompt = base_prompt.partial(instructions=prompt_instructions)
    
    llm = ChatOpenAI(temperature=0, model=os.environ.get("OPENAI_MODEL"))

    # Define tool list, containing tools to use, should be Tool object with docstring. Custom function can be converted to a tool with @tool decorator.
    tools_lists = [PythonREPLTool()]

    # Create agent as recipe with react prompt to reason and act based on outputs obtained from tools used.
    qr_agent = create_react_agent(
        llm=llm,
        tools=tools_lists,
        prompt=react_prompt
    )

    # Orchestrator for agent with verbose enabled to track its inner workings
    qr_agent_executor = AgentExecutor(
        agent=qr_agent,
        tools=tools_lists,
        verbose=True
    )

    input_prompt = dedent(
        """\
            Generate and save in current working directory, under a folder 'qrcodes' the following:\
                  1 QR codes pointing to https://www.channelnewsasia.com with the filename labelled as 'cna.png'; and 1 QR code pointing to https://www.straitstimes.com/ with the filename labelled as 'straitstimes.png'. You have 'qrcode' package installed and available for use.
        """)
    
    # Invoke agent for generating QR code
    qr_agent_executor.invoke({input:input_prompt})


    # CSV agent declaration and instantiation. Due to it being an experimental stuff
    # csv_agent = create_csv_agent(
    #     llm=llm,
    #     path=os.environ.get("CSV_FILEPATH"),
    #     verbose=True
    # )

if __name__ == "__main__":
    main()