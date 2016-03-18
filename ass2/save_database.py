from parser import parser
from table import Table
import pickle
import sys


if (len(sys.argv) != 2):
	print("Usage : python3 save_database.py <input_filename>",)
	exit()


database_file = './data/database.pkl'
input_file = sys.argv[1]
# output_file = input_file + " - output.txt"

f = open(input_file)
# fout = open(output_file,'w')

try:
	tables = parser(f)
except:
	print(str(sys.exc_info()[0]).strip('class< >'), "occured while parsing \n ---- ", sys.exc_info()[1])
	print("Exitting Program Execution...")
	# fout.write("Invalid\n")
	exit()


picklefile = open(database_file,'wb')
pickle.dump(tables,picklefile)
picklefile.close()
