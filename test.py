from app import question_anwering
from fastapi import FastAPI

"""
users= ['Sophia Al-Farsi',
        'Fatima El-Tahir',
        """
        'Armand Dupont',
        'Hans Müller',
        'Layla Kawaguchi',
        'Amina Van Den Berg',

#print(question_anwering("what are the likes of Vikram Desai?"))

app = FastAPI()


# Exposing it as an API endpoint
@app.get("/ask",
        description="Ask a query only specific to the user members present in the database")
def ask(query: str):
    result = question_anwering(query)
    return {"answer": result}


# To run the test app, use the command:
# uvicorn test:app --reload
#open http://127.0.0.1:8000/docs to see the interactive API documentation



