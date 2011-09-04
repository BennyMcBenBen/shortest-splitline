'''
Created on Aug 21, 2011

@author: Ben
'''
import math
from collections import deque

class SimpleSplitLine(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
    def printSplitLine(self, n):
        out = []
        
        # BFS
        working = deque()
        working.append(n)
        while len(working) > 0:
            x = working.popleft()
            out.append(x)
            if x > 1:
                a = math.ceil(x/2)
                b = math.floor(x/2)
                working.append(a)
                working.append(b)
        
        print(out)
        
        # first level
        if len(out) > 2:
            print(str(out[0]) + " = " + str(out[1]) + " + " + str(out[2]))
        
simple = SimpleSplitLine()
simple.printSplitLine(7)
        