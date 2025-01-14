import asyncio
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))


from app.servers.cloudflare5s_screenshot import Cloudflare5sScreenshotBypass

# from
url = "https://nopecha.com/demo/cloudflare"
# url = 'https://chatgpt.com'
proxy_server = None
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15"
os.system("rm -rf images/*")

cloudflare5s = Cloudflare5sScreenshotBypass(user_agent, proxy_server)
cf_cookie = asyncio.run(cloudflare5s.get_cf_cookie(url, debug=True))
print("cf_cookie", cf_cookie)
cloudflare5s.driver.quit()
