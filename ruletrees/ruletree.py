from roman import RomanWriter
import re
import string

def empty(n, s):
	return ''

def title(n, s):
	return str(n+1)
	
def sub_title(n, s):
	ss = str(n+1)
	ss = max(2-len(ss), 0)*'0'+ss
	return s+ss
	
def sub_element(n, s):
	return s+'.'+str(n+1)
	
def alphabet_lst(n, s):
	if n<len(string.ascii_lowercase):
		return s+string.ascii_lowercase[n]
	return s+'_'+str(n+1)
	
def roman_lst(n, s):
	return s+'.'+RomanWriter.get(n+1)

class Element:
	def __init__(self, head='', content='', label='', separator='. '):
		self.head = head
		self.content = content
		self.label = label
		self.separator = separator
	def get(self):
		return self.head+self.separator + self.content
		
class ElementLst(list):
	def dumps(self, separator='\n\n'):
		def r(m):
			if m.groups(0)[0] in list(label_dict):
				return label_dict[m.groups(0)[0]]
			return 'UNKNOWNREF'
		def r2(m):
			return m.groups()[0]
		label_dict = {o.label: o.head for o in self if o.label}
		for ele in self:
			ele.content = re.sub('\\\\([<|>])', r2, re.sub('\\\\ref:(\w+)', r, ele.content))
		return ''.join([ele.get() + separator for ele in self])
	
class Tree:
	def __init__(self, content='', label='', separator='. '):
		self.content = content
		self.label = label
		self.separator = separator
		self.branches = []
		self.style = [empty, title, sub_title, sub_element, alphabet_lst, roman_lst]
	def get_style(self, level):
		if level<len(self.style):
			return self.style[level]
		return self.style[-1]
	def add_branch(self, branch):
		self.branches.append(branch)
	def get(self, level=0, position=0, base_style=''):
		s = self.get_style(level)(position, base_style)
		c = [Element(s, self.content, self.label, self.separator)]
		for i in range(len(self.branches)):
			c.extend(self.branches[i].get(level+1, i, s))
		return ElementLst(c)
	def dumps(self, level=0, position=0, base_style=0):
		return self.get(level, position, base_style).dumps()
	def dump(self, file, level=0, position=0, base_style=0):
		file.write(self.dumps(level, position, base_style))