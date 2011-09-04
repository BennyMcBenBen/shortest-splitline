'''
Created on Aug 21, 2011

@author: Ben
'''
import math

class SimpleSplitLine(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
    def printSplitLine(self, n):
        if n == 1:
            pass
        else:
            a = math.ceil(n/2)
            b = math.floor(n/2)
            print("a=" + str(a) + ", b=" + str(b))
            self.printSplitLine(a)
            self.printSplitLine(b)
        
simple = SimpleSplitLine()
simple.printSplitLine(7)
        