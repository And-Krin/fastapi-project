# import jwt
# from fastapi import HTTPException, Security, APIRouter, Depends
# from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
# from passlib.context import CryptContext
# from datetime import datetime, timedelta
# from sqlalchemy.orm import Session
#
# from auth import schemas
# import crud, models
# from database import get_db
#
# router = APIRouter(tags=['auth'])
#
#
# class AuthHandler:
#     security = HTTPBearer()
#     pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#     secret = 'SECRET'
#
#     def get_password_hash(self, password):
#         return self.pwd_context.hash(password)
#
#     def verify_password(self, plain_password, hashed_password):
#         return self.pwd_context.verify(plain_password, hashed_password)
#
#     def encode_token(self, user_id):
#         payload = {
#             'exp': datetime.utcnow() + timedelta(days=0, minutes=5000),
#             'iat': datetime.utcnow(),
#             'sub': user_id
#         }
#         return jwt.encode(
#             payload,
#             self.secret,
#             algorithm='HS256'
#         )
#
#     def decode_token(self, token):
#         # print('Token', token, jwt.decode(jwt=token, key=self.secret, algorithms=['HS256']))
#         try:
#             payload = jwt.decode(token, self.secret, algorithms=['HS256'])
#
#             return payload['sub']
#         except jwt.ExpiredSignatureError:
#             raise HTTPException(status_code=401, detail='Signature has expired')
#         except jwt.InvalidTokenError as e:
#             raise HTTPException(status_code=401, detail='Invalid token')
#
#     def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
#         return self.decode_token(auth.credentials)
#
#
# auth_handler = AuthHandler()
#
#
# @router.post('/register', status_code=201)
# def register(
#         auth_pass: schemas.UserCreate,
#         db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_username(db, username=auth_pass.username)
#     if db_user:
#         raise HTTPException(status_code=400, detail='Username is taken')
#     return crud.create_user(db=db, user=auth_pass)
#
#
# @router.post('/login')
# def login(
#         auth_pass: schemas.UserLogin,
#         db: Session = Depends(get_db)):
#     user = None
#     users_db = db.query(models.User).all()
#     for x in users_db:
#         if x.username == auth_pass.username:
#             user = crud.get_user_by_username(db=db, username=auth_pass.username)
#             break
#     if (user is None) or (not auth_handler.verify_password(auth_pass.password, user.hashed_password)):
#         raise HTTPException(status_code=401, detail='Invalid username and/or password')
#     token = auth_handler.encode_token(user.id)
#     return {'token': token}
#
#
# @router.post('/unprotected')
# def unprotected():
#     return {'hello': 'world'}
#
#
# @router.get('/protected',
#             dependencies=[Depends(auth_handler.auth_wrapper)])
# def protected(user_id=Depends(auth_handler.auth_wrapper)):
#     return {"user_id": user_id}
