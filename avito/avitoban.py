from rotating_proxies.policy import BanDetectionPolicy

FORBIDDEN_TEXTS = [
    b'firewall-title',
    'Доступ с вашего IP-адреса временно ограничен'.encode('utf-8')
]


class AvitoPolicy(BanDetectionPolicy):
    def _html_valid(selt, response):
        for forbidden in FORBIDDEN_TEXTS:
            if forbidden in response.body:
                return False
        return True

    def response_is_ban(self, request, response):
        # use default rules, but also consider HTTP 200 responses
        # a ban if there is 'captcha' word in response body.
        ban = super(AvitoPolicy, self).response_is_ban(request, response)
        ban = ban or not self._html_valid(response)
        ban = ban or response.status == 302
        return ban

    def exception_is_ban(self, request, exception):
        # override method completely: don't take exceptions in account
        return None
