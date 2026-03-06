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
        "title": "Ubuntu",
        "content": "Ubuntu is now one of the most widely used Linux distributions. It is based on Debian, but it has a more consistent release schedule.",
        "date_posted": "March 01, 2026"
    },
    {
        "id": 2,
        "author": "Mimi Mensah",
        "title": "Debian",
        "content": "Debian is known for giving rise to well-known Linux distributions like Mint, Deepin, and Ubuntu, which have delivered outstanding results, reliability, and user interface.",
        "date_posted": "March 04, 2026"
    }
]

@app.get("/", include_in_schema=False, name="home")
@app.get("/posts", include_in_schema=False, name="posts")
def home(request: Request):
    return templates.TemplateResponse(request, "home.html", {"posts": posts, "title": "Home"})


@app.get("/api/posts")
def get_posts():
    return posts
