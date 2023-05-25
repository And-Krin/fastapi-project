from typing import Literal

# print(sys.path)
# sys.path.remove('.')
# print(sys.path)

# from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi.middleware.cors import CORSMiddleware

import models
from database import engine
from auth import items, users, auth

# print("In module products __package__, __name__ ==", __package__, __name__)

# load_dotenv('/.env')

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])
app.add_middleware(DBSessionMiddleware, db_url='postgresql://postgres:postgres@postgresql/test')

app.include_router(users.router)
app.include_router(items.router)
app.include_router(auth.router)


# Dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# sys.path.append(r'/sql_app/routers')



# To run locally
# if __name__ == '__main__':
#     uvicorn.run(app, host='0.0.0.0', port=8000)

# запуск докера: docker-compose up -d
# запуск проекта: uvicorn src/main:app --reload
# запуск фронта: npm start
