import asyncio

from DrissionPage import ChromiumPage, ChromiumOptions

from app.const import DefaultUserAgent
from app.const import IS_LINUX


class Cloudflare5sBypass(object):
    driver = None

    def __init__(self, user_agent=None, proxy_server=None):
        browser_path = "/usr/bin/google-chrome"
        options = ChromiumOptions()
        options.set_paths(browser_path=browser_path)
        user_agent = user_agent or DefaultUserAgent
        if user_agent:
            options.set_user_agent(user_agent)
        arguments = [
            "-no-first-run",
            "-force-color-profile=srgb",
            "-metrics-recording-only",
            "-password-store=basic",
            "-use-mock-keychain",
            "-export-tagged-pdf",
            "-no-default-browser-check",
            "-disable-background-mode",
            "-enable-features=NetworkService,NetworkServiceInProcess,LoadCryptoTokenExtension,PermuteTLSExtensions",
            "-disable-features=FlashDeprecationWarning,EnablePasswordsAccountStorage",
            "-deny-permission-prompts",
            "-disable-gpu",
            "-accept-lang=en-US",
        ]

        if IS_LINUX:
            options.headless(True)
            arguments.append("--no-sandbox")

        if proxy_server:
            options.set_proxy(proxy_server)

        for argument in arguments:
            options.set_argument(argument)

        self.driver = ChromiumPage(addr_or_opts=options)

    async def bypass(self):
        print(self.tag.cookies())
        ele_flag = ".spacer"
        if self.tag.wait.ele_displayed(ele_flag, timeout=1.5):
            verify_element = self.tag.ele(ele_flag, timeout=2.5)
            if verify_element:
                verify_element.click()
                await asyncio.sleep(5)

        for line in self.tag.cookies():
            if line["name"] == "cf_clearance":
                return self.tag.cookies()

    async def get_cf_cookie(self, url):
        self.driver.set.cookies.clear()
        tab_id = self.driver.new_tab(url).tab_id
        self.tag = self.driver.get_tab(tab_id)

        print(self.tag.user_agent)
        await asyncio.sleep(10)
        cookies = None
        for _ in range(10):
            print("Verification page detected.  ", self.tag.title)
            cookies = await self.bypass()

            if cookies:
                break
            await asyncio.sleep(3)

        result = {"user_agent": self.tag.user_agent, "cookies": cookies}
        self.tag.close()
        return result if cookies else None
