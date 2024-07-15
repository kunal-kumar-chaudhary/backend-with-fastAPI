from fastapi import FastAPI
from . import models
from .database import engine 
from .routers import blog, user, authentication

app = FastAPI()


# migrating all the tables to the database whenever we run the server (run main.py file)
models.Base.metadata.create_all(bind=engine)

# registering routes
app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)






