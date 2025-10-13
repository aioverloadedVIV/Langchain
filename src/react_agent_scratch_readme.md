# ReAct Agent from Scratch

## What This Project Does

A command-line chatbot that implements the ReAct (Reasoning + Acting) pattern using OpenAI's GPT-4o-mini model. The agent can think through problems, take actions using available tools, and provide answers based on observations.

## Why I Built This

To understand how AI agents work under the hood by building one from scratch without using frameworks like LangChain. This helps grasp the core concepts of:

- Agent reasoning loops (Thought → Action → Observation)
- Tool integration with LLMs
- Prompt engineering for agent behavior

## Tech Stack

- **OpenAI API** (gpt-4o-mini) - Cost-effective model for agent reasoning
- **Python 3.x**
- **httpx** - For Wikipedia API calls
- **python-dotenv** - Environment variable management
- **re** (regex) - For parsing agent actions

## How It Works

The agent follows a **ReAct loop**:

1. **Thought**: Reasons about what to do
2. **Action**: Calls a tool (calculate, get_cost, wikipedia)
3. **PAUSE**: Waits for observation
4. **Observation**: Gets tool result
5. **Answer**: Provides final response

Maximum 5 turns per query to prevent infinite loops.

## Available Tools

- `calculate`: Evaluates math expressions (e.g., "4 * 7 / 3")
- `get_cost`: Returns prices for pen ($5), book ($20), stapler ($10)
- `wikipedia`: Fetches summary from Wikipedia search

## Key Technical Decisions

### Why GPT-4o-mini?

Balance between cost and performance for experimentation

### Why Agent Class Pattern?

- Maintains conversation history in `self.messages`
- Separates system prompt initialization from execution
- Makes agent reusable and testable

### Why Regex for Action Parsing?

Simple pattern matching for "Action: tool_name: input" format without needing complex parsers

### Why max_turns=5?

Prevents runaway loops while allowing multi-step reasoning

## What I Learned

- How ReAct agents make LLMs more powerful through tool use
- Importance of clear system prompts with examples
- Regex for parsing structured LLM outputs
- Managing conversation state in agent loops
- The eval() security concern (fine for personal projects, dangerous in production)

## Example Usage

```
Type Your query or quit to exit: What is 25 * 4 divided by 2?
Thought: I need to calculate this
Action: calculate: 25 * 4 / 2
PAUSE
Observation: 50.0
Answer: The result is 50

Type Your query or quit to exit: How much would 3 books cost?
Thought: I should get the cost of a book first
Action: get_cost: book
PAUSE
Observation: A book costs $20
Answer: 3 books would cost $60
```
