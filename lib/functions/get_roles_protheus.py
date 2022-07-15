import json
import requests
import browser_cookie3

from lib.functions.get_config import get_config


def get_protheus_role(issuekey: str) -> dict:
    """
    Get the roles from protheus, delivers a payload like: values: [{}]
    :return:
    """

    # Get the cookies from your chrome
    cookies = browser_cookie3.chrome(domain_name="e-core.com")

    def auth():
        cfg = get_config()
        return cfg['username'], cfg['password']

    url = f"https://jira.e-core.com/rest/scriptrunner/latest/custom/protheusRoleConsultCached?issueKey={issuekey}"
    roles = requests.get(url, cookies=cookies, auth=auth())

    try:
        roles_as_json = json.loads(roles.text.replace("null ( ", "").replace(" )", ""))
        print("roles", roles_as_json)
        return roles_as_json

    except:
        return {}
