import requests
import constants
import lxml.html
import requests


class TokenService:
    def _logIn(self):
        login = 'staz12345@list.ru'
        password = 'annaisthebest29'
        url = 'https://vk.com/'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ru-ru,ru;q=0.8,en-us;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'DNT': '1'
        }
        session = requests.session()
        data = session.get(url, headers=headers)
        page = lxml.html.fromstring(data.content)

        form = page.forms[0]
        form.fields['email'] = login
        form.fields['pass'] = password

        response = session.post(form.action, data=form.form_values())
        return 'onLoginDone' in response.text

    def getToken(self):
        if self._logIn():
            url = 'https://oauth.vk.com/authorize'
            params = {
                'client_id': 7527111,
                'display': 'page',
                'redirect_uri': 'http://api.vk.com/blank.html',
                'scope': 'wall,photos',
                'response_type': 'code',
                'v': constants.VK_VERSION,
            }

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'ru-ru,ru;q=0.8,en-us;q=0.5,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'DNT': '1'
            }

            res = requests.get(url, params=params, headers=headers)
            page = lxml.html.fromstring(res.content)

            login = 'staz12345@list.ru'
            password = 'annaisthebest29'

            session = requests.session()

            form = page.forms[0]
            form.fields['email'] = login
            form.fields['pass'] = password
            response = session.post(form.action, data=form.form_values(), headers=headers)

            return response.text
            # https: // oauth.vk.com / authorize?client_id = 1 & display = page & redirect_uri = http: // example.com / callback & scope = friends & response_type = code & v = 5.120
