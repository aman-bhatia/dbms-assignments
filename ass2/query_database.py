import pickle
import sys
from utils import *


if (len(sys.argv) != 2):
	print("Usage : python3 query_database.py <query_filename>",)
	exit()


database_file = './data/database.pkl'
query_file = sys.argv[1]
output_file = sys.argv[1] + ' - output.txt'

f = open(query_file)
query = f.readline()
f.close()

picklefile = open(database_file,'rb')
tables = pickle.load(picklefile)
picklefile.close()


# across table queries must be specified as t1.att = t2.att
def processSubquery(subq):
	subq = subq.strip('( )')
	subq = subq.split()
	assert(subq[0].lower() == 'select')
	att_list = subq[1].split(',')
	table_list = subq[2].split(',')
	cond_list = subq[3].split(',')

	cond_left = []
	cond_mid = []
	cond_right = []

	# print('a')
	
	for cond in cond_list:
		if ('=' in cond):
			temp = cond.split('=')
			cond_left.append(temp[0])
			cond_right.append(temp[1])
			cond_mid.append('=')
		elif ('<' in cond):
			temp = cond.split('<')
			cond_left.append(temp[0])
			cond_right.append(temp[1])
			cond_mid.append('<')
		elif ('>' in cond):
			temp = cond.split('>')
			cond_left.append(temp[0])
			cond_right.append(temp[1])
			cond_mid.append('>')
			
	new_tables = []

	# print('b')

	for tab in table_list:
		t = tables[tab]
		t_att_list = t.attributes
		t_cond_list = []

		# get conditions related to this table only
		for i in range(len(cond_left)):
			if ((tab+'.') in cond_left[i] and '.' not in cond_right[i]):
				t_cond_list.append(cond_left[i].split('.')[1] + cond_mid[i] + cond_right[i])
		
		# print(tab,t_att_list, t_cond_list)
		t_recs = t.getRecordsWithConditions(t_cond_list)
		# print(t_recs)
		new_tables.append(makeTable(tab,[tab+'.'+att for att in t_att_list],t_recs))

	# print('c')

	def getTableCorrespondingToName(x):
		for nt in new_tables:
			temp = nt.name.split(',')
			if (x in temp):
				return nt

	# print('d')


	# verify a across table condition
	for i in range(len(cond_left)):
		if ('.' in cond_left[i] and '.' in cond_right[i]):		
			att_t1 = []
			att_t2 = []

			att_t1.append(cond_left[i])
			att_t2.append(cond_right[i])

			t1_name = cond_left[i].split('.')[0]
			t2_name = cond_right[i].split('.')[0]

			t1 = getTableCorrespondingToName(t1_name)
			t2 = getTableCorrespondingToName(t2_name)

			jt = joinTables(t1,t2,att_t1,att_t2)

			new_tables.remove(t1)
			new_tables.remove(t2)

			new_tables.append(jt)

	# print('e')

	ret = Table_helper("Return Table")
	for att in att_list:
		ret.dict[att] = new_tables[0].dict[att]
		ret.num_attr += 1
	ret.num_record = len(ret.dict[att_list[0]])
	
	return ret


q = query.split()
keyword = q[0].lower()
result = None

if (keyword == 'insert'):
	table_name = q[1]
	att_list = q[2].split(',')
	val_list = q[3].split(',')
	result = tables[table_name]
	attrs = result.attributes
	record = ['*' for x in attrs]
	for attr in attrs:
		if (attr in att_list):
			record[attrs.index(attr)] = val_list[att_list.index(attr)]
	record[0] = int(record[0])
	result.addRecord(record)

elif (keyword == 'delete'):
	table_name = q[1]
	cond_list = q[2].split(',')
	result = tables[table_name]
	to_delete = result.getRecordsWithConditions(cond_list)

	for td in to_delete:
		result.deleteRecord(td[0])

elif (keyword == 'update'):
	table_name = q[1]
	cond_list = q[2].split(',')
	set_val = q[3].split('=')
	result = tables[table_name]
	to_modify = result.getRecordsWithConditions(cond_list)

	for tm in to_modify:
		tm[result.attributes.index(set_val[0])] = set_val[1]
		result.updateRecord(tm)

elif (keyword == 'project'):
	subquery = query[7:].strip('( )\n')
	
	if ('UNION' in subquery):
		subquery = subquery.split('UNION')
		result = setOperation(processSubquery(subquery[0]),processSubquery(subquery[1]),'union')
	elif ('INTERSECTION' in subquery):
		subquery = subquery.split('INTERSECTION')
		result = setOperation(processSubquery(subquery[0]),processSubquery(subquery[1]),'intersection')
	elif ('DIFFERENCE' in subquery):
		subquery = subquery.split('DIFFERENCE')
		result = setOperation(processSubquery(subquery[0]),processSubquery(subquery[1]),'difference')
	else:
		result = processSubquery(subquery)

		
fout = open(output_file,'w')
result.printTable(fout)
