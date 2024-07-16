from fastapi import FastAPI, Depends, status, HTTPException, APIRouter
from typing import List
from .. import schemas, oauth2
from ..database import get_db 
from sqlalchemy.orm import Session
from ..controllers import user

router = APIRouter(
    prefix="/user",
    tags=["users"]
)

@router.post("/", response_model=schemas.ShowUser)
async def create_user(request: schemas.User, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return user.create_user(request, db)

@router.get("/{id}", response_model=schemas.ShowUser)
async def get_user(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return user.get_user(id, db)
