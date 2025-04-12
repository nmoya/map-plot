from typing import List

from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, ConfigDict, field_serializer

templates = Jinja2Templates(directory="templates")


class TemplateContext(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    request: Request | None = None
    text: str | None = None
    text_safe: str | None = None
    svg_content: str | None = None
    error: str | None = None

    @field_serializer("request")
    def serialize_request(self, request: Request, _info) -> str:
        return request

    @field_serializer("text_safe")
    def serialize_text_safe(self, text_safe: str | None) -> str | None:
        if text_safe is None:
            return None
        return text_safe.replace(" ", "_").replace("/", "")


def template_response(template_name: str, context: TemplateContext):
    return templates.TemplateResponse(template_name, context.model_dump())


def html_response(template_name: str, contexts: TemplateContext | List[TemplateContext]):
    if not isinstance(contexts, list):
        contexts = [contexts]
    template = templates.get_template(template_name)
    htmls = []
    for context in contexts:
        htmls.append(template.render(context.model_dump()))
    return HTMLResponse("\n".join(htmls))
