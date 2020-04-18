import datetime
import os
import time

import fire
import yaml
import ujson as json

from newsapi import NewsApiClient

API_KEY = os.environ.get('NEWSAPI_KEY')

class NewsCrawler(object):
    def get_news(self, config, store):
        print(config)
        now = datetime.datetime.now()
        config = yaml.load(open(config), Loader=yaml.FullLoader)
        newsapi = NewsApiClient(api_key=API_KEY)

        for key, conf in config.items():
            params = { k: v for k, v in conf.items() if k not in ['method', 'title']}
            func = getattr(newsapi, conf['method'])
            data = func(**params)
            date = now.date().isoformat()
            timestamp = int(time.time())
            store_path = "{}/{}".format(store, date)
            try:
                os.makedirs(store_path)
            except Exception:
                pass
            fname = "{}/{}-{}.json".format(store_path, key, timestamp)
            with open(fname, "w", encoding="utf8") as file:
                json.dump(data, file)


if __name__ == '__main__':
  fire.Fire(NewsCrawler)
