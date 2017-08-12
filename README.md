## Python API redirector


如果你需要使用 `Vue.js` | `React.js` | `Angular.js` 等前端`MVVM`框架将他人提供的API 封装成 `SPA` （Single Page App）来方便用户使用，因为API的域名与你提供服务的域名不同，你可能会遇到跨域（CORS）的问题


本项目使用 Flask 框架搭建一个简单的后台应用，改变域名，并转发 payload，而且在转发的时候注入了部分变量，例如当前调用者的用户名（单点登录）：


https://api.xxx.com/

body:
```json
{
    "action": "ListAppName"
}
```
转发到：
https://api.yyy.com/

body:
```json
{
    "action": "ListAppName",
    "yyy_user": "kevin.gao"
}
```

来解决CORS跨域问题

## Python版本
3.6.2

## requirements.txt
```
Flask==0.12.2
requests==2.18.3
```

## 部署到生产环境
```bash
gunicorn -w 4 -b 127.0.0.1:4000 redirector:app
```

## Nginx 配置
```
  server {
    listen 80;
    server_name example.org;
    access_log  /var/log/nginx/example.log;

    location / {
        proxy_pass http://127.0.0.1:4000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-User $http_remote_user;
    }
  }
```