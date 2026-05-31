from fastapi import FastAPI
from schema import InputSchema
from utils.agents import agent
from fastapi.middleware.cors import CORSMiddleware
app=FastAPI()

@app.post("/res")
def resu(payload: InputSchema):
    city = payload.city
    result=agent.invoke({"city": city})
    return {"city": city, "result": result["res"]}
    


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
