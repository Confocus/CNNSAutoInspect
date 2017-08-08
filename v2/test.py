#coding=utf-8
import subprocess
import os
import time
import sys
import copy
import commands

cmd = "getconf LONG_BIT"

def testSpeed1():
    #real 15.35
    #user 5.09
    #sys 8.13
    
    i = 0
    while(i < 10000):
        
        p = subprocess.Popen(cmd, shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait() 
        i += 1


def testSpeed2():
    #real 11.67
    #user 1.44
    #sys 3.08
    
    i = 0
    while(i < 10):
        result = os.popen(cmd)  
        res = result.read()  
        print(res)
        i += 1
        
        
def testSpeed3():

#real 13.70
#user 0.95
#sys 2.19

    i = 0
    while(i < 10000):
        output = commands.getstatusoutput(cmd)  
        i += 1 
        
        
def GetCurrentPath():
    #os.path.dirname(os.path.realpath(__file__))　
    #os.path.split(os.path.realpath(__file__))[0]
    return os.path.split(os.path.realpath(__file__))[0]

print(GetCurrentPath())