from fastapi import FastAPI, Depends, status, Response, HTTPException
from typing import Optional, List
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from .hashing import Hash

app = FastAPI()


# migrating all the tables to the database whenever we run the server (run main.py file)
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog", status_code=status.HTTP_201_CREATED, tags=["blogs"])
async def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get("/blog", response_model=List[schemas.ShowBlog], tags=["blogs"])
async def get_all(db: Session = Depends(get_db)):
    # querying on the Blog model to get all the blogs
    blogs = db.query(models.Blog).all()
    return blogs

@app.get("/blog/{id}", status_code=200, response_model=schemas.ShowBlog, tags=["blogs"])
async def get_one(id: int, response: Response, db: Session = Depends(get_db)):
    # getting a single blog corresponding to the id
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"Blog with id {id} not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    return blog

@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["blogs"])
async def destroy(id: int, db: Session = Depends(get_db)):
    # deleting a blog corresponding to the id
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return "done"

@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["blogs"])
async def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    # updating a blog corresponding to the id
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    
    # updating the blog
    db.query(models.Blog).filter(models.Blog.id == id).update({"title": request.title, "body": request.body})
    db.commit()
    return "updated"

@app.post("/user", response_model=schemas.ShowUser, tags=["users"])
async def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/user/{id}", response_model=schemas.ShowUser, tags=["users"])
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with {id} not found")
    return user
