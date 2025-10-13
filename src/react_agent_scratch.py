
# REACT AGENT FROM SCRATCH USING OPENAI 
import time
print("Welcome to ReAct Agent Bot using OpenAI API models\n")
time.sleep(2)

## Loading the ENV File

import os
from dotenv import load_dotenv, find_dotenv

env = load_dotenv(find_dotenv(), override=True)

if env:
    print(".env file found")
else:
    raise FileNotFoundError(".env file not found please check your directory!")

## Importing the necessary Libraries

import openai
import re
import httpx
import os

print("Libraries Loaded!")

## Using the most cost effective yet high performance model from OpenAI - GPT-4o-mini

from openai import APIError, OpenAI, api_key

client = OpenAI(api_key=api_key)
if client:
    print("API Key Configured Successfully")
else:
    raise KeyError("API key not configured!")


## Define the Agent Class
class Agent:
    def __init__(self, system=""): # It initializes System attribute which is empty by default and messages list
        self.system = system
        self.messages = [] # To store messages

        if self.system:  # if developer defines system message
            self.messages.append({"role": "system", "content": system})

    def __call__(self, prompt): # Decides what the Agent will gonna do
        self.messages.append({"role": "user", "content": prompt})
        result = self.execute() 
        self.messages.append({"role": "assistant", "content": result})
        return result # returing the assistance response

    def execute(self, model="gpt-4o-mini", temperature=0):
        completion = client.chat.completions.create(
            model=model,
            temperature=temperature,
            messages=self.messages
        )
        return completion.choices[0].message.content

## Writing a System prompt
prompt = """
You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop you output an Answer
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.

Your available actions are:

calculate:
e.g. calculate: 4 * 7 / 3
Runs a calculation and returns the number - uses Python so be sure to use floating point syntax if neccessary

get_cost:
e.g. get_cost: book
returns the cost of a book

wikipedia:
e.g. wikipedia: LangChain
Returns a summary from searching Wikipedia

Always look things up on Wikipedia if you have the opportunity to do so.

Example session #1:

Question: How much does a pen cost?
Thought: I should look the pen cost using get_cost
Action: get_cost: pen
PAUSE

You will be called again with this:

Observation: A pen costs $5 

You then output:

Answer: A pen costs $5

Example session #2

Question: What is the capital of France?
Thought: I should look up France on Wikipedia
Action: wikipedia: France
PAUSE

You will be called again with this:

Observation: France is a country. The capital is Paris.

You then output:

Answer: The capital of France is Paris
""".strip()

## Creating the Tools - Provided in the last prompt (calculate, get_cost, wikipedia)

### calculate function
def calculate(what):
    """The calculate() function takes in a string, evaluates that string, and returns the result"""
    return eval(what)


### get_cost function
def get_cost(thing):
    """The get_cost() function returns the cost for a pen, a book, and a stapler."""
    if thing in "pen":
        return "A pen cost $5"
    elif thing in "book":
        return "A book costs $20"
    elif thing in "stapler":
        return "A stapler costs $10"
    else:
        return "A random thing for writing costs $12."

### wikipedia function
def wikipedia(q):
    response = httpx.get("https://en.wikipedia.org/w/api.php", params={
        'action': 'query',
        'list':'search',
        'srsearch': q,
        'format': 'json'
    })
    results = response.json().get('query').get('search', [])

    if not results:
        return None
    return results[0]['snippet']

## defining a regex for finding the action string
action_re = re.compile(r'^Action: (\w+): (.*)$') # python regular expression to select Action:

## ReACT Agent Chatbot
def query(question, max_turns=5):
    """query: takes a question and runs the process for 5 cycles."""
    i = 0
    bot = Agent(prompt)
    next_prompt = question 

    while i < max_turns:
        i += 1
        result = bot(next_prompt)
        print(result)

        # we'll extract the action string using regex
        actions = [action_re.match(a) for a in result.split('\n') if action_re.match(a)]

        if actions:
            action, action_input = actions[0].groups()

            if action not in known_actions:
                raise Exception(f"Unknown actions: {action}: {action_input}")

            print(f" --running {action} for {action_input}")
            observation = known_actions[action](action_input)

            print(f"Observation: {observation}")
            next_prompt = f"Observation: {observation}"

        else:
            return  


while True:
    user_question = input("Type Your query or quit to exit: ")
    if user_question.lower().strip() not in ['exit', 'bye', 'quit']:
        query(question=user_question)
    elif user_question.lower().strip() in ['exit', 'bye', 'quit']:
        print("Exiting App...")
        time.sleep(2)
        print("bye")
        break 
    else:
        print("Query not entered properly")
