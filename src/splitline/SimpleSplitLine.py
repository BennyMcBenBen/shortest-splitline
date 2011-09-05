'''
Created on Aug 21, 2011

@author: Ben
'''
import math
from collections import deque

class SimpleSplitLine(object):
    '''
    SimpleSplitLine provides an implementation which prints out each iteration 
    of the shortest splitline algorithm
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
        
        # print out BFS results
        print(out)
        
        # print out each level of the tree
        if len(out) > 2:
            print("%s = %s + %s" % (out[0], out[1], out[2]))
            
            log = math.log(len(out), 2)
            steps = math.floor(log)
            
            step = 0
            i = 1
            j = 3
            power = 1
            
            while (step < steps):
                right = " ".join(["%s" % o for o in out[i:j]])
                print(str(out[0]) + " = " + right)
                step += 1
                power += 1
                i = j
                j = min(j + int(math.pow(2, power)), len(out))
                pass
            
        # TODO format the results so it looks like
        # 7 = (2 + 2) + (2 + 1)
        
simple = SimpleSplitLine()
simple.printSplitLine(7)
        