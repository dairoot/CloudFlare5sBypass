from pydantic import Field, BaseModel, HttpUrl


class CloudFlare5sQuerySchema(BaseModel):
    url: HttpUrl = Field(..., description="cloudflare 5s url")
    # user_agent: str = Field(None, description="user_agent")
    proxy_server: str = Field(None, description="proxy server")
