from db_builder import *
def categoryTableBuilder(data):
	ret = '<table cellpadding= "10"><tr> <th align="left">Forum Category</th> <th align="left"> Forum Description  </th> 	</tr>'
	for each in data:
		link = '<a href = "forumconfig?category={}">{}</a>'.format(each['id'], each['name'])
		ret += '<tr><td>{}</td><td>{}</td><tr>'.format(link, each['desc'])

	ret += '</table>'

	return ret


def topicTableBuilder(data, category):
	ret = '<table cellpadding= "10"> <tr> <th align="left">Title</th> <th align="left"> Author </th> 	</tr>'

	for each in data:

		username = getUserName(each['userID'])

		link = '<a href = "forumconfig?category={}&topic={}">{}</a>'.format(category, each['topicID'], each['title'])

		ret += '<tr><td>{}</td><td>{}</td><tr>'.format(link, username)

	return ret

def postTableBuilder(data):
	ret = '<table cellpadding= "10"> <tr> <th align="left"> Post </th> <th align="left"> Author </th> 	</tr>'

	for each in data:

		username = getUserName(each['userID'])

		ret += '<tr><td>{}</td><td>{}</td><tr>'.format(each['body'], username)

	return ret	