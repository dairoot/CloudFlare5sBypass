# CloudFlare 5s 盾 绕过

## 本地运行
```bash
pip install -r requirements.txt

uvicorn app:app --host=0.0.0.0 --reload
```

## docker 运行方式
```bash
# 编译镜像
docker compose build

# 国内机子，可使用下方命令编译镜像
docker build -t dairoot/cloudflare5sbypass -f Dockerfile-CN .

# 运行
docker compose up
```

## 获取 cloudflare 5s 盾 cf_clearance 值
### 接口1：POST /cloudflare5s/bypass-v1 
- 描述：此接口通过 HTML 元素定位来绕过 Cloudflare 5s 盾。
- 优点：查询结果返回速度较快。
- 缺点：由于 Cloudflare 可能会更新 HTML 元素，此接口可能会失效。
- 测试：python tests/test_v1.py
- 鸣谢：[Cloudflare 5S 绕过](https://github.com/sarperavci/CloudflareBypassForScraping)

### 接口2：POST /cloudflare5s/bypass-v2
- 描述：此接口通过图像识别定位来绕过 Cloudflare 5s 盾。
- 优点：稳定性高，适用场景广泛。
- 缺点：响应时间可能相对较长。
- 测试：python tests/test_v2.py


### 提交参数

| 字段 | 类型 | 描述                       | 举例                      |
|:---|:---|:-------------------------|-------------------------|
| url | string | 需要绕过的url  | https://chatgpt.com     |
| proxy_server | string | 代理服务器地址（不填默认为本机）         | http://12.34.56.78:7890 |

### 返回参数
| 字段         | 类型     | 描述            |
|:-----------|:-------|:--------------|
| user_agent | string | user_agent  头 |
| cookies    | dict   | 浏览器 cookie    |



## 注意事项
如果不使用代理服务器（proxy_server），则必须将该项目部署在需要绕过 Cloudflare 5s 盾的服务器上。否则，即使获取到 cf_clearance 值，也将无法适用。


## 致谢
