import requests

BACKLOG_ENDPOINT_RATELIMIT = "https://{space}.backlog.jp/api/v2/rateLimit?apiKey={api_key}"


def get_ratelimit(backlog_space_key, api_key):

    url = BACKLOG_ENDPOINT_RATELIMIT.format(
        space=backlog_space_key, api_key=api_key)
    headers = {"Content-Type": "application/json;charset=utf-8"}

    res = requests.get(url, headers=headers)

    if res.status_code != 200:
        res.raise_for_status()

    return res.json()
