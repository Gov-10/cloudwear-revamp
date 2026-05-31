from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from typing import Optional
import requests,json
load_dotenv()
llm= ChatGroq(model='qwen/qwen3-32b', temperature=0, max_tokens=None, reasoning_format="hidden", timeout=None, max_retries=2)

class State(BaseModel):
    city: str
    res: Optional[str]=None
    latitude: Optional[float]=0.0
    longitude:Optional[float]=0.0
    temperature: Optional[float]=0.0
    wind_speed: Optional[float]=0.0
    relative_humid: Optional[float]=0.0

def city_node(state: State):
    city= state.city
    url= f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
    data = requests.get(url, timeout=10).json()
    latitude = data["results"][0]["latitude"]
    longitude = data["results"][0]["longitude"]
    url1=f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m,relative_humidity_2m"
    dt= requests.get(url1, timeout=10).json()
    temperature=dt["current"]["temperature_2m"]
    wind_speed=dt["current"]["wind_speed_10m"]
    relative_humid=dt["current"]["relative_humidity_2m"]
    return {"city":city, "latitude": latitude, "longitude": longitude, "temperature": temperature, "wind_speed":wind_speed, "relative_humid": relative_humid}

def ai_node(state: State):
    prompt=f"""
    Given below the city or area name, along with current weather and other metrics, provide a fun, friendly travel and clothing suggestion for a tourist visiting today
    city= {state.city}
    latitude={state.latitude}
    longitude={state.longitude}
    temperature={state.temperature}
    wind speed= {state.wind_speed}
    relative humidity= {state.relative_humid}
    """
    resp=llm.invoke(prompt)
    return {"res": resp.content}

graph=StateGraph(State)
graph.add_node("city", city_node)
graph.add_node("ai", ai_node)
graph.set_entry_point("city")
graph.set_finish_point("ai")
graph.add_edge("city", "ai")
graph.add_edge("ai", END)
agent=graph.compile()








