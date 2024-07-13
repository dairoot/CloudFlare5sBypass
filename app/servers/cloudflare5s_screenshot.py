import asyncio
import os
from datetime import datetime

from DrissionPage import ChromiumOptions, ChromiumPage
from app.const import DefaultUserAgent, IS_LINUX
from app.servers import get_click_xy
from app.utils import check_path

r = 2  # 苹果分辨率需要除 2
if IS_LINUX:
    r = 1

file_path = "images"
check_path(file_path)

file_suffix = "png"


class Cloudflare5sScreenshotBypass:
    def __init__(self, proxy_server=None):
        browser_path = "/usr/bin/google-chrome"
        options = ChromiumOptions()
        options.set_paths(browser_path=browser_path)
        options.set_user_agent(DefaultUserAgent)
        arguments = [
            "--accept-lang=en-US",
            "--no-first-run",
            "--force-color-profile=srgb",
            "--metrics-recording-only",
            "--password-store=basic",
            "--use-mock-keychain",
            "--export-tagged-pdf",
            "--no-default-browser-check",
            "--enable-features=NetworkService,NetworkServiceInProcess,LoadCryptoTokenExtension,PermuteTLSExtensions",
            "--disable-gpu",
            "--disable-infobars",  # 关闭菜单栏
            "--disable-extensions",
            "--disable-popup-blocking",
            "--disable-background-mode",
            "--disable-features=FlashDeprecationWarning,EnablePasswordsAccountStorage,PrivacySandboxSettings4",
            "--deny-permission-prompts",
            "--disable-suggestions-ui",
            "--hide-crash-restore-bubble",
            "--window-size=1920,1080",
        ]
        if IS_LINUX:
            arguments.append("--start-maximized")
            arguments.append("--no-sandbox")
        else:
            pass
            arguments.append("--start-fullscreen")

        for argument in arguments:
            options.set_argument(argument)

        if proxy_server:
            print("proxy_server", proxy_server)
            options.set_proxy(proxy_server)

        options.headless(False)

        self.driver = ChromiumPage(addr_or_opts=options)
        print("self.driver.rect.page_location", self.driver.rect.page_location)

    async def bypass(self):
        import pyautogui

        print("Verification page detected.  ", self.driver.title)
        print(self.driver.cookies())
        # 截取整个屏幕的截图
        screenshot = pyautogui.screenshot()
        file_name = datetime.now().strftime("%Y%m%d.%H_%M_%S")

        screenshot_path = f"{file_path}/{file_name}.{file_suffix}"
        screenshot.save(screenshot_path)
        for click_x, click_y in get_click_xy(screenshot_path):
            pyautogui.moveTo(click_x / r, click_y / r, duration=0.5, tween=pyautogui.easeInElastic)
            pyautogui.click()
            await asyncio.sleep(5)

        for line in self.driver.cookies():
            if line["name"] == "cf_clearance":
                return {"user_agent": self.driver.user_agent, "cookies": self.driver.cookies()}

    async def get_cf_cookie(self, url, debug=False):

        self.driver.set.cookies.clear()
        self.driver.new_tab(url)
        print(self.driver.user_agent)
        cookies = None
        await asyncio.sleep(5)
        for _ in range(10):
            print("Verification page detected.  ", self.driver.title)
            cookies = await self.bypass()

            if cookies:
                break
            await asyncio.sleep(3)

        result = {"user_agent": self.driver.user_agent, "cookies": cookies}
        self.driver.close()

        if not debug:
            command = f"rm -rf {file_path}/*"
            # 执行命令
            os.system(command)

        return result
