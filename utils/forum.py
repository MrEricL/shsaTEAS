def categoryTableBuilder(data):
	ret = '<table><tr> <th>Forum Category</th> <th> Forum Description  </th> 	</tr>'
	for each in data:
		link = '<a href = "forumconfig?category={}">{}</a>'.format(each['id'], each['name'])
		ret += '<tr><td>{}</td><td>{}</td><tr>'.format(link, each['desc'])

	ret += '</table>'

	return ret