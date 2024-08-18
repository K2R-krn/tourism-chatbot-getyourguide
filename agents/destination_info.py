from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool, AgentType

from tools.tools import get_destination_tourism_info


def get_destination_data(destination: str, question: str) -> str:
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    template = """
        Given the destination {destination} and the question {question}
        Can you find all the information about the destination from the 
        context of the given question, and then present your answer to the
        given question in this format:
        
        Your answer should be of this format:
        It should be in points, and each point should contain the following subtitles:
        1. Title 
        2. Description of the title: Describe location mentioned in the title  
        3. Link to the webpage
        4. Price 
        5. Reviews
        
        Your answer should also be of maximum 5 points most suitable to the question
    """

    tools_for_agent = [
        Tool(
            name="Scrape the Web for Tourism plans in destination",
            func=get_destination_tourism_info,
            description="Useful for when tourism plans and activities in the destination is required",
        )
    ]

    agent = initialize_agent(
        tools=tools_for_agent,
        llm=llm,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        verbose=True,
    )

    prompt_template = PromptTemplate(
        template=template, input_variables=["destination", "question"]
    )

    destination_info = agent.run(
        {
            "input": prompt_template.format_prompt(
                destination=destination, question=question
            ),
            "chat_history": [],
        }
    )

    return destination_info
