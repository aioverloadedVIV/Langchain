# ReAct Agent with Multi-Tool Integration

An intelligent AI agent that combines reasoning and action to solve complex queries using multiple tools - Python execution, Wikipedia search, and web search.

## Overview

This project implements the ReAct (Reasoning + Acting) framework, enabling an LLM to break down complex problems, decide which tools to use, and iteratively work toward solutions. The agent can write and execute Python code, search Wikipedia, and perform web searches autonomously.

## Key Features

- **Multi-Tool Orchestration**: Seamlessly switches between Python REPL, Wikipedia, and DuckDuckGo search
- **ReAct Framework**: Uses chain-of-thought reasoning to plan and execute actions
- **Autonomous Problem Solving**: Breaks complex queries into actionable steps
- **Error Handling**: Robust parsing error management and iteration limits
- **Interactive CLI**: Real-time conversational interface

## Tech Stack

- **LLM**: OpenAI GPT-3.5-turbo
- **Framework**: LangChain with ReAct Agent
- **Tools**:
  - Python REPL (code execution)
  - Wikipedia API (knowledge lookup)
  - DuckDuckGo Search (web queries)
- **Language**: Python 3.x

## How It Works

1. **User Input**: Accepts natural language questions
2. **Reasoning**: Agent analyzes the query and determines required actions
3. **Tool Selection**: Chooses appropriate tool(s) from available options
4. **Action Execution**: Runs selected tools and observes results
5. **Iteration**: Repeats reasoning-action cycle until answer is found (max 10 iterations)
6. **Response**: Returns final answer based on gathered information

## Usage

Simply ask questions in natural language. The agent will:

- Determine which tool(s) to use
- Execute actions step-by-step
- Show its reasoning process (verbose mode)
- Provide final answers

Type `exit`, `quit`, or `bye` to end the session.

## Example Queries

- "What is the population of Tokyo and calculate its growth rate?"
- "Search for Python best practices and summarize key points"
- "Who invented the telephone and when was it patented?"
- "Calculate the area of a circle with radius 15.7"

## Use Cases

- Research assistant with computational capabilities
- Data analysis with web context
- Educational tool for learning and exploration
- Automated fact-checking and verification

## Technical Highlights

- **ReAct Prompting**: Industry-standard reasoning pattern from LangChain Hub
- **Tool Abstraction**: Modular design allows easy addition of new tools
- **Iteration Control**: Prevents infinite loops with max iteration limits
- **Verbose Logging**: Full transparency into agent decision-making

---

**Note**: Requires OpenAI API access. Agent makes autonomous decisions about tool usage.
