# coding=utf-8

import base64
import requests
import json
import string


# GET FROM ZENDESK
zdHost = 'amandeepmidha' 
articleId = 214891008


zdUrl = 'https://'+str(zdHost)+'.zendesk.com/api/v2/help_center/en-us/articles/'+str(articleId)+'.json'
response = requests.get(zdUrl, data={})
articleJson = response.json()

print articleJson

label = articleJson['article']['name']
value = articleJson['article']['body']


# POST THIS TO GATHER CONTENT

guser = 'GATHER-CONENT-USER'
gApikey = 'GATHER-CONTENT-API-KEY'

#Following documentation from https://gathercontent.com/developers/the-config-field/ Step-wise

gelements = [{ "type": "text", "name": "el1", "required": False, "label": label, "value": value, "microcopy": "", "limit_type": "words", "limit": 1000, "plain_text": False }]

gtab = [{"label": "Content","name": "Random name","hidden": False, "elements":gelements}]

gdata = {"project_id":"60645", "name": "Using Python Yet Again", "config": base64.b64encode(json.dumps(gtab))}

response = requests.post('https://api.gathercontent.com/items', data=gdata, headers={"Accept": "application/vnd.gathercontent.v0.5+json"}, cookies=None, auth=(guser, gApikey))

print response

