# Level 1
# @app.get("/")
# def home():
#     return {"name": "Ebad", "goal": "Forward Deployed Engineer"}
# Level 2
# todos=[]
# @app.get("/")
# def home():
#     return {"message": "Todos website."}
# @app.get("/todos")
# def get_todos():
#     return todos
# @app.post(f"/todos")
# def create_task(task: str):
#     todos.append(task)
#     return {"message": "Task created successfully."}
# @app.delete("/todos/{index}")
# def delete_task(index: int):
#     todos.pop(index)
#     return {"message": "Task is deleted successfully."}
# Level 3
# class CreateTask(BaseModel):
#     title:str=Field(..., min_length=3, max_length=20)
#     done:bool=False
# todos=[]
# @app.get("/")
# def home():
#     return {"message": "Todos website."}
# @app.get("/todos")
# def get_todos():
#     return todos
# @app.post(f"/todos")
# def create_task(task: CreateTask):
#     todos.append(task)
#     return {"message": "Task created successfully."}
# @app.put("/todos/{index}")
# def mark_as_done(index: int):
#     for i, task in enumerate(todos):
#         if index==i:
#             task["done"]=True
#             return {"message": "Task done as completed."}
# @app.delete("/todos/{index}")
# def delete_task(index: int):
#     todos.pop(index)
#     return {"message": "Task is deleted successfully."}
# Capstone
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
import json
import os
from dotenv import load_dotenv
from groq import AsyncGroq
app = FastAPI()
work_orders = []
current_id = 0
load_dotenv()
api_key=os.getenv("GROQ_API_KEY")
client=AsyncGroq(api_key=api_key)
try:
    with open("workorders.json", "r") as file:
        data = json.load(file)
    work_orders = data
    current_id = max(order["order_id"] for order in work_orders) + 1
except(FileNotFoundError, ValueError, json.JSONDecodeError):
    work_orders = []
    current_id = 0

class Customer(BaseModel):
    name:str=Field(..., min_length=2, max_length=30)
    contact_num:str=Field(..., min_length=10, max_length=15)
class WorkOrder(BaseModel):
    description: str = Field(..., min_length=5, max_length=200)
    status: bool
    priority: Literal["high", "low"]
    customer:Customer
class UpdateStatus(BaseModel):
    order_id:int
    status: bool
class ResponseOrder(BaseModel):
    order_id: int
    description: str
    status: bool
    priority: Literal["high", "low"]
    customer:Customer

@app.get("/")


def home():
    return {"message": "This is work orders website."}


@app.get("/work-orders", response_model=list[ResponseOrder])


def get_workorders():
    return work_orders


@app.post("/work-orders")


def create_workorder(workorder: WorkOrder):
    global current_id
    order = {
        "order_id": current_id,
        "customer":{
        "name": workorder.customer.name,
        "contact_num": workorder.customer.contact_num,
        },
        "description": workorder.description,
        "status": workorder.status,
        "priority": workorder.priority,
    }
    work_orders.append(order)
    current_id += 1
    with open("workorders.json", "w") as file:
        json.dump(work_orders, file)
    return {"message": "Work order created successfully."}


@app.put("/work-orders")


def update_status(update: UpdateStatus):
    for order in work_orders:
        if order["order_id"]==update.order_id:
            order["status"]=update.status
            with open("workorders.json", "w") as file:
                json.dump(work_orders, file)
                    
            return {"message": "Status updated successfully."}
    raise HTTPException(status_code=404, detail="Given id does not exist.")


@app.get("/work-orders/{id}", response_model=ResponseOrder)


def get_workorder(id: int):
    for order in work_orders:
        if order["order_id"] == id:
            return order
    raise HTTPException(status_code=404, detail="Given id not found.")
@app.get("/work-orders/summarize/{id}")
async def summarize(id: int):
    order=next((order for order in work_orders if order["order_id"]==id), None)
    if order is None:
        raise HTTPException(status_code=404, detail="Given id does not exist.")
    response=await client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
        {
            "role":"user",
            "content":f"Summarize this description: {order['description']}"
        }
        ]
    )
    return {"response": response.choices[0].message.content}
@app.delete("/work-orders/{id}")
def delete_order(id: int):
    order=next((order for order in work_orders if order["order_id"]==id), None)
    if order is None:
        raise HTTPException(status_code=404, detail="Given id does not exist.")
    work_orders.remove(order)
    with open("workorders.json", "w") as file:
        json.dump(work_orders, file)
    return {"response": "Order deleted successfully."}