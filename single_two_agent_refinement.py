
from autogen import AssistantAgent


llm_config = {
    "config_list": [{
        "model": "llama-3.2-3b-instruct",
        "base_url": "http://localhost:1234/v1",
        "api_key": "lm-studio"
        }],
    "cache_seed": None
}

task = '''
        Write a concise but engaging blogpost about
       udemy.com. Make sure the blogpost is
       within 200 words.
       '''

writer = AssistantAgent(
    name="Writer",
    system_message="You are a writer. You write engaging and concise " 
        "blogposts (with title) on given topics. You must polish your "
        "writing based on the feedback you receive and give a refined "
        "version. Only return your final work without additional comments.",
    llm_config=llm_config,
)

#For Multiagent use case
critic = AssistantAgent(
    name="Critic",
    llm_config=llm_config,
    system_message="You are a critic. You review the work of "
                "the writer and provide constructive "
                "feedback to help improve the quality of the content.",
)

#SINGLE AGENT REFLECTION : Only one agent we are asking to generate a reply
# reply = writer.generate_reply(messages=[{"content": task, "role": "user"}])
# print(reply)

#2 AGENT REFLECTION : Two agents are involved in the conversation
chat_result = critic.initiate_chat(
    recipient=writer,
    message=task,
    max_turns=2,
    summary_method="last_msg"
)

print(chat_result.summary)
