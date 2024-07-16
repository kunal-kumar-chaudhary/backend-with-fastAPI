from fastapi import APIRouter, HTTPException, status, Depends
from datetime import timedelta
from .. import schemas, models
from ..database import get_db
from sqlalchemy.orm import Session
from ..hashing import Hash
from ..token import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(
    tags=["authentication"]
)

@router.post("/login")
def login(request:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    # if there is no user with the email
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    # if there is user, we need to verify the password
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect password")
    
    # generate a jwt token and return
    access_token = create_access_token(data={"sub": user.email})
    return schemas.Token(access_token=access_token, token_type="bearer")