from table import Table


def parser(f):
	tables = {} 
	
	# parse tables
	num_tables = int(f.readline()[1:])
	for i in range(num_tables):
		table_name = f.readline().strip('\n')
		tables[table_name] = Table(table_name)
		
		# parse table attributes
		num_attr = int(f.readline()[1:])
		temp = f.readline().split(",")
		assert (len(temp) == num_attr) , "Number of Attribute are not equal to defined previously"
		for j in range(num_attr):
			attr_name = temp[j].strip('() \n')
			tables[table_name].addAttribute(attr_name)

		# parse table records
		num_record = int(f.readline()[1:])
		for j in range(num_record):
			temp = f.readline().split(",")
			
			# check if elements in record is same as number of attributes
			assert (len(temp) == num_attr) , "Number of elements in records are not equal to number of attributes"

			for k in range(num_attr):
				temp[k] = temp[k].strip('() \n')
				if (temp[k].isdigit()):
					temp[k] = int(temp[k])

			tables[table_name].addRecord(temp)

		# check end of table
		assert (f.readline().strip('\n') == '$') , "End of table not verified"

	return tables