import json

import browser_cookie3
import requests

from lib.functions.get_config import get_config


def log_time_on_tempo(tempo_datetime, role_id, seconds, comment, original_issue_id, event_id):
    # log_time_on_tempo("2022-06-06T09:00:00.000", 2, "200000080", 1800, "test plans timesheets", "890651")
    url = "https://jira.e-core.com/rest/tempo-timesheets/4/worklogs/"

    # Fix role id if problematic.
    role_id = "NONE" if role_id == "" else role_id

    payload = {
        "attributes": {
            "_Role_": {
                "key": "_Role_",
                "name": "Role",
                "value": str(role_id),
                "type": "DYNAMIC_DROPDOWN",
            },
            "_OnCall_": {
                "name": "On Call",
                "workAttributeId": 0,
                "value": "FALSE"
            }
        },
        "billableSeconds": "",
        "originId": -1,
        "worker": get_config()['user_key'],
        "comment": comment,
        "started": tempo_datetime,
        "timeSpentSeconds": seconds,
        "originTaskId": str(original_issue_id)
    }
    headers = {
        'accept': 'application/json, application/vnd-ms-excel',
        'content-type': 'application/json',
        'origin': 'https://jira.e-core.com',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36'
    }
    cookie = browser_cookie3.chrome(domain_name="e-core.com")
    response = requests.request("POST", url, headers=headers, cookies=cookie, data=json.dumps(payload))
    print(response.status_code, response.text)
    return response
