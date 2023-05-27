from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.schema import Register, RegisterRes, LogIn, UpdateUserSchema
from app.model import User
from fastapi_jwt_auth import AuthJWT
from werkzeug.security import generate_password_hash, check_password_hash


auth = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@auth.get('/')
async def hello():
    return {'hi'}


@auth.post('/sign-up', response_model=RegisterRes, status_code=status.HTTP_201_CREATED)
async def Sign_up(user: Register, db: Session = Depends(get_db)):
    db_email = db.query(User).filter(User.email == user.email).first()
    if db_email is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with email already exist :(")

    db_username = db.query(User).filter(User.username == user.username).first()
    if db_username is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with username already exist :(")

    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_admin=user.is_admin
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    resp = new_user
    return resp


@auth.put('/update-user/{id}', response_model=RegisterRes)
async def update_user(new_user: UpdateUserSchema, authorize: AuthJWT = Depends(), db: Session = Depends(get_db),
                      identity: int = {id}):
    if identity is None:
        identity = {id}
    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token :(")
    current_user = authorize.get_jwt_subject()

    db_user = db.query(User).filter(User.username == current_user).first()
    user = db.query(User).filter(User.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")
    if db_user.id != id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user :(")
    user.username = new_user.username
    user.email = new_user.email
    db.commit()
    db.refresh(user)
    return user


@auth.post('/log-in', status_code=200)
async def log_in(user: LogIn, authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()

    if db_user and check_password_hash(db_user.password, user.password):
        access_token = authorize.create_access_token(subject=db_user.username)
        refresh_token = authorize.create_refresh_token(subject=db_user.username)

        response = {
            'access_token': access_token,
            'refresh_token': refresh_token,
        }
        return jsonable_encoder(response)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username or password :(")


@auth.get('/refresh')
async def refresh_token(authorize: AuthJWT = Depends()):
    try:
        authorize.jwt_refresh_token_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Refresh Token :(")

    current_user = authorize.get_jwt_subject()
    access_token = authorize.create_access_token(subject=current_user)

    return jsonable_encoder({
        'access_token': access_token
    })
