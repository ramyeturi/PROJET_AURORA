"""

import json 
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore


#loads api key from .env file
load_dotenv()

#load user messages from json file
with open('user_messages.json', 'r') as f:
    user_messages = json.load(f) 

print("json messages loaded")

users = list(user_messages['user_messages'].keys())

# initialize embeddings model and get embedding dimension
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
embedding_dim = len(embeddings.embed_query("dimension test"))
print("intialized embeddings model")

# function to create in-memory FAISS vector store
def create_in_memory_faiss_vector_store(msgs: list[str]) -> FAISS:
    """
    Create an in-memory FAISS vector store for a given list of texts.
    """
    
    index = faiss.IndexFlatL2(embedding_dim)
    vector_store = FAISS(
        embedding_function=embeddings,
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
    )
    docs = [Document(page_content=msg, metadata={"index": i}) for i, msg in enumerate(msgs)]
    vector_store.add_documents(docs)
    return vector_store


# create vector stores for each user
vector_stores = {
    username: create_in_memory_faiss_vector_store(messages.split('\n'))
    for username, messages in user_messages['user_messages'].items()
}
print("created vector stores for all users and ready to save to disk")

# save vector stores to disk
for username in users:
    vector_store_t = vector_stores[username]
    vector_store_t.save_local(f"vector_stores/username_{username.split()[0]}_vector_store") 

print("saved all vector stores to disk")