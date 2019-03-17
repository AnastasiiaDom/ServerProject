import re
from urllib.parse import urlparse, parse_qs
from views import LoginView, ScoreView, HighscorelView

class Urls(object):

    def __init__(self):
        urls = [
            ('^/(?P<userId>\d+)/login/?$', LoginView),
            ('^/(?P<levelId>\d+)/score/?$', ScoreView),
            ('^/(?P<levelId>\d+)/highscorelist/?$', HighscorelView)
        ]
        self.urls = [(re.compile(url), klass) for url, klass in urls]

    def matchView(self, url):
        parsed = urlparse(url)

        for regex, klass in self.urls:
            res = regex.match(parsed.path)
            if res:
                kwargs = res.groupdict()
                kwargs['params'] = parse_qs(parsed.query)

                return klass(**kwargs)

        return None