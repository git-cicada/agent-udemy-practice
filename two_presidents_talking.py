from autogen import ConversableAgent
llm_config = {
    "config_list": [{
        "model": "llama-3.2-3b-instruct",
        "base_url": "http://localhost:1234/v1",
        "api_key": "lm-studio"
        }],
    "cache_seed": None
}

pm = ConversableAgent(
    name="PM_Modi",
    llm_config=llm_config,
    system_message="You are Prime minister of India and you are talking to the president of USA. You are discussing about the "
    "current situation of the world and how India and USA can work together to make the world a better place. When you're ready to end the conversation, say 'Thanks to having you'.",
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: "Thanks to having you" in msg["content"],
)
president = ConversableAgent(
    name="President_Trumph",
    llm_config=llm_config,
    system_message="You are the president of USA and you are talking to the Prime minister of India. You are discussing about the "
    "current situation of the world and how India and USA can work together to make the world a better place. "
    "When you're ready to end the conversation, say 'Thanks to having you'.",
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: "Thanks to having you" in msg["content"],
)

# chat_result = agentBret.initiate_chat(
#     recipient = agentJemaine,
#     message="Hello Madam, let me tell you about the features of this car.", 
#     max_turns=2 # The conversation will stop after each agent has spoken twice
# )

chat_result = pm.initiate_chat(
    recipient = president,
    message="Hello Mr President, How are you? Let's talk about the current situation of the world.",
)