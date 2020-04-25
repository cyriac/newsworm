# Newsworm

Collects daily news and sends top news to your inbox every morning.


## Crons

### Collect news
```
python newsworm/get_news.py get_news ./config.yml ./data
```

- `./config.yml` - list of news types and parameters you want to pass to newsapi.org
- `./data` - local folder to store the daily news


### Send mail
```
python newsworm/mailer.py send_mails ./config.yml ./data email@example.com
```

### Create archive
```
python newsroom/mailer.py archive ./config.yml ./data
```
