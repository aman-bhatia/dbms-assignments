from bisect import bisect
import numpy as np


'''
This is the Node class
which stores BPlusTree's Node
'''
class Node:
	def __init__(self):
		self.keys = []
		self.children = []
		self.is_leaf = True

	'''
	This function splits the node
	in two parts.

	It is called when the no. of keys in node exceeds limit.
	'''
	def splitNode(self):
		newNode = Node()
		if self.is_leaf:
			mid = len(self.keys)//2
			midKey = self.keys[mid]
			
			# Update sibling parameters
			newNode.keys = self.keys[mid:]
			newNode.children = self.children[mid:]
			
			# Update node parameters
			self.keys = self.keys[:mid]
			self.children = self.children[:mid]
		
		else:
			newNode.is_leaf = False
			mid = len(self.keys)//2
			midKey = self.keys[mid]
			
			# Update sibling parameters
			newNode.keys = self.keys[mid+1:]
			newNode.children = self.children[mid+1:]
			
			# Update node parameters
			self.keys = self.keys[:mid]
			self.children = self.children[:mid + 1]
		return midKey, newNode



'''
This is the BPlusTree class
which stores BPlusTree structure
'''
class BPlusTree:
	def __init__(self, _factor=4):
		self.root = Node()
		self.factor = _factor

	'''
	Searches in the BPlusTree with given
	key=k
	Returns node corresponding to that key and the child
	'''
	def search(self,k):
		current = self.root
		if (len(current.keys) == 0):
			return (None, None)
		while (True):
			index = bisect(current.keys,k)
			if (current.is_leaf):
				if (k == current.keys[index-1]):
					return (current,current.children[index-1])
				else:
					return (None,None)
			current = current.children[index]


	'''
	Inserts in the BPlusTree with given
	key=k, value=v
	'''
	def insert(self,k,v):
		node,val = self.search(k)
		if (node is not None and val is None):
			index = bisect(node.keys,k)
			node.children[index-1] = v
		else:
			ans, newNode = self.insert_helper(k,v,self.root)
			if ans:
				newRoot = Node()
				newRoot.is_leaf = False
				newRoot.keys = [ans]
				newRoot.children = [self.root, newNode]
				self.root = newRoot

	def insert_helper(self,k,v,node):
		if (node.is_leaf):
			index = bisect(node.keys,k)
			node.keys[index:index] = [k]
			node.children[index:index] = [v]

			if len(node.keys) <= self.factor-1:
				return None, None
			else:
				midKey, newNode = node.splitNode()
				return midKey, newNode
		else:
			if k < node.keys[0]:
				ans, newNode = self.insert_helper(k, v, node.children[0])
			elif k >= node.keys[-1]:
				ans, newNode = self.insert_helper(k, v, node.children[-1])
			else:
				for i in range(len(node.keys)-1):
					if k>=node.keys[i] and k<node.keys[i+1]:
						ans, newNode = self.insert_helper(k, v, node.children[i+1])
		if ans:
			index = bisect(node.keys, ans)
			node.keys[index:index] = [ans]
			node.children[index+1:index+1] = [newNode]
			if len(node.keys) <= self.factor-1:
				return None, None
			else:
				midKey, newNode = node.splitNode()
				return midKey, newNode
		else:
			return None, None


	'''
	Deletes in the BPlusTree with given
	key=k
	'''
	def delete(self,k):
		node,val = self.search(k)
		assert (node is not None and val is not None)
		index = bisect(node.keys,k)
		node.children[index-1] = None

	'''
	Updates in the BPlusTree with given
	key=k to value=new_v
	'''
	def update(self, k, new_v):
		node,val = self.search(k)
		assert (node is not None and val is not None)
		index = bisect(node.keys,k)
		node.children[index-1] = new_v


	def printBtree(self):
		nodes = [self.root]
		nodeskeys = [node.keys for node in nodes]
		print(nodeskeys)
		val_level = nodes[0].is_leaf
		while (not val_level):
			nodes = [node.children for node in nodes]
			nodes = [item for sublist in nodes for item in sublist]
			nodeskeys = [node.keys for node in nodes]
			print(nodeskeys)
			val_level = nodes[0].is_leaf

		vals = [node.children for node in nodes]
		print(vals)
		print("\n\n")


	def prettyPrintBtree(self,fout=None):
		nodes = [self.root]
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

		for i in range(len(nodeskeys)):
			if (vals[i] is not None):
				print(nodeskeys[i],end=',',file=fout)
				print(*vals[i],sep=',',file=fout)

		

'''

btree = BPlusTree()
btree.printBtree()

btree.insert(5,'a')
btree.printBtree()

btree.insert(3,'b')
btree.printBtree()

btree.insert(9,'c')
btree.printBtree()

btree.insert(2,'d')
btree.printBtree()

btree.insert(11,'q')
btree.printBtree()

btree.insert(12,'w')
btree.printBtree()

btree.insert(13,'e')
btree.printBtree()

btree.insert(14,'h')
btree.printBtree()

btree.insert(15,'o')
btree.printBtree()

btree.insert(16,'p')
btree.printBtree()

btree.update(13,"r")
btree.printBtree()

btree.delete(11)
btree.printBtree()

btree.insert(11,'aman')
btree.printBtree()



print(13, btree.search(13)[1])
print(2,btree.search(2)[1])
print(5,btree.search(5)[1])
print(11,btree.search(11)[1])
print(7,btree.search(7)[1])

'''