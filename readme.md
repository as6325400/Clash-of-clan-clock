# Usage

```
docker compose up -d
```

```
cp example.env .env
```

填寫好整個 .env 的資料，資料庫位置看部署在哪邊可以自己改，API的話請自行去 coc 的官網以及 line 那邊申請

使用 poetry 管理虛擬環境

```
poetry install
```

```
poetry shell
```

```
alembic upgrade head
```

```
ngrok http 127.0.0.1:5000
```
也可以用其他習慣的內網穿透服務，或者不用也行

最終
```=python
python3 app.py
```
啟動