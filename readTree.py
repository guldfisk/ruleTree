from ruleTree import *
import sys
import re

def reads(s):
	root = Tree(seperator='')
	current = [root]
	for m in re.finditer('(\w*)(?<!\\\\)(<+|\||>+)(.+?)\s*(?<!\\\\)(?=\w*(?:<+|\||>+|.\Z))', t, re.DOTALL+re.UNICODE):
		label, action, content = m.groups()
		move = len(action)
		tree = Tree(content, label)
		if action[0]=='>' and current[-1].branches:
			current[-1].branches[-1].addBranch(tree)
			current.append(current[-1].branches[-1])
		elif action[0]=='<' and len(current)>move and current[-move].branches:
			current = current[:-move]
			current[-1].addBranch(tree)
		else: current[-1].addBranch(tree)
	return root
		
if __name__=='__main__' and len(sys.argv)>1:
	file = open(sys.argv[1], 'r')
	t = file.read()
	file.close()
	root = reads(t)
	if len(sys.argv)>2: path = sys.argv[2]
	else: path = re.match('(.+)(\..*?\Z)', sys.argv[1]).groups()[0]+'.txt'
	file = open(path, 'wb')
	file.write(root.dumps().encode('UTF-8'))
	file.close()