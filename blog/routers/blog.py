from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from .. import schemas, models, database
from sqlalchemy.orm import Session
from ..controllers import blog


router = APIRouter(
    prefix="/blog",
    tags=["blogs"]
)

@router.get("/", response_model=List[schemas.ShowBlog])
async def all(db: Session = Depends(database.get_db)):
    return blog.get_all(db)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(request: schemas.Blog, db: Session = Depends(database.get_db)):
    return blog.create(db, request)

@router.get("/{id}", status_code=200, response_model=schemas.ShowBlog)
async def get_one(id: int, db: Session = Depends(database.get_db)):
    return blog.get_one(db, id)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def destroy(id: int, db: Session = Depends(database.get_db)):
    return blog.destroy(id, db)

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update(id: int, request: schemas.Blog, db: Session = Depends(database.get_db)):
    return blog.update(id, request, db)
