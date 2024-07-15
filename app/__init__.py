from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.responses import JSONResponse

from app.const import DefaultUserAgent, IS_LINUX
from app.extensions.display import start_xvfb_display
from app.routers import cloudflare5s, index

app = FastAPI()
app.include_router(index.router)
app.include_router(cloudflare5s.router)
if IS_LINUX:
    start_xvfb_display()


# 自定义返回验证错误的异常处理器
@app.exception_handler(ResponseValidationError)
async def rep_validation_exception_handler(reponse: Response, exc: ResponseValidationError):
    if not isinstance(exc.errors(), list):
        return JSONResponse(
            status_code=422,
            content=exc.errors(),
        )

    err_list = []
    for line in exc.errors():
        print(line)
        err_list.append("[{}] {}".format(line["loc"][-1], line["msg"]))
    return JSONResponse(
        status_code=422,
        content={"message": err_list},
    )


@app.exception_handler(RequestValidationError)
async def req_validation_exception_handler(request: Request, exc: RequestValidationError):
    if not isinstance(exc.errors(), list):
        return JSONResponse(
            status_code=422,
            content=exc.errors(),
        )

    err_list = []
    for line in exc.errors():
        print(line)
        err_list.append("[{}] {}".format(line["loc"][-1], line["msg"]))
    return JSONResponse(
        status_code=422,
        content={"message": err_list},
    )
