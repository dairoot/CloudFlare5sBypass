import asyncio
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))

from app.servers.cloudflare5s import Cloudflare5sBypass

proxy_server = None

cloudflare5s = Cloudflare5sBypass(proxy_server)
url = "https://nopecha.com/demo/cloudflare"
# url = 'https://chatgpt.com'
cf_cookie = asyncio.run(cloudflare5s.get_cf_cookie(url))
print(cf_cookie)

cloudflare5s.driver.quit()
