# Usage

```
cp example.env .env
```

填寫好整個 .env 的資料，資料庫位置看部署在哪邊可以自己改，API的話請自行去 coc 的官網以及 line 那邊申請

```
docker compose up -d
```

就可以成功啟用了

因為 line 的 webhook 一定要 SSL , 所以可以考慮使用

```
ngrok http 127.0.0.1:5050
```

也可以用其他習慣的內網穿透服務，或者不用也行，反正能把這個 port expose 成 SSL 就可以了