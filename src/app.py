from db.user import find_user_with_email
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.hash import argon2
from routes import products
from routes.utils import create_access_token

app = FastAPI()

app.include_router(products.router, prefix="/product")

@app.middleware("http")
async def request_middleware(request, call_next):
    print("Request started for {}".format(request.scope["path"]))
    try:
        return await call_next(request)
    except Exception as ex:
        print(f"Request failed: {ex}")
    finally:
        print("Request ended")

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = find_user_with_email(form_data.username)
    if user==None:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not argon2.verify(form_data.password,user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    data = {"user_id": user.user_id}
    encoded_jwt = create_access_token(data)
    return {"access_token": encoded_jwt, "token_type": "bearer"}