import platform

# DefaultUserAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
DefaultUserAgent = None

platform = platform.system().lower()
IS_LINUX = bool(platform == "linux")
IS_MAC = bool(platform == "darwin")
print(platform)
