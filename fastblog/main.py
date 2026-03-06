from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

posts: list[dict] = [
    {
        "id": 1, 
        "author": "Cecil Mensah",
        "title": "Demographics",
        "content": "Introduction into FastAPI Blog",
        "date_posted": "March 01, 2026"
    },
    {
        "id": 2,
        "author": "Mimi Mensah",
        "title": "Infographics",
        "content": "Running into FastAPI Blog",
        "date_posted": "March 04, 2026"
    }
]

@app.get("/", include_in_schema=False)
@app.get("/posts", include_in_schema=False)
def home(request: Request):
    return templates.TemplateResponse(request, "home.html", {"posts": posts, "title": "Home"})


@app.get("/api/posts")
def get_posts():
    return posts
