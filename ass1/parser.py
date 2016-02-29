import datetime

# support for format dd/mm/yy and dd/mm/yyyy
def decodeDate(d):
	if (len(d) == 10):
		return datetime.datetime.strptime(d, "%d/%m/%Y").date()
	elif (len(d) == 8):
		return datetime.datetime.strptime(d, "%d/%m/%y").date()
	else:
		print("Unable to decode the date format : ", d)
		raise Exception


# support for format hh:mm:ss
def decodeTime(t):
	if (len(t) == 8):
		return datetime.datetime.strptime(t, "%H:%M:%S").time()
	else:
		print("Unable to decode the time format : ", t)
		raise Exception




from table import Table, Relation, types


# finds duplication in the primary key
def verifyTable(table):
	if (table.primary_attr == 0):
		return True
	elif (len(table.dict[table.primary_attr]) == len(set(table.dict[table.primary_attr])) ):
		return True
	else:
		print("Duplication in Primary key in table : ",table.name)
		return False



# checks whether foreign key is a subset of the primary key
def verifyRelation(tables,rel):
		attr1_vals = 0
		attr2_vals = 0
		for t in tables:
			if (t.name == rel.dict["t1"]):
				if (t.primary_attr[0] == rel.dict["pk"]):
					attr1_vals = t.dict[t.primary_attr]
				else:
					print("Attribute defined as primary key is not the primary key of the table")
					return False
			elif (t.name == rel.dict["t2"]):
				for key in t.dict.keys():
					if (key[0] == rel.dict["fk"]):
						attr2_vals = t.dict[key]

		if (attr1_vals == 0 or attr2_vals == 0):
			print("Unable to verify the relation - ", rel.dict)
			return False

		# Check whether foreign key is subset of primary key
		for x in attr2_vals:
			if (x not in attr1_vals):
				print("Foreign Key is not a subset of Primary Key...")
				return False

		return True


def parser(f,fout):
	tables = [] 
	relations = [] 
	
	# parse tables
	num_tables = int(f.readline())
	for i in range(num_tables):
		table_name = f.readline().strip('\n')
		tables.append(Table(table_name))
		
		# parse table attributes
		num_attr = int(f.readline())
		for j in range(num_attr):
			temp = f.readline().split(",")
			assert (len(temp) == 3) , "Length of Attribute tuple is not equal to 3"
			attr_name = temp[0].strip('() \n')
			attr_type = temp[1].strip('() \n')
			attr_isKey = int(temp[2].strip('() \n'))
			assert (attr_isKey == 1 or attr_isKey == 0) , "isKey is neither 0 nor 1"

			# check if type is defined
			if (attr_type not in types.keys()):
				print("Undefined Type : ", attr_type)
				raise Exception
			else:
				attr_type = types[attr_type]

			# check if only one primary key is defined
			if (attr_isKey==1):
				if (tables[-1].primary_attr != 0):
					print("Multiple Primary Keys defined in table : ", table_name)
					tables[-1].isValid = 0
					continue
				else:
					tables[-1].primary_attr = (attr_name, attr_type, attr_isKey)

			tables[-1].addAttribute((attr_name, attr_type, attr_isKey))

		# parse table records
		num_record = int(f.readline())
		for j in range(num_record):
			temp = f.readline().split(",")
			
			# check if elements in record is same as number of attributes
			assert (len(temp) == num_attr) , "Number of elements in records is more than number of attributes"

			for k in range(num_attr):
				temp[k] = temp[k].strip('() \n')

			tables[-1].addRecord(temp)

		# if the table is valid, then print it
		if (not verifyTable(tables[-1])):
			tables[-1].isValid = 0

	# parse relations
	num_relations = int(f.readline())
	for i in range(num_relations):
		rel = f.readline().split(",")
		assert (len(rel) == 4) , "More than 4 element found in relation..."
		for j in range(len(rel)):
			rel[j] = rel[j].strip('() \n')
		relations.append(Relation(rel))

		# check if the relation is invalid
		if (not verifyRelation(tables,relations[-1])):
			for t in tables:
				if (t.name == relations[-1].dict["t1"] or t.name == relations[-1].dict["t2"]):
					t.isValid = 0

		# check whether any of the table in the relation is invalid
		for t in tables:
			if (t.name == relations[-1].dict["t1"] and t.isValid == 0):
				for x in tables:
					if (x.name == relations[-1].dict["t2"]):
						x.isValid = 0
			if (t.name == relations[-1].dict["t2"] and t.isValid == 0):
				for x in tables:
					if (x.name == relations[-1].dict["t1"]):
						x.isValid = 0

	return tables