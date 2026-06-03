from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


templates = Jinja2Templates(directory="templates")

fake_user = {}
        


app = FastAPI()

app.mount('/static', StaticFiles(directory='static'))


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/signup", response_class=HTMLResponse)
async def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@app.post("/signup/processing")
async def create_account(
    request: Request, nickname: str = Form(...), password: str = Form(...)
):
    print(nickname)
    print(password)
    fake_user["nickname"] = nickname
    fake_user["password"] = password
    fake_user['photo'] = '/static/photo.jpg'
    return RedirectResponse("/profile", status_code=302)


@app.get("/profile")
async def profile(request: Request):
    return templates.TemplateResponse(
        "profile.html", {"request": request, "nickname": fake_user.get("nickname"), 'photo_url': fake_user.get('photo')}
    )
