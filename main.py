from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from db.users import add_user, init_db, user_exists, get_user
from starlette.middleware.sessions import SessionMiddleware
from db.posts import add_post, get_post


templates = Jinja2Templates(directory="templates")


app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="novi_secret_key")


@app.on_event("startup")
async def startup():
    await init_db()


app.mount("/static", StaticFiles(directory="static"))


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    posts = await get_post()

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "posts": posts},
    )


@app.get("/signup", response_class=HTMLResponse)
async def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@app.post("/signup/processing")
async def create_account(
    request: Request, nickname: str = Form(...), password: str = Form(...)
):
    print(nickname)
    print(password)

    if await user_exists(nickname):
        return templates.TemplateResponse(
            "signup.html",
            {
                "request": request,
                "error": "Никнейм занят. придумай что-нибудь уникальное",
            },
        )

    if len(password) < 6:
        return templates.TemplateResponse(
            "signup.html",
            {
                "request": request,
                "error": "Пароль слишком короткий. Минимум 6 символов",
            },
        )

    await add_user(password, nickname)

    request.session["nickname"] = nickname

    return RedirectResponse("/profile", status_code=302)


@app.get("/login", response_class=HTMLResponse)
async def loggin(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login/processing")
async def login(request: Request, nickname: str = Form(...), password: str = Form(...)):
    user = await get_user(nickname)

    if user is None:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": "Пользователь не найден",
            },
        )

    if user[1] != password:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": "Неверный пароль",
            },
        )

    request.session["nickname"] = nickname

    return RedirectResponse("/profile", status_code=302)


@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=302)


@app.get("/profile")
async def profile(request: Request):

    nickname = request.session.get("nickname")

    if not nickname:
        return templates.TemplateResponse("need_login.html", {"request": request})

    # передаём посты пользователя в профиль (по умолчанию берём все записи из БД)
    posts = await get_post()
    user_posts = [p for p in posts if p[1] == nickname]

    return templates.TemplateResponse(
        "profile.html",
        {
            "request": request,
            "nickname": nickname,
            "photo_url": "/static/photo.jpg",
            "posts": user_posts,
        },
    )


@app.get("/post")
async def post(request: Request):
    nickname = request.session.get("nickname")
    if not nickname:
        return templates.TemplateResponse("need_login.html", {"request": request})

    return templates.TemplateResponse(
        "post.html",
        {"request": request, "nickname": nickname},
    )


@app.get("/create_post")
async def create_post_page(request: Request):
    nickname = request.session.get("nickname")
    if not nickname:
        return templates.TemplateResponse("need_login.html", {"request": request})

    return templates.TemplateResponse("post.html", {"request": request, "nickname": nickname})


@app.post("/create_post")
async def create_post_post(request: Request, content: str = Form(...)):
    nickname = request.session.get("nickname")

    if not nickname:
        return RedirectResponse("/", status_code=302)

    await add_post(nickname, content)
    return RedirectResponse("/profile", status_code=302)
