import requests
import json

ck = {'Authentication': f'Token:{token}'}
resp = requests.get('https://xkcd.com/info.0.json', ck)
if resp.status_code == 200:
    test = json.loads(resp.content)
    print(test['year'])
