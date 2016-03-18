from collections import OrderedDict
import numpy as np


class Table_helper(object):
	def __init__(self, _name):
		self.name = _name
		self.dict = OrderedDict()
		self.num_attr = 0
		self.num_record = 0

	def addAttribute(self, attr):
		self.dict[attr] = []
		self.num_attr += 1

	def addRecord(self, record):
		self.num_record += 1
		i=0
		for key in self.dict.keys():
			self.dict[key].append(record[i])
			i+=1

	def printTable(self,fout=None):
		print("#",self.num_attr,file=fout)
		print(*self.dict.keys(),sep=',',file=fout)

		rec_list = []
		for i in range(self.num_record):
			rec = ()
			for key in self.dict.keys():
				rec += (self.dict[key][i],)
			rec_list.append(rec)
		
		rec_list = set(rec_list)

		print("#",len(rec_list),file=fout)
		for rec in rec_list:
			print(*rec,sep=',',file=fout)		
		print("$",file=fout)

def makeTable(name,atts,recs):
	t = Table_helper(name)
	
	for att in atts:
		t.addAttribute(att)

	for rec in recs:
		t.addRecord(rec)

	for key in t.dict.keys():
		t.dict[key] = np.array(t.dict[key])

	return t

# given two lists, returns there intersection
def intersection(x,y):
	# one way
	# temp = []
	# for a in x:
	# 	if (a in y):
	# 		temp.append(a)
	# # other way
	# temp2 = []
	# for a in y:
	# 	if (a in x):
	# 		temp2.append(a)

	# if (len(temp) >= len(temp2)):
	# 	return temp
	# else:
	# 	return temp2

	#new code
	tempx = [tuple(a) for a in x]
	tempy = [tuple(a) for a in y]
	temp = set(tempx).intersection(set(tempy))
	return [list(a) for a in temp]


# return joint table of t1 and t2 
def joinTables(t1,t2,att_t1,att_t2):

	# print(1)
	rec_att_t1 = []		# record corresponding to att_t1
	rec_att_t2 = []		# record corresponding to att_t2
	# print(2)

	for i in range(t1.num_record):
		rec1 = []
		for att in att_t1:
			rec1.append(t1.dict[att][i])
		rec_att_t1.append(rec1)
	# print(3)

	for i in range(t2.num_record):
		rec2 = []
		for att in att_t2:
			rec2.append(t2.dict[att][i])
		rec_att_t2.append(rec2)
	# print(4)

	common_records = intersection(rec_att_t1, rec_att_t2)
	# print(5)

	# only keep common_records in t1
	i=0
	while (i<t1.num_record):
		rec = []
		for att in att_t1:
			rec.append(t1.dict[att][i])

		if (rec not in common_records):
			for key in t1.dict.keys():
				t1.dict[key] = np.delete(t1.dict[key],i)
			t1.num_record -= 1
			i -= 1
		i+=1
	# print(6)

	# make a new table with all the necessary attributes
	t = Table_helper(t1.name+','+t2.name)
	for key in t1.dict.keys():
		t.dict[key] = []
		t.num_attr += 1
	for key in t2.dict.keys():
		t.dict[key] = []
		t.num_attr += 1
	# print(7)

	# new code
	templist1=[]
	for att in att_t1:
		templist1.append(t1.dict[att])

	templist2=[]
	for att in att_t2:
		templist2.append(t2.dict[att])

	tempzip1 = np.array([hash(x) for x in zip(*templist1)])
	tempzip2 = np.array([hash(x) for x in zip(*templist2)])

	for i in range(t1.num_record):
		value = tempzip1[i]
		indarray = np.where(tempzip2==value)[0]
		for j in indarray:
			for key in t1.dict.keys():
				t.dict[key].append(t1.dict[key][i])
			for key in t2.dict.keys():
				t.dict[key].append(t2.dict[key][j])
			t.num_record += 1

	# # add records to those attributes
	# for i in range(t1.num_record):
	# 	rec_comm1 = []
	# 	for att in att_t1:
	# 		rec_comm1.append(t1.dict[att][i])
	# 	for j in range(t2.num_record):
	# 		rec_comm2 = []
	# 		for att in att_t2:
	# 			rec_comm2.append(t2.dict[att][j])
	# 		if (rec_comm1 == rec_comm2):
	# 			for key in t1.dict.keys():
	# 				t.dict[key].append(t1.dict[key][i])
	# 			for key in t2.dict.keys():
	# 				t.dict[key].append(t2.dict[key][j])
	# 			t.num_record += 1
	# print(8)

	return t


def setOperation(t1,t2,mode):
	att_list1 = t1.dict.keys()
	att_list2 = t2.dict.keys()
	assert (att_list1==att_list2)

	rec_list1 = []
	for i in range(t1.num_record):
		rec = ()
		for key in att_list1:
			rec += (t1.dict[key][i],)
		rec_list1.append(rec)
	

	rec_list2 = []
	for i in range(t2.num_record):
		rec = ()
		for key in att_list1:
			rec += (t2.dict[key][i],)
		rec_list2.append(rec)

	rec_list1 = set(rec_list1)
	rec_list2 = set(rec_list2)

	if (mode=='union'):
		return makeTable("Union",att_list1,rec_list1.union(rec_list2))
	elif (mode=='intersection'):
		return makeTable("Intersection",att_list1,rec_list1.intersection(rec_list2))
	elif (mode=='difference'):
		return makeTable("Difference",att_list1,rec_list1.difference(rec_list2))
	else:
		print('invalid mode')
		exit()



