import json, os, requests
from requests.auth import HTTPBasicAuth
from pprint import pprint

DIR = os.path.dirname(__file__) or '.'
DIR += '/../key.txt'

def get_apikey():
    keyfile = open(DIR, "r")
    av_key = keyfile.readline().replace("\n", "").replace("\r", "")
    return av_key

KEY = get_apikey()

def get_events():
	link = 'https://www.eventbriteapi.com/v3/events/search/?location.address={}&q={}&token={}'
	link = link.format('NewYork', 'SHSAT', str(KEY))

	r = requests.get(link) 
	data = json.loads(r.content)

	#print r.status_code

	return data
	
def table_builder(data):
	table = '<table> <tr> <th> Name </th> <th> Description </th> </tr>'
	for i in range(len(data['events'])):
		name = str(data['events'][i]['name']['text'])
		desc =  data['events'][i]['description']['text'][:350].encode('utf-8')

		if desc[-1] == "." or desc[-1] == "?" or desc[-1] == "!":
			pass
		else:
			desc+="..."

		url = str(data['events'][i]['url'])

		url = '<a href="{}">{}</a>'.format(url,name)

		table += "<tr><td>{}</td><td>{}</td></tr>".format(url, desc)
	table += '</table>'
	return table

#print table_builder(get_events())

def getData():
    data = get_events()
    events = []
    list = []
    print "GET DATA:\n"
    for i in range(len(data['events'])):
	name = str(data['events'][i]['name']['text'])
        # print "   Name:", name
	desc =  data['events'][i]['description']['text'][:350].encode('utf-8')
        # print "   Desc:", desc
        start = data['events'][i]['start']['local']
        # print "   Start:", start
        end = data['events'][i]['end']['local']
        # print "   End:", end
        list = [name, desc, start, end]
        events.append(list)
    # print events
    return events

getData()
