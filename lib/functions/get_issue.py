import requests
import browser_cookie3

from lib.functions.get_config import get_config


def get_issue(key):
    cfg = get_config()

    def auth():
        return cfg['username'], cfg['password']

    cookies = browser_cookie3.chrome(domain_name=cfg['domain'])
    url = "https://jira.e-core.com/rest/api/2/issue/" + key
    response = requests.get(url, cookies=cookies, auth=auth(), headers={"Content-Type": "application/json", "accept": "*/*"})

    return response.json()


