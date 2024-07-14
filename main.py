from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def index():
    return {"data": {"name": "kunal", "age": 25}}

@app.get("/about")
def about():
    return {"data": {"about": "This is about page"}}