import importlib.metadata
import json
import os
from os import path
from typing import Union

from fastapi import FastAPI, Query, applications
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from funcaptcha import funcaptcha

projectMetadata = importlib.metadata.metadata('funcaptcha-token')
app = FastAPI(
    title=projectMetadata['Name'].title().replace('-', ' '),
    description=projectMetadata['Summary'],
    version=projectMetadata['Version'],
    contact={
        "url": projectMetadata['Home-page']
    },
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    license_info={
        "name": "MIT License",
        "url": projectMetadata['License']
    }
)

assets_path = os.getcwd() + "/swagger-ui-assets"
if path.exists(assets_path + "/swagger-ui.css") and path.exists(assets_path + "/swagger-ui-bundle.js"):
    app.mount("/assets", StaticFiles(directory=assets_path), name="static")


    def swagger_monkey_patch(*args, **kwargs):
        return get_swagger_ui_html(
            *args,
            **kwargs,
            swagger_favicon_url="",
            swagger_css_url="/assets/swagger-ui.css",
            swagger_js_url="/assets/swagger-ui-bundle.js",
        )


    applications.get_swagger_ui_html = swagger_monkey_patch


@app.get("/", response_class=RedirectResponse, include_in_schema=False)
async def index():
    return "/docs"


@app.post("/token", tags=["Endpoints"])
async def token(
        public_key: str = Query(description="FunCaptcha public key"),
        service_url: Union[str, None] = Query(default="https://tcr9i.chat.openai.com", description="Some websites can have a custom service URL"),
        site_url: Union[str, None] = Query(default="https://auth0.openai.com", description="Site URL"),
        user_agent: Union[str, None] = Query(default="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36", description="User Agent"),
        capi_version: Union[str, None] = Query(default="1.5.5", description="CAPI Version"),
        proxy: Union[str, None] = Query(default=None, description="A proxy to fetch the token, usually not required"),
):

    response = await funcaptcha(public_key=public_key, service_url=service_url, site_url=site_url, user_agent=user_agent,
                              capi_version=capi_version, proxy=proxy, ).get_token()

    return JSONResponse(content=json.loads(response))
