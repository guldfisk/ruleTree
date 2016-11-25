import sys
sys.path.append('c:\\Projeter\\farligfarligslange\\roman')
import roman
import re

alph = 'abcdefghijkmnpqrstuvwxyz'

romanWriter = roman.RomanWriter()

def empty(n, s):
	return ''

def title(n, s):
	return str(n+1)
	
def subtitle(n, s, min=2):
	ss = str(n+1)
	ss = max(2-len(ss), 0)*'0'+ss
	return s+ss
	
def subelement(n, s):
	return s+'.'+str(n+1)
	
def alphabetlist(n, s):
	if n<len(alph): return s+alph[n]
	return s+'_'+str(n+1)
	
def romanlist(n, s):
	return s+'.'+romanWriter.get(n+1)

class Element:
	def __init__(self, head='', content='', label='', seperator='. '):
		self.head = head
		self.content = content
		self.label = label
		self.seperator = seperator
	def get(self):
		return self.head+self.seperator+self.content
		
class ElementLst(list):
	def dumps(self, seperator='\n\n'):
		def r(m):
			if m.groups(0)[0] in list(labelDict): return labelDict[m.groups(0)[0]]
			return 'UNKNOWNREF'
		def r2(m):
			return m.groups()[0]
		labelDict = {o.label: o.head for o in self if o.label}
		for ele in self: ele.content = re.sub('\\\\([<|>])', r2, re.sub('\\\\ref:(\w+)', r, ele.content))
		return ''.join([ele.get()+seperator for ele in self])
	
class Tree:
	def __init__(self, content='', label='', seperator='. '):
		self.content = content
		self.label = label
		self.seperator = seperator
		self.branches = []
		self.style = [empty, title, subtitle, subelement, alphabetlist, romanlist]
	def getStyle(self, level):
		if level<len(self.style): return self.style[level]
		return self.style[-1]
	def addBranch(self, branch):
		self.branches.append(branch)
	def get(self, level=0, position=0, baseStyle=''):
		s = self.getStyle(level)(position, baseStyle)
		c = [Element(s, self.content, self.label, self.seperator)]
		for i in range(len(self.branches)): c.extend(self.branches[i].get(level+1, i, s))
		return ElementLst(c)
	def dumps(self, level=0, position=0, baseStyle=0):
		return self.get(level, position, baseStyle).dumps()
	def dump(self, file, level=0, position=0, baseStyle=0):
		file.write(self.dumps(level, position, baseStyle))
		
if __name__=='__main__':
	t1 = Tree('wauw')
	for i in range(10): t1.addBranch(Tree('damn'))
	f1 = Tree('gdamn', 'her')
	g1 = Tree('boom\\ref:her')
	h1 = Tree('', seperator='')

	h1.addBranch(g1)
	g1.addBranch(f1)
	f1.addBranch(t1)

	es = h1.get()
	print(es.dumps())