from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List

MONGODB_CONNECTION_STRING=os.environ["MONGODB_CONNECTION_STRING"]

client=AsyncIOMotorClient(MONGODB_CONNECTION_STRING,uuidRepresentation="standard")
db=client.todolist
todos=db.todos

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

class TodoItem(BaseModel):
    id: UUID = Field(default_factory=uuid4,alias="_id")
    content: str

class TodoItemCreate(BaseModel):
    content: str

todos: List[TodoItem] = []
id_counter = 1

@app.post("/todos", response_model=TodoItem)
async def create_todo(item: TodoItemCreate):
    global id_counter
    new_todo = TodoItem(id=id_counter, content=item.content)
    await todos.insert_one(new_todo.model_dump(by_alias=True))
    return new_todo

@app.get("/todos", response_model=List[TodoItem])
async def read_todos():
    return await todos.find().to_list(length=None)

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    delete_result=await todso.delete_one({"_id":todo_id})
    if delete_result.deleted_count==0:
      raise HTTPException(status_code=404, detail="Todo not found")        
    return {"message": "Todo deleted successfully"}
