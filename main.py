from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import math
import prometheus_client
from prometheus_client import Counter
from prometheus_client import Histogram
from prometheus_client import Gauge

app = FastAPI()
c = Counter('http_requests_total', 'Number of HTTP requests received')
h = Histogram('http_requests_milliseconds', 'Duration of HTTP requests in milliseconds')
g = Gauge('last_sum1n', 'Value stores last result of sum1n')
g1 = Gauge('last_fibo', 'Value stores last result of fibo')
g2 = Gauge('list_size', 'Value stores current list size')
g3 = Gauge('last_calculator', 'Value stores last result of calculator')
c1 = Counter('errors_calculator_total', 'Number of errors in calculator')
metrics_app = prometheus_client.make_asgi_app()
app.mount("/metrics", metrics_app)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/sum1n/{num}")
def sum(num:int):
    c.inc() 
    h.observe(2)
    sum=0
    for i in range(1, num+1):
        sum+=i 
    g.set(sum)
    return{"result":sum}
    

@app.get("/fibo/")
def fibonacci(n:int):
    a = 0
    b = 1
    if n == 0:
        g1.set(a)
        return{"result":a}
    elif n == 1:
        g1.set(b)
        return{"result":b}
    else:
        for i in range(2, n):
            c = a + b
            a = b
            b = c
            g1.set(b)
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
    g2.set(len(elements))
    return {"result": elements}

@app.post("/calculator")
async def calculator(expr: str):
    array = expr.split(',') 
    if len(array) == 3:
        num1 = int(array[0])
        num2 = int(array[2])
        operator = array[1] 
        result = -1
        if operator == '+':
            g3.set(num1 + num2)
            result = num1 + num2
        elif operator == '-':
            g3.set(num1 - num2)
            result = num1 - num2
        elif operator == '*':
            g3.set(num1 * num2)
            result = num1 * num2
        elif operator == '/':
            if num2==0:
                g3.set(num2)
                c1.inc()
                result = "cannot divide to zero"
            else:
                g3.set(num1 / num2)
                result = int(num1 / num2)
        elif operator == '^':
            g3.set(num1 ** num2)
            result = num1 ** num2
    elif len(array) == 2:
        num1 = int(array[0])
        operator = array[1]
        result = math.factorial(num1)
    else:
       result = "invalid"
       c1.inc()
    return {"result": result}