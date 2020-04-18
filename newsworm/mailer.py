import datetime
import os
import smtplib
import ssl

from collections import Counter

import fire
import yaml
import ujson as json



API_KEY = os.environ.get('NEWSAPI_KEY')


class NewsMailer(object):
    def send_mails(self, config, store, date=None, top_list=10):
        news_bucket = self._get_top_articles(config, store, date, top_list)

    def _get_top_articles(self, config, store, date=None, top_list=10):
        config = yaml.load(open(config), Loader=yaml.FullLoader)
        # TODO: refactor this to yesterday after dev
        if date is None:
            date = "2020-04-18"

        store_path = "{}/{}".format(store, date)
        files = os.listdir(store_path)

        news_bucket = {}

        for key, conf in config.items():
            news_bucket = {}
            news_files = [
                "{}/{}".format(store_path, f)
                for f in (os.listdir(store_path))
                if f.startswith("{}-".format(key))
            ]

            articles_pool = {}
            article_urls = []

            for nf in news_files:
                nf_articles = json.load(open(nf))['articles']
                for article in nf_articles:
                    articles_pool[article['url']] = article
                article_urls.extend([n['url'] for n in nf_articles])

            top_article_urls = {i[0] for i in Counter(article_urls).most_common(top_list)}
            top_articles = [articles_pool[url] for url in top_article_urls]

            news_bucket[conf['title']] = top_articles

            print ("")
            print (conf['title'])
            print("=============")
            for t in top_articles:
                print (t['title'])
                print (t['description'])
                print (t['url'])
                print ('---------------')
        return news_bucket

if __name__ == '__main__':
  fire.Fire(NewsMailer)
