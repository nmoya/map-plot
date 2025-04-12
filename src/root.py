from fastapi import APIRouter, Form, Query, Request

from src.map_api import map_automplete
from src.svg_render import render
from src.templates import TemplateContext, template_response

router = APIRouter(
    tags=["root"],
)


@router.get("/")
async def root(request: Request):
    return template_response("index.html", TemplateContext(request=request))


@router.post("/")
async def render_address(request: Request, text: str = Form(...)):
    svg = render(text, 1600, 1200)
    return template_response(
        "index.html",
        TemplateContext(request=request, svg_content=str(svg), text=text, text_safe=text),
    )


@router.get("/autocomplete")
async def autocomplete(query: str = Query(...)):
    options = map_automplete(query)
    return [option["display_name"] for option in options]
