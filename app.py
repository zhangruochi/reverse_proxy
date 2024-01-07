from flask import Flask, request, Response, redirect, url_for
import requests

app = Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    # 目标 URL，这里替换为你想要代理的网站的地址
    target_url = f'http://82.156.69.32:5000/{path}'

    # 将原始请求的方法、数据和头部转发到目标 URL
    resp = requests.request(
        method=request.method,
        url=target_url,
        headers={key: value for key, value in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)

    # 将从目标 URL 获取的响应返回给客户端
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    response = Response(resp.content, resp.status_code, headers)
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
