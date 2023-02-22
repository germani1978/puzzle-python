import pandas as pd
import random
import json

from cruzigrama import Cruzigrama
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Permitir cualquier origen para CORS
origins = ["*"]

# Agregar el middleware de CORS a la aplicación
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return Cruzigrama().llena_puzzle()

    



