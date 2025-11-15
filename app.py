import json 
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import create_agent


#loads api key from .env file
load_dotenv()
"""

#load user messages from json file
with open('user_messages.json', 'r') as f:
    user_messages = json.load(f) 
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

#load vector stores from disk
vector_stores = {
    username: FAISS.load_local(f"vector_stores/username_{username.split()[0]}_vector_store", embeddings, allow_dangerous_deserialization=True)
    for username in users
}


# function that takes query and username and returns relevant messages
@tool
def get_relevant_member_messages(username: str, query: str) -> str:
    """
    Function to get relevant information about the query asked about the member or user
    with the help of username and query, and return the information most closely
    related to that query.

    Args:
        username: Exact user name of the member whose messages should be searched.
        query: A detailed description of what information to look for from the query.
    """
    vector_store = vector_stores.get(username)
    if not vector_store:
        return "no messages exists for this user"
    docs = vector_store.similarity_search(query, k=15) # retrieve top 15 relevant messages
    docs.sort(key=lambda doc: doc.metadata["index"])
    return "\n ".join([doc.page_content for doc in docs])

model = ChatOpenAI(
                    model="gpt-4o-mini",
                    temperature=0,
                )



system_prompt = """
You are an assistant designed to answer questions about member-specific information using semantic search. 
You do not store or generate personal details yourself; all information must come from the provided function interface.

You can answer questions only about the following users:

Sophia Al-Farsi,
Fatima El-Tahir,
Armand Dupont,
Hans Müller,
Layla Kawaguchi,
Amina Van Den Berg,
Vikram Desai,
Lily O’Sullivan,
Lorenzo Cavalli,
Thiago Monteiro.

To answer any question about one of these users, you must call the function:

get_relevant_member_messages(username, query)

• username must exactly match one name in the list above.
• query must NOT contain the user’s name or terms like “the user,” “this member,” etc.  
  It should contain only the information being requested — the topic, context, or details needed to understand what the user wants to know.

If the user asks about anyone not in the list, respond by saying I don’t have any data about them, mentioning the name from the query.

You may not answer directly; the function is the only source of truth for member-related information.
If the user asks about any of the listed users, respond only by calling get_relevant_member_messages.

Do not explain how the information was found.  
Do not say phrases like “I found,” “my search shows,” or “according to the data.”  
The final answer must read as a direct response, as if the information is simply being provided naturally.
"""

#create the agent using the model, tool and system prompt
agent = create_agent(
    model,
    tools =[get_relevant_member_messages],
    system_prompt=system_prompt,
)


def question_anwering(query:str):
    response = agent.invoke({
        "messages": [{"role": "user", "content": query}]
    })
    return response['messages'][-1].content



if __name__ == "__main__":
    print(question_anwering("what are the numbers of ram? answer with user name"))


