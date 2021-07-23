## ccu-juice-webscraper

一個爬蟲程式爬取 ccu juice 網頁的題庫，並同時發送通知到 line 群組。

### Install requirements

```shell
pip install -r requirements.txt
```

### Set up environment variable

```shell
touch .env
```

```shell
# .env
POSTGRES_DB=postgres_database_name
POSTGRES_USER=postgres_user
POSTGRES_PASSWORD=postgres_password
EMAIL=ccu_juice_email
PASSWORD=ccu_juice_password
LINE_TOKEN＝line_notify_token
```

### Run the script

```shell
python3 main.py
```

