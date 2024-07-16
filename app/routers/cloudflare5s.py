from fastapi import APIRouter
from fastapi import BackgroundTasks

from app.schemas.cloudflare5s import CloudFlare5sQuerySchema
from app.servers.cloudflare5s import Cloudflare5sBypass
from app.servers.cloudflare5s_screenshot import Cloudflare5sScreenshotBypass
from app.utils.decorator import cache_route

router = APIRouter(tags=["cloudflare5s"], prefix="/cloudflare5s")


@router.post("/bypass-v1", summary="cloudflare5s bypass")
@cache_route(cache_time=1800)
async def bypass(query_params: CloudFlare5sQuerySchema, background_tasks: BackgroundTasks):
    cloudflare5s = Cloudflare5sBypass(user_agent=query_params.user_agent, proxy_server=query_params.proxy_server)
    cf_cookie = await cloudflare5s.get_cf_cookie(str(query_params.url))
    return cf_cookie


@router.post("/bypass-v2", summary="cloudflare5s screenshot bypass")
@cache_route(cache_time=1800)
async def bypass_v2(query_params: CloudFlare5sQuerySchema, background_tasks: BackgroundTasks):
    url = str(query_params.url)
    cloudflare5s = Cloudflare5sScreenshotBypass(user_agent=query_params.user_agent,
                                                proxy_server=query_params.proxy_server)
    cf_cookie = await cloudflare5s.get_cf_cookie(url)
    return cf_cookie
