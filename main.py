from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, field_validator, ValidationError
from typing import Union

templates = Jinja2Templates(directory="templates")


class Calc(BaseModel):
    a: Union[int, float]
    b: Union[int, float]
    sign: str

    @field_validator("sign")
    def validator_operation(cls, v):
        if v not in ["+", "-", "*", "/"]:
            raise ValueError("Недопустимая операция")
        return v


class Name(BaseModel):
    first_name: str
    last_name: str
    surname: str


class CalcOutput(BaseModel):
    a: Union[int, float] = 0
    b: Union[int, float] = 0
    c: Union[int, float] = 0
    sign: str = None
    error: Union[str, None] = None


app = FastAPI()


def calculation(a: int, b: int, sign: str):
    if sign == "-":
        return a - b
    elif sign == "+":
        return a + b
    elif sign == "/":
        return a / b
    elif sign == "*":
        return a * b


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/calc", response_class=HTMLResponse)
async def plus(request: Request, a: str, b: str, sign: str):
    try:
        calc_input = Calc(a=a, b=b, sign=sign)
        c = calculation(calc_input.a, calc_input.b, calc_input.sign)
        calc_output = CalcOutput(a=a, b=b, sign=sign, c=c)
        calc_output = CalcOutput(
            a=calc_output.a, b=calc_output.b, c=calc_output.c, sign=calc_output.sign
        )
        return templates.TemplateResponse(
            "calc.html", {"request": request, "calc_output": calc_output}
        )
    except ValidationError:
        calc_output = CalcOutput(error="брат ты забыл что такое числа?")
        return templates.TemplateResponse(
            "calc.html",
            {"request": request, "calc_output": calc_output},
        )
    except Exception:
        calc_output = CalcOutput(error="что то непонятное ты делаешь")
        return templates.TemplateResponse(
            "calc.html", {"request": request, "calc_output": calc_output}
        )


@app.get("/name", response_class=HTMLResponse)
async def name(request: Request, first_name: str, last_name: str, surname: str):
    return templates.TemplateResponse(
        "name.html",
        {
            "request": request,
            "first_name": first_name,
            "last_name": last_name,
            "surname": surname,
        },
    )
