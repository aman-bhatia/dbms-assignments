from collections import OrderedDict
from btree import BPlusTree

class Table(object):
	def __init__(self, _name):
		self.name = _name
		self.attributes = []
		self.num_records = 0
		self.tree = BPlusTree()

	def addAttribute(self, attr):
		self.attributes.append(attr)

	def addRecord(self, record):
		self.num_records += 1
		self.tree.insert(record[0],record[1:])

	def deleteRecord(self,key):
		self.num_records -= 1
		self.tree.delete(key)

	def updateRecord(self,rec):
		self.tree.update(rec[0],rec[1:])

	def printTable(self,fout=None):
		print("#",len(self.attributes),file=fout)
		print(*self.attributes,sep=',',file=fout)
		print("#",self.num_records,file=fout)
		self.tree.prettyPrintBtree(fout)
		print("$",file=fout)


	'''
	Given a condition list, this function returns
	the records satisfying those conditions
	'''
	def getRecordsWithConditions(self,cond_list):
		cond_left = []
		cond_mid = []
		cond_right = []
		for cond in cond_list:
			if ('=' in cond):
				temp = cond.split('=')
				cond_left.append(temp[0])
				cond_right.append(temp[1])
				if (temp[1].isdigit()):
					cond_mid.append(int.__eq__)
				else:
					cond_mid.append(str.__eq__)
			elif ('<' in cond):
				temp = cond.split('<')
				cond_left.append(temp[0])
				cond_right.append(temp[1])
				if (temp[1].isdigit()):
					cond_mid.append(int.__lt__)
				else:
					cond_mid.append(str.__lt__)
			elif ('>' in cond):
				temp = cond.split('>')
				cond_left.append(temp[0])
				cond_right.append(temp[1])
				if (temp[1].isdigit()):
					cond_mid.append(int.__gt__)
				else:
					cond_mid.append(str.__gt__)

		records = []

		prim_key_n_eq_in_cond_list = False

		if (self.attributes[0] in cond_left):
			temp_key = cond_left.index(self.attributes[0])
			if (cond_mid[temp_key] == int.__eq__):
				prim_key_n_eq_in_cond_list = True

		if (prim_key_n_eq_in_cond_list):
			key = int(cond_right[cond_left.index(self.attributes[0])])
			rec = self.tree.search(key)
			assert(rec[1] is not None)
			records.append([key]+rec[1])
		else:
			nodes = [self.tree.root]
			nodeskeys = [node.keys for node in nodes]
			val_level = nodes[0].is_leaf
			while (not val_level):
				nodes = [node.children for node in nodes]
				nodes = [item for sublist in nodes for item in sublist]
				nodeskeys = [node.keys for node in nodes]
				val_level = nodes[0].is_leaf

			vals = [node.children for node in nodes]
			nodeskeys = [item for sublist in nodeskeys for item in sublist]
			vals = [item for sublist in vals for item in sublist]
			for i in range(len(vals)):
				if (vals[i] is not None):
					records.append([nodeskeys[i]] + vals[i])
					

		to_ret = []

		for rec in records:
			candidate = True
			for i in range(len(cond_left)):
				if (cond_right[i].isdigit() and (not cond_mid[i](rec[self.attributes.index(cond_left[i])],int(cond_right[i])))):
					candidate = False
					break
				elif ((not cond_right[i].isdigit()) and (not cond_mid[i](rec[self.attributes.index(cond_left[i])],cond_right[i]))):
					candidate = False
					break
			if candidate:
				to_ret.append(rec)

		return to_ret