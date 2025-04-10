# We'll always have to start by creating a llm_config object to configure our agents
# llm_config = {
#     "model": "gpt-4o", 
#     "api_key": "sk-proj-1",
#     }

llm_config = {
    "config_list": [{
        "model": "llama-3.2-3b-instruct",
        "base_url": "http://localhost:1234/v1",
        "api_key": "lm-studio"
        }],
    "cache_seed": None
}

# Command Line Executor
from autogen.code_utils import create_virtual_env
from autogen.coding import CodeBlock, LocalCommandLineCodeExecutor

venv_dir = ".coding/env_llm"
venv_context = create_virtual_env(venv_dir)

executor = LocalCommandLineCodeExecutor(
    virtual_env_context=venv_context,
    timeout=200,
    work_dir="coding",
)
print(
    executor.execute_code_blocks(code_blocks=[CodeBlock(language="python", code="import sys; print(sys.executable)")])
)

# ---

# Agent 1: Code Writer agent
from autogen import AssistantAgent
from autogen import ConversableAgent

# Agent that writes code
code_writer_agent = AssistantAgent(
    name="code_writer_agent",
    llm_config=llm_config,
    code_execution_config=False,
    human_input_mode="NEVER",
)

# Code writer agent default prompt
code_writer_agent_system_message = code_writer_agent.system_message
print('code_writer_agent_system_message',code_writer_agent_system_message)


import pdb; pdb.set_trace()
# 'continue' to unfreeze the code execution & 'exit' to exit the debugger


# Agent 2: Code Executor agent
code_executor_agent = ConversableAgent(
    name="code_executor_agent",
    llm_config=False, #It will just execute hence does not need any LLM intercation
    code_execution_config={"executor": executor},
    human_input_mode="ALWAYS", #LLM generated code(Agent 1) could be malicious hence human intervenation always needed before execution
    default_auto_reply=
    "Please continue. If everything is done, reply 'TERMINATE'.",
)

# ---

# Coding Task
import datetime

today = datetime.datetime.now().date()

message = f"Today is {today}. "\
"Create a plot showing the normalized price of NVDA and BTC-USD for the last 5 years "\
"with their 60 weeks moving average. "\
"Make sure the code is in markdown code block, print the normalized prices, save the figure"\
" to a file asset_analysis.png and show it. Provide all the code necessary in a single python bloc. "\
"Re-provide the code block that needs to be executed with each of your messages. "\
"If python packages are necessary to execute the code, provide a markdown "\
"python block with only the command necessary to install them and no comments."

# Let's define the chat and initiate it !
chat_result = code_executor_agent.initiate_chat(
    code_writer_agent,
    message=message
)