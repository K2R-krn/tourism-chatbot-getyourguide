from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

from validate import validate_openai_key


def find_question_type(question: str) -> bool:
    """
    Given a prompt by the user, this function finds out if the prompt is
    a question related to tours and travels or not
    :param question: question asked by the user
    :return: bool: True or False
    """

    valid = validate_openai_key()
    if not valid:
        print("API Key not present in the environment")
        return False

    template = """
        Given the text:
        {question}
        Can you answer as "true" if the text is related to tourism, tours, or travels,
        else, answer as "false".
        Your answer should only contain either the word "true" or "false"
    """

    prompt_template = PromptTemplate(input_variables=["question"], template=template)

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    chain = LLMChain(llm=llm, prompt=prompt_template)

    answer = chain.run(question=question)

    if "true" in answer:
        return True
    else:
        return False


def answer_non_travel_question(question: str) -> str:
    """
    Answers any question that is not a travel question
    :param question:
    :return:
    """

    valid = validate_openai_key()
    if not valid:
        print("API Key not present in the environment")
        return ""

    template = """
            Given the text:
            {question}
            Please give out a suitable answer
        """

    prompt_template = PromptTemplate(input_variables=["question"], template=template)

    llm = ChatOpenAI(temperature=0.5, model_name="gpt-3.5-turbo")

    chain = LLMChain(llm=llm, prompt=prompt_template)

    answer = chain.run(question=question)

    return answer


def get_destination(question: str) -> str:
    """
    This function takes in a question and tries to figure out if the destination is
    mentioned in the question.
    :param question:
    :return:
    """
    valid = validate_openai_key()
    if not valid:
        print("API Key not present in the environment")
        return ""

    template = """
               Given the text:
               {question}
               Can you read the text and find out if the text is curious about a certain destination he wants to tour?
               Your answer should be of one word, and it should only contain the destination the user wants to go to.
               If the user is not talking about any destination, your answer should again be only one word and it should
               be "false__no_destination"
           """

    prompt_template = PromptTemplate(input_variables=["question"], template=template)

    llm = ChatOpenAI(temperature=0.5, model_name="gpt-3.5-turbo")

    chain = LLMChain(llm=llm, prompt=prompt_template)

    answer = chain.run(question=question)

    return answer


def get_location_curiosity(destination: str, question: str) -> bool:
    """
    This function takes in a question and tries to figure out if the
    question asked is curious about a destination, or wants to get
    information about the tours in that destination
    :param destination: Destination extracted from the question
    :param question: The question at hand
    :return: True or false
    """
    valid = validate_openai_key()
    if not valid:
        print("API Key not present in the environment")
        return False

    template = """
               Given the destination {destination}
               and the question {question}
               answer as "false" if the question asked represents wanting to travel
               to that location. and answer as "true" if the question asked at the moment
               has no intent on travelling there at the moment.
               Your answer should only contain the word "true" or "false"
           """

    prompt_template = PromptTemplate(input_variables=["destination", "question"], template=template)

    llm = ChatOpenAI(temperature=0.5, model_name="gpt-3.5-turbo")

    chain = LLMChain(llm=llm, prompt=prompt_template)

    answer = chain.run(destination=destination, question=question)

    if "true" in answer:
        return True
    else:
        return False
