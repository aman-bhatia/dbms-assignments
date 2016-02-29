from parser import parser
from table import Table
import sys


if (len(sys.argv) != 3):
	print("Usage : python3 main.py <inputfile_part1> <nputfile_part2>",)
	exit()
print("\n\n-------------------Part 1---------------------------------\n")

f = open(sys.argv[1])
fout = open('output1.txt','w')

try:
	tables = parser(f,fout)
except:
	print(str(sys.exc_info()[0]).strip('class< >'), "occured while parsing \n ---- ", sys.exc_info()[1])
	print("Exitting Program Execution...")
	fout.write("Invalid\n")
	exit()

for t in tables:
	t.printTable(fout)

for t in tables:
	if (not t.isValid):
		tables.remove(t)



f.close()
fout.close()


print("\n\n-------------------Part 2---------------------------------\n")

f = open(sys.argv[2])
fout = open('output2.txt','w')


# parse the queries
queries = []
num_attr = int(f.readline())
for i in range(num_attr):
	temp = f.readline().split(",")
	assert (len(temp) == 2) , "Length of Attribute tuple is not equal to 2"
	table_name = temp[0].strip('() \n')
	attr_name  = temp[1].strip('() \n')
	
	queries.append([table_name, attr_name])


# check if attr defined are in tables
for q in queries:
	tbl = 0
	for t in tables:
		if (t.name == q[0]):
			tbl = t
			break
	
	if (tbl==0):
		print("Unable to find the table : ", q[0])
		fout.write("Invalid\n")
		exit()

	q[0] = tbl
	att = 0
	for x in tbl.dict.keys():
		if (q[1] == x[0]):
			att = x
			break

	if (att==0):
		print("Unable to find the attribue : ",q[1]," in table : ", tbl.name)
		fout.write("Invalid\n")
		exit()
	q[1] = att



# make new tables of useful attributes only
subschema_tables = []
for q in queries:
	if (q[0].name in [x.name for x in subschema_tables]):
		for x in subschema_tables:
			if (x.name == q[0].name):
				x.dict[(q[1][0],q[1][1])] = q[0].dict[q[1]]
				x.num_attr += 1
				break
	else:
		t = Table(q[0].name)
		# we dont need isKey anymore
		t.dict[(q[1][0],q[1][1])] = q[0].dict[q[1]]
		t.num_attr += 1
		t.num_record = len(q[0].dict[q[1]])
		subschema_tables.append(t)



# given two lists, returns there intersection
def intersection(x,y):
	# one way
	temp = []
	for a in x:
		if (a in y):
			temp.append(a)
	# other way
	temp2 = []
	for a in y:
		if (a in x):
			temp2.append(a)

	if (len(temp) >= len(temp2)):
		return temp
	else:
		return temp2


# return joint table of t1 and t2 
def joinTables(t1,t2):
	global fout
	common_attr = intersection(t1.dict.keys(), t2.dict.keys())		# list of common attributes

	# if there are no common attributes
	if (len(common_attr) == 0):
		# just do the cartesian product
		for key in t1.dict.keys():
			for j in range(t2.num_record-1):
				for i in range(t1.num_record):
					t1.dict[key].append(t1.dict[key][i])

		
		for key in t2.dict.keys():
			t1.dict[key] = []
			t1.num_attr += 1
			for val in t2.dict[key]:
				for i in range(t1.num_record):
					t1.dict[key].append(val)

		t1.num_record *= t2.num_record
		return t1

	# there are few common attributes
	else:
		rec_common1 = []		# record corresponding to common attributes in table 1
		rec_common2 = []		# record corresponding to common attributes in table 2

		for i in range(t1.num_record):
			rec1 = []
			for att in common_attr:
				rec1.append(t1.dict[att][i])
			rec_common1.append(rec1)

		for i in range(t2.num_record):
			rec2 = []
			for att in common_attr:
				rec2.append(t2.dict[att][i])
			rec_common2.append(rec2)


		common_records = intersection(rec_common1, rec_common2)

		# only keep common_records in t1
		i=0
		while (i<t1.num_record):
			rec = []
			for att in common_attr:
				rec.append(t1.dict[att][i])

			if (rec not in common_records):
				for key in t1.dict.keys():
					del t1.dict[key][i]
				t1.num_record -= 1
				i -= 1
			i+=1

		# make a new table with all the necessary attributes
		t = Table(t1.name)
		for key in t1.dict.keys():
			t.dict[key] = []
			t.num_attr += 1
		for key in t2.dict.keys():
			t.dict[key] = []
			t.num_attr += 1

		# add records to those attributes
		for i in range(t1.num_record):
			rec_comm1 = []
			for att in common_attr:
					rec_comm1.append(t1.dict[att][i])
			for j in range(t2.num_record):
				rec_comm2 = []
				for att in common_attr:
					rec_comm2.append(t2.dict[att][j])
				if (rec_comm1 == rec_comm2):
					for key in common_attr:
						t.dict[key].append(t1.dict[key][i])
					for key in t1.dict.keys():
						if (key not in common_attr):
							t.dict[key].append(t1.dict[key][i])
					for key in t2.dict.keys():
						if (key not in common_attr):
							t.dict[key].append(t2.dict[key][j])
					t.num_record += 1

		return t

while(len(subschema_tables) != 1):
	subschema_tables[0] = joinTables(subschema_tables[0], subschema_tables[1])
	del subschema_tables[1]

subschema_tables[0].name = "Subschema Table"
subschema_tables[0].printTable(fout)
