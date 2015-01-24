import re

tot = 0
gobal tot
ID = dict()
Name = list()


def get_id(name):
	gobal tot
	if ID.get(name) == None:
		ID[name] = tot
		tot += 1
	Name[tot-1] = name
	return ID[name]

def get_name(id):
	return Name[id]

def is_match(name):
	pattern1 = re.compile(r'\d{4}$|\d{4}\s*:\s*\d$')
	if pattern1.search(name):
		return True
	print name,'fuck'
	return False

def deal_name(name):
	ret = name
	pattern1 = re.compile(r'\d{4}$|\d{4}\s*:\s*\d$')
	match = pattern1.search(name)
	if match:
		ret = ret[0:match.start()-1]
	ret = ret.strip()
	ret.capitalize()
	return ret



f = open("Data.in")

line = f.readline()
print line,'|'
while line:
	if is_match(line):
		line = deal_name(line)
		u = get_id(line)
		line = f.readline()
		print u
		while line != '':
			line = deal_name(line)
			v = getid(line)
			mat[u][v] += 1
			line = f.readline()
			print u,' ',v
		line = f.readline()

for [name,id] in ID:
	print 'name:',name,' id:',id







