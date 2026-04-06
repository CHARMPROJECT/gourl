from fastapi import FastAPI, Request, Response, status
from fastapi.responses import RedirectResponse, FileResponse, JSONResponse # Добавлены FileResponse и JSONResponse
from fastapi.staticfiles import StaticFiles # Импорт для статики
from contextlib import asynccontextmanager
from middlewares import add_middlewares
import uvicorn, sys, asyncio
from database import orm as db
from middlewares import limiter
from schemas import CreateUrlRequestSchema, CreateUrlResponseSchema

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.create_tables()
    yield

app = FastAPI(lifespan=lifespan)

add_middlewares(app)

app.mount("/static", StaticFiles(directory="static"), name="static")

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

@app.get("/")
async def read_index():
    return FileResponse("static/index.html")

@app.post('/create', response_model=CreateUrlResponseSchema)
@limiter.limit('5/minute')
async def create_url(request: Request, data: CreateUrlRequestSchema):
    url = await db.create_url(target_url=str(data.url))

    return CreateUrlResponseSchema(
        path=f'/{url.code}'
    )

@app.get('/{code}', response_class=RedirectResponse)
@limiter.limit('10/minute')
async def redirect_to_url(request: Request, code: str):
    if code == "favicon.ico":
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    url = await db.get_url_by_code(code)

    if not url:
        return JSONResponse(
            content={
                'ok': False,
                'message': 'Url not found'
            },
            status_code=status.HTTP_404_NOT_FOUND
        )

    return RedirectResponse(
        url=url.url,
        status_code=status.HTTP_301_MOVED_PERMANENTLY
    )

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0')
