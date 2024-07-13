import asyncio
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))


from app.servers.cloudflare5s_screenshot import Cloudflare5sScreenshotBypass

# from
url = "https://nopecha.com/demo/cloudflare"
# url = 'https://chatgpt.com'
proxy_server = "http://127.0.0.1:9999"
proxy_server = None
cloudflare5s = Cloudflare5sScreenshotBypass(proxy_server)
cf_cookie = asyncio.run(cloudflare5s.get_cf_cookie(url, debug=True))
print("cf_cookie", cf_cookie)
cloudflare5s.driver.quit()
