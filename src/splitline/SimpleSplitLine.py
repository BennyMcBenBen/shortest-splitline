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
        leno = len(out)
        if len(out) > 2:
            log = math.log(leno, 2)
            steps = math.floor(log)
            
            step = 0
            i = 0
            j = 1
            power = 0
            
            while (step < steps):
                power += 1
                i = j
                j = j + int(math.pow(2, power))
                
                print("i=%s, j=%s" % (i, j))
                print(out[i:j])
                
                right = " ".join(["%s" % o for o in out[i:j]])
                
                sumo = sum(out[i:j])
                if sumo < n:
                    for x in range(sumo, n):
                        right += " 1"
                    
                print(str(n) + " = " + right)
                
                step += 1
                pass
            
        # TODO format the results so it looks like
        # 7 = (2 + 2) + (2 + 1)
        
simple = SimpleSplitLine()
simple.printSplitLine(9)
        