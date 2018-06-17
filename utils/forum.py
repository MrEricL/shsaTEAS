from db_builder import *
def categoryTableBuilder(data):
	ret = '<table class="table table-hover" ><tr> <th align="left">Forum Category</th> <th align="left"> Forum Description  </th> 	</tr>'
	for each in data:
		link = '<a href = "forumconfig?category={}">{}</a>'.format(each['id'], each['name'])
		ret += '<tr><td>{}</td><td>{}</td><tr>'.format(link, each['desc'])

	ret += '</table>'

	return ret


def topicTableBuilder(data, category):
	ret = '<table class="table table-hover"><col width="80"><col width="800"> <tr> <th align="left"> Author </th> <th align="left"> Title </th> 	</tr>'

	for each in data:

		username = getUserName(each['userID'])

		link = '<a href = "forumconfig?category={}&topic={}">{}</a>'.format(category, each['topicID'], each['title'])

		ret += '<tr><td>{}</td><td>{}</td><tr>'.format(username,link)

	ret += "</table>"
	return ret

def postTableBuilder(data):
	ret = '<table class="table table-hover"> <col width="80"><col width="800"> <tr> <th align="left"> Post </th> <th align="left"> Author </th> 	</tr>'

	for each in data:

		username = getUserName(each['userID'])

		ret += '<tr><td>{}</td><td>{}</td><tr>'.format(username, each['body'])

	ret += "</table>"
	return ret	