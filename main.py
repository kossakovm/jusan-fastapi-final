from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/sum1n/{num}")
def sum(num:int):
    sum=0
    for i in range(1, num+1):
        sum+=i 
    return{"result":sum}

@app.get("/fibo/")
def fibonacci(n:int):
    a = 0
    b = 1
    if n == 0:
        return{"result":a}
    elif n == 1:
        return{"result":b}
    else:
        for i in range(2, n):
            c = a + b
            a = b
            b = c
        return{"result":b}

@app.post("/reverse")
async def reverse(rqst: Request):
    str = rqst.headers.get('string')
    return{"result": str[::-1]}

class Item(BaseModel):
    element: str
elements = []

@app.put("/list")
async def putlist(item: Item):
    elements.append(item.element)
    return {"result": elements}

@app.get("/list")
async def getlist():
    return {"result": elements}

@app.post("/calculator")
async def calculator(expr: str):
    array = expr.split(',')
    num1 = int(array[0])
    num2 = int(array[2])
    operator = array[1] 
    result = -1
    if operator == '+':
        result = num1 + num2
    elif operator == '-':
        result = num1 - num2
    elif operator == '*':
        result = num1 * num2
    elif operator == '/':
        result = int(num1 / num2)
    else:
       result = "incalculable"
    return {"result": result}