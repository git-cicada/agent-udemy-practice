"""
pip install pyautogen
pip install openai
"""

from autogen import ConversableAgent
llm_config = {
    "config_list": [{
        "model": "llama-3.2-3b-instruct",
        "base_url": "http://localhost:1234/v1",
        "api_key": "lm-studio"
        }],
    "cache_seed": None
}

# agentBret = ConversableAgent(
#     name="Bret",
#     llm_config=llm_config,
#     system_message="Your name is Bret and you are a car sales man and you are trying to sell a latest overpriced model to customer Jeminae who plans to buy a car for her husband. You are trying to convince her to buy the car by telling her about the features and benefits of the car.",
# )
# agentJemaine = ConversableAgent(
#     name="Jemaine",
#     llm_config=llm_config,
#     system_message="Your name is Jemain and you are wife of a rich person. Bret trying to convince you to buy a car for your husband. You are not interested in buying the car but you are trying to be polite and listen to Bret's sales pitch.",
# )

agentBret = ConversableAgent(
    name="Bret",
    llm_config=llm_config,
    system_message="Your name is Bret and you are a stand-up comedian in a two-person comedy show. "
    "When you're ready to end the conversation, say 'I gotta go'.",
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: "I gotta go" in msg["content"],
)
agentJemaine = ConversableAgent(
    name="Jemaine",
    llm_config=llm_config,
    system_message="Your name is Jemine and you are a stand-up comedian in a two-person comedy show. "
    "When you're ready to end the conversation, say 'I gotta go'.",
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: "I gotta go" in msg["content"],
)

# chat_result = agentBret.initiate_chat(
#     recipient = agentJemaine,
#     message="Hello Madam, let me tell you about the features of this car.", 
#     max_turns=2 # The conversation will stop after each agent has spoken twice
# )

chat_result = agentBret.initiate_chat(
    recipient = agentJemaine,
    message="Hello Jemine, let me tell you a joke.",
)