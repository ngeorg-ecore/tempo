import browser_cookie3
import requests

from lib.functions.get_config import get_config


def get_issues_by_jql(jql):
    cfg = get_config()

    def auth():
        return cfg['username'], cfg['password']

    cookies = browser_cookie3.chrome(domain_name=cfg['domain'])
    url = f"https://jira.e-core.com/rest/api/2/search?jql={jql}"
    response = requests.get(url, cookies=cookies, auth=auth(), headers={"Content-Type": "application/json", "accept": "*/*"})

    return response.json()




