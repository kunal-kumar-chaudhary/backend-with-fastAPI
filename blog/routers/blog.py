from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from .. import schemas, models, database
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/blog",
    tags=["blogs"]
)

@router.get("/", response_model=List[schemas.ShowBlog])
async def get_all(db: Session = Depends(database.get_db)):
    # querying on the Blog model to get all the blogs
    blogs = db.query(models.Blog).all()
    return blogs

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(request: schemas.Blog, db: Session = Depends(database.get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.get("/{id}", status_code=200, response_model=schemas.ShowBlog)
async def get_one(id: int, db: Session = Depends(database.get_db)):
    # getting a single blog corresponding to the id
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"Blog with id {id} not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    return blog

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def destroy(id: int, db: Session = Depends(database.get_db)):
    # deleting a blog corresponding to the id
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return "done"

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update(id: int, request: schemas.Blog, db: Session = Depends(database.get_db)):
    # updating a blog corresponding to the id
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    
    # updating the blog
    db.query(models.Blog).filter(models.Blog.id == id).update({"title": request.title, "body": request.body})
    db.commit()
    return "updated"
