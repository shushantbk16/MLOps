import chromadb
import os
from chromadb.utils import embedding_functions

client=chromadb.Client()
embedding_fn=embedding_function.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

collection=client.get_or_create_collection(
    name="interview_demo",
    embedding_function=embedding_fn
)

def add_data_to_db(text_corpus):
    chunk_size=200
    overlap=50
    chunks=[]

    for i in range(0,len(text_corpus),chunk_size-overlap):
        chunk=text_corpus[i:i +chunk_size]
        chunks.append(chunk)

    ids=[str(i) for i in range(len(chunks))]
    collection.add(
        documents=chunks,
        ids=ids
    )
def retrieve_context(query):

    results=collection.query(
        query_texts=[query],
        n_results=2
    )

    retrieved_chunks = results['documents'][0]
    for i, chunk in enumerate(retrieved_chunks):
        print(f"       Result {i+1}: \"{chunk}\"")
        
    return retrieved_chunks

if __name__=="__main__":
    sop_data="""SOP-101: Laboratory Safety Protocols.
    All personnel must wear Grade-A protective gear when handling Chronium.
    Chronium is highly unstable at temperatures above 50 degrees Celsius.
    If a spill occurs, evacuate the room immediately and trigger the Halon suppression system.
    Do not use water on Chronium fires; it causes an explosion.
    Reporting: All incidents must be logged in the QMS within 1 hour.
    """
    add_data_to_db(sop_data)
    query="What do I do if chronium spills?"
    context=retrieve_context(query)