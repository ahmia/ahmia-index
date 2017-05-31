import filter_onions
import child_abuse_onions
import sys
import os

def blacklisting():
	list=child_abuse_onions.get_abuse_onions()
	for n in range(len(list)):
		for i in range(0,2):
			os.system("python filter_onions.py "+list[n])
if __name__ == '__main__':
	blacklisting()