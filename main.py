from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, field_validator 

templates = Jinja2Templates(directory="templates")

class Calc(BaseModel):
    a : int
    b: int
    sign: str

app = FastAPI()

def calculation(a: int, b:int, sign:str):
    if sign == '-':
        return a - b
    elif sign == '+':
        return a + b
    elif sign == '/':
        return a / b
    elif sign == '*':
        return a * b
    @field_validator('sign')
    def validator_operation(cls, v):
        if v not in ['+', '-', '/', '*']:
            raise ValueError('неизвестная операция')
        return v

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/calc", response_class=HTMLResponse)
async def plus(request: Request, a: str, b: str, sign: str):
    calc_input = Calc(a=a, b=b, sign=sign)
    c = (calculation(calc_input.a, calc_input.b, calc_input.sign))
    return templates.TemplateResponse(
        "calc.html", {"request": request, "c": c}
    )

# @app.get('/name', response_class=HTMLResponse)
# async def name(request: Request, first_name: str, last_name: str, surname: str):
#     return templates.TemplateResponse(
#         'name.html', {"request": request, "first_name": first_name, 'last_name': last_name, "surname": surname}, 
#     )