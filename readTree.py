from ruleTree import *
import sys
import re

def reads(s):
	root = Tree(seperator='')
	current = [root]
	for m in re.finditer('(\w*)(?<!\\\\)(<+|\||>+)(.+?)\s*(?<!\\\\)(?=\w*(?:<+|\||>+|.\Z))', s, re.DOTALL+re.UNICODE):
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

def main():
	if len(sys.argv)<1: return
	with open(sys.argv[1], 'r') as f: t = f.read()
	root = reads(t)
	if len(sys.argv)>2: path = sys.argv[2]
	else: path = re.match('(.+)(\..*?\Z)', sys.argv[1]).groups()[0]+'.txt'
	with open(path, 'wb') as f: f.write(root.dumps().encode('UTF-8'))
	
if __name__=='__main__': main()