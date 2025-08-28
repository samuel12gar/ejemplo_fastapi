from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import os

app = FastAPI()

#Modelo simple
class Item(BaseModel):
    text: str


def get_db():
    db = sqlite3.connect("items.db")
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NO EXISTS items (id INTEGER PRIMARY KEY, text TEXT)")
    db.commit()
    return db

@app.get("/")
async def root():
    return {"message": "Hola Mundo con base de datos!"}

@app.get("/items")
async def get_items():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, text FROM items")
    items = cursor.fetchall()
    db.close()
    return [{"id": item[0],"text":item[1]} for item in items]

@app.post("/items")
async def create_item(item: Item):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO items (text) VALUES(?)",(item.text,))
    db.commit()
    item_id = cursor.lastrowid
    db.close()
    return {"id":{item_id},"text":item.text}



if __name__=="__main__":
    import uvicorn
    port = int(os.getenv("PORT",8000))
    uvicorn.run(app,host="0.0.0.0",port=port)

