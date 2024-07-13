import asyncio

from DrissionPage import ChromiumPage, ChromiumOptions

from app.const import DefaultUserAgent


class Cloudflare5sBypass(object):
    driver = None

    def __init__(self, user_agent=DefaultUserAgent, proxy_server=None):
        browser_path = "/usr/bin/google-chrome"
        options = ChromiumOptions()
        options.set_paths(browser_path=browser_path)
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
            "--no-sandbox",
        ]
        for argument in arguments:
            options.set_argument(argument)
        options.headless(True)
        if proxy_server:
            options.set_proxy(proxy_server)

        options.set_user_agent(user_agent=user_agent)
        self.driver = ChromiumPage(addr_or_opts=options)

    async def get_cf_cookie(self, url):
        self.driver.set.cookies.clear()
        self.driver.get(url)
        print(self.driver.user_agent)
        await asyncio.sleep(10)
        for _ in range(10):
            print("Verification page detected.  ", self.driver.title)
            print(self.driver.cookies())
            await asyncio.sleep(1)
            ele_flag = "#turnstile-wrapper"
            if self.driver.wait.ele_displayed(ele_flag, timeout=1.5):
                verify_element = self.driver.ele(ele_flag, timeout=2.5)
                if verify_element:
                    verify_element.click()
                    await asyncio.sleep(10)

            for line in self.driver.cookies():
                if line["name"] == "cf_clearance":
                    result = {"user_agent": self.driver.user_agent, "cookies": self.driver.cookies()}
                    self.driver.close()
                    return result

        self.driver.close()
