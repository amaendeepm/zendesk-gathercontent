# coding=utf-8

import base64
import requests
import json
import string

guser = 'GATHER_CONTENT_USER'
gApikey = 'GATHER_CONTENT_APIKEY'
zdhost = 'ZENDESK_HOST'

# GET ARTICLES LIST FROM ZENDESK (which exists in more than one language)

articleListUrl = 'https://'+zdhost+'.zendesk.com/api/v2/help_center/articles.json?per_page=100'
#TODO: Handle Paginated Responses Later

response = requests.get(articleListUrl, data={})
articlesListJson = response.json()
articles = []

for article in articlesListJson['articles']:
	articleID = article['id']
	articleName = article['title']

#Make each translation as a section in GatherContent for that article	
	articleTranslationsUrl = 'https://'+zdhost+'.zendesk.com/api/v2/help_center/articles/'+ str(articleID) +'/translations.json'
	print articleTranslationsUrl
	response = requests.get(articleTranslationsUrl, auth=('xxx', 'xxx'))
	articleTranslations = response.json()
	
	gelements = []
	gtab = []	
	
	for articleTranslation in articleTranslations['translations']:
		sectionID = articleTranslation['id']
		locale = articleTranslation['locale']
		lastUpdate = articleTranslation['updated_at']
		sectionTitle = articleTranslation['title']
		sectionContent = articleTranslation['body']
		
		# POST THIS TO GATHER CONTENT
		
		#Following documentation from https://gathercontent.com/developers/the-config-field/ Step-wise
		
		gelements = [{ "type": "text", "name": sectionTitle, "required": False, "label": sectionTitle, "value": sectionContent, "microcopy": "", "limit_type": "words", "limit": 1000, "plain_text": False }]
		
		gtab.append({"label": locale,"name": locale,"hidden": False, "elements":gelements})
		

	gdata = {"project_id":"60645", "name": articleName, "config": base64.b64encode(json.dumps(gtab))}
		
	response = requests.post('https://api.gathercontent.com/items', data=gdata, headers={"Accept": "application/vnd.gathercontent.v0.5+json"}, cookies=None, auth=(guser, gApikey))
	print response
															       



