from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from read_pdf import read_pdfs
from generate_embeddings import add_to_storage
from llm_query import llm_query

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

@app.post("/db_update")
async def startup_event():
    pdfs = read_pdfs("handbook_by_chapter")
    add_to_storage(pdfs)

@app.post("/query")
async def query(request: QueryRequest):
    try:
        response = llm_query(request.question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return response
