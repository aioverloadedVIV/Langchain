
# LangChain React Agent using OpenAI GPT Model
# Loading Important Packages

import time
import langchainhub
import os
from dotenv import find_dotenv, load_dotenv
from langchain.agents import Tool, AgentExecutor, initialize_agent, create_react_agent
from langchain.tools import (
    DuckDuckGoSearchRun,
    DuckDuckGoSearchResults,
    WikipediaQueryRun,
)
from langchain_experimental.tools.python.tool import PythonREPLTool
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain import hub
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_openai import ChatOpenAI
print("\nRequired packages loaded")

# Load Environment
load_dotenv(find_dotenv(), override=True)
print("ENV file loaded")

# Set the API Key
api_key = os.environ.get("OPENAI_API_KEY")
if api_key:
    print("API key loaded successfully")
else:
    raise ValueError ("API key not found. Please check your .env file.")

# Set the model
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, api_key=api_key)  # type: ignore

# Prompt Template
template = """ 
Answer the following questions as best you can.
Questions: {q}
"""

prompt_template = PromptTemplate.from_template(template)

prompt = hub.pull("hwchase17/react")  # Load ReAct Prompt from LangChain hub
#print(type(prompt))
#print(prompt.input_variables)
#print(prompt.template)


# Defining Various Tools {tools} so that LLM can use it.

## 1. Python REPL Tool (for executing Python Code)
python_repl = PythonREPLTool()
python_repl_tool = Tool(
    name="python_repl",
    func=python_repl.run,
    description="Useful when you need to use Python to answer a question. You should input Python Code.",
)

## 2. Wikipedia Tool (for searching Wikipedia)
api_wrapper = WikipediaAPIWrapper(top_k_results=5, doc_content_chars_max=500)  # type: ignore
wikipedia = WikipediaQueryRun(api_wrapper=api_wrapper)
wikipedia_tool = Tool(
    name="wikipedia",
    func=wikipedia.run,
    description="Useful for when you need to look up a topic, country, or person on Wikipedia",
)

## 3. DuckDuckGo Search Tool (for general web searches)
search = DuckDuckGoSearchRun()
duckduckgo_tool = Tool(
    name="duckduckgo",
    func=search.run,
    description="Useful for when you need to perform an internet search to find information that another tool can't provide.",
)

tools = [python_repl_tool, wikipedia_tool, duckduckgo_tool]

# Loading the ReAct Agent and initializing the agent
agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,  # handles potential parsing errors for debugging purposes. Making agents more robust and less failures
    max_iterations=10,  # Stops getting stuck in loops.
)

print("\nReAct Agent initialized successfully")

print("\nReAct Agent Ready! Type your question/query or say 'bye' to exit.\n")

while True:
    question = input("Your Question: ").strip().lower()

    if question in ["exit", "quit", "bye"]:
        print("Exiting ReAct Agent... Goodbye!")
        time.sleep(1)
        break

    if not question:
        print("Please enter a valid query.")
        continue

    try:
        formatted_prompt = prompt_template.format(q=question)
        output = agent_executor.invoke({'input': formatted_prompt})
        print(f"\nAgent: {output['output']}\n")
    except Exception as e:
        print(f"Error during response generation: {e}\n")
