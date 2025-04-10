from autogen import AssistantAgent

llm_config = {
    "config_list": [{
        "model": "llama-3.2-3b-instruct",
        "base_url": "http://localhost:1234/v1",
        "api_key": "lm-studio"
        }],
    "cache_seed": None
}



writer = AssistantAgent(
    name="Writer",
    system_message="You are a writer. You write engaging and concise " 
        "blogposts (with title) on given topics. You must polish your "
        "writing based on the feedback you receive and give a refined "
        "version. Only return your final work without additional comments.",
    llm_config=llm_config,
)


critic = AssistantAgent(
    name="Critic",
    llm_config=llm_config,
    system_message="You are a critic. You review the work of "
                "the writer and provide constructive "
                "feedback to help improve the quality of the content.",
)





SEO_reviewer = AssistantAgent(
    name="SEO_Reviewer",
    llm_config=llm_config,
    system_message="You are an SEO reviewer, known for "
        "your ability to optimize content for search engines, "
        "ensuring that it ranks well and attracts organic traffic. " 
        "Make sure your suggestion is concise (within 3 bullet points), "
        "concrete and to the point. "
        "Begin the review by stating your role.",
)

legal_reviewer = AssistantAgent(
    name="Legal_Reviewer",
    llm_config=llm_config,
    system_message="You are a legal reviewer, known for "
        "your ability to ensure that content is legally compliant "
        "and free from any potential legal issues. "
        "Make sure your suggestion is concise (within 3 bullet points), "
        "concrete and to the point. "
        "Begin the review by stating your role.",
)

ethics_reviewer = AssistantAgent(
    name="Ethics_Reviewer",
    llm_config=llm_config,
    system_message="You are an ethics reviewer, known for "
        "your ability to ensure that content is ethically sound "
        "and free from any potential ethical issues. " 
        "Make sure your suggestion is concise (within 3 bullet points), "
        "concrete and to the point. "
        "Begin the review by stating your role. ",
)

# gather the work of other reviewers and give a final suggestion on the content to writer
meta_reviewer = AssistantAgent(
    name="Meta_Reviewer",
    llm_config=llm_config,
    system_message="You are a meta reviewer, you aggregate and review "
    "the work of other reviewers and give a final suggestion on the content.",
)

# NESTED Chat
# This will be triggereed once crtic receives the reply from writer
def reflection_message(recipient, messages, sender, config):
    return f'''Review the following content. 
            \n\n {recipient.chat_messages_for_summary(sender)[-1]['content']}'''

# message for each nested chat will be constructed by the reflection_messae() function
review_chats = [ # This is our nested chat
    {
     "recipient": SEO_reviewer, 
     "message": reflection_message, 
     "summary_method": "reflection_with_llm",
     "summary_args": 
        {
        "summary_prompt" : 
        "Return review into as JSON object only:"
        "{'Reviewer': '', 'Review': ''}. Here Reviewer should be your role",
        },
     "max_turns": 1},
    
    {
     "recipient": legal_reviewer, 
     "message": reflection_message, 
     "summary_method": "reflection_with_llm",
     "summary_args": {"summary_prompt" : 
        "Return review into as JSON object only:"
        "{'Reviewer': '', 'Review': ''}.",},
     "max_turns": 1},
    
    {"recipient": ethics_reviewer, 
     "message": reflection_message, 
     "summary_method": "reflection_with_llm",
     "summary_args": {"summary_prompt" : 
        "Return review into as JSON object only:"
        "{'reviewer': '', 'review': ''}",},
     "max_turns": 1},
    
     {"recipient": meta_reviewer, 
      "message": "Aggregrate feedback from all reviewers and give final suggestions on the writing.", 
      "max_turns": 1},
]



if __name__ == "__main__":
    task = '''
        Write a concise but engaging blogpost about
       udemy.com. Make sure the blogpost is
       within 200 words.
       '''


    # Register the nested chats. This will be triggered once critic receives the reply from writer
    critic.register_nested_chats(
        review_chats,
        trigger=writer,
    )
    #Main CHat
    chat_results = critic.initiate_chat(
        recipient=writer,
        message=task,
        max_turns=2,
        summary_method="last_msg"
    )



