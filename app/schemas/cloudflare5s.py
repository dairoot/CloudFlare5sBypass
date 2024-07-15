from pydantic import Field, BaseModel, HttpUrl
from pydantic import BaseModel, field_validator, ValidationError
from typing import Any
import re
from app.const import DefaultUserAgent


class CloudFlare5sQuerySchema(BaseModel):
    url: HttpUrl = Field(..., description="cloudflare 5s url")
    user_agent: str = Field(default=DefaultUserAgent, description="user_agent")
    # proxy_server: HttpUrl = Field(None, description="proxy server")
    proxy_server: str = Field(None, description="proxy server")

    @field_validator('proxy_server')
    def validate_url(cls, v: Any) -> Any:
        # 正则表达式匹配 http:// 或 https:// 开头，后面跟域名部分，不允许有路径
        regex = re.compile(
            r'^(http://|https://)'  # http:// 或 https://
            r'(\w+\.)+\w+'  # 域名部分
            r'(:\d+)?$'  # 可选的端口部分，不允许有路径
        )
        if not regex.match(v):
            raise ValueError('Invalid URL format')
        return v
