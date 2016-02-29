from collections import OrderedDict
from parser import decodeDate, decodeTime
from tabulate import tabulate
import datetime


types = { 'STRING' : str, 'BOOLEAN' : bool, 'INTEGER' : int, 'REAL' : float, 'FLOAT' : float,\
		  'DATE' : datetime.date, 'TIME' : datetime.time , 'CURRENCY' : float }


class Table(object):
	def __init__(self, _name):
		self.name = _name
		self.isValid = 1
		self.dict = OrderedDict()
		self.num_attr = 0
		self.num_record = 0
		self.primary_attr = 0

	def addAttribute(self, attr):
		self.dict[attr] = []
		self.num_attr += 1

	def addRecord(self, record):
		# print(record)
		self.num_record += 1
		i=0
		for key in self.dict.keys():
			if (key[1] == datetime.date):
				record[i] = decodeDate(record[i])
			elif (key[1] == datetime.time):
				record[i] = decodeTime(record[i])
			elif (key[1] != str):
				record[i] = eval(record[i])
			
			assert (type(record[i]) == key[1]) # , str(record[i]) + str(type(record[i])) + str(key[1])

			self.dict[key].append(record[i])
			i+=1

	def printTable(self,_file):
		l = len(self.name) + 13 + 10
		print( ("\n+" + '='*l + "+\n|     TABLE NAME : %s     |\n+" + '='*l + "+" ) % self.name, file=_file)
		if (self.isValid):
			temp_table = []
			headers = []
			for key in self.dict.keys():
				headers.append(key[0])

			for i in range(self.num_record):
				entry = []
				for key in self.dict.keys():
					entry.append(self.dict[key][i])
				temp_table.append(entry)

			print(tabulate(temp_table, headers, tablefmt="fancy_grid", numalign="center") , file=_file)
			print("\n\n", file=_file)
		else:
			print("Invalid\n\n", file=_file)



class Relation(object):
	def __init__(self, rel ):
		self.dict = { "t1" : rel[0] , "pk" : rel[1], "t2" : rel[2], "fk" : rel[3]}
