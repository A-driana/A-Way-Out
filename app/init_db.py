from db import engine
from model import *

Base.metadata.create_all(bind=engine)
