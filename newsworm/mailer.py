import datetime
import os
import smtplib
import ssl

from collections import Counter
from email.mime.text import MIMEText

import fire
import yaml
import ujson as json



API_KEY = os.environ.get('NEWSAPI_KEY')


class NewsMailer(object):
    def send_mails(self, config, store, receiver_email, date=None, top_list=10):

        port = os.environ.get('SMTP_PORT', 587)  # For starttls
        smtp_server = os.environ.get('SMTP_SERVER')
        sender_email = os.environ.get('SMTP_SENDER')
        sender_login = os.environ.get('SMTP_LOGIN', sender_email)
        password = os.environ.get('SMTP_PASSWORD')

        if date is None:
            today = datetime.date.today()
            yesterday = today - datetime.timedelta(days = 1)
            date = str(yesterday)

        news_bucket = self._get_top_articles(config, store, date, top_list)

        for subject, articles in news_bucket.items():
            article_text = []
            for t in articles:
                article_text.append(t['title'])
                article_text.append('-' * len(t['title']))
                article_text.append(t['description'])
                article_text.append(t['url'])
                article_text.append("")

            article_text.append("")
            msg = MIMEText("\n".join(article_text))
            msg['Subject'] = "{} ({})".format(subject, date)
            msg['From'] = sender_email
            msg['To'] = receiver_email

            context = ssl.create_default_context()
            with smtplib.SMTP(smtp_server, port) as server:
                print ("Sending email {} to {}".format(subject, receiver_email))
                server.ehlo()
                server.starttls(context=context)
                server.ehlo()
                server.login(sender_login, password)
                server.sendmail(msg['From'], msg['To'], msg.as_string())


    def _get_top_articles(self, config, store, date, top_list=10):
        config = yaml.load(open(config), Loader=yaml.FullLoader)

        store_path = "{}/{}".format(store, date)
        files = os.listdir(store_path)

        news_bucket = {}

        for key, conf in config.items():
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

        return news_bucket

if __name__ == '__main__':
  fire.Fire(NewsMailer)
