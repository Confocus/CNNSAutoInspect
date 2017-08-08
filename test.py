#coding=utf-8
#import subprocess
#import os
#import time
#import sys
#import copy
#import CheckCommonFunc


#def GetPyVersion():
    ##print(sys.version_info)
    #return sys.version_info[0]

#def GetLongBit():
    #cmd = "getconf LONG_BIT"
    #p = subprocess.Popen(cmd, shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #retval = p.wait()               
    #pyVer = GetPyVersion()
    #if pyVer == 2:
        ##print("PyVersion is 2\n")
        #lbinfo = p.stdout.read().rstrip().lstrip() 
    #else:
        ##print("PyVersion is 3\n")
        #lbinfo = str(p.stdout.read().rstrip().lstrip(), encoding = "utf-8")   
    #try:
        #lbinfo = int(lbinfo)
    #except ValueError:
        #lbinfo = 0
    #return lbinfo

#def GetLinuxVer():#CentOS5:Python2;CentOS6:Python2;CentOS7:Python3
    #count = 0
    #cmd = ""
    #if os.path.exists("/etc/release"):#Solaris
           
        #fver = open("/etc/release")
        #line = fver.readline().lstrip('\n').rstrip()
        #fver.close()
        #try:
            #ver = int(line.split()[2].split('.')[0])
        #except:
            #ver = 0
        #if ver == 11:
            #print("yes")
        #print(ver)
        #return ver
        
    #if os.path.exists("/etc/redhat-release"):
        #cmd = "cat \/etc\/redhat-release"
   
    
    #verinfo = ""
    #p = subprocess.Popen(cmd, shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #retval = p.wait()           
    
    ##pyVer = GetPyVersion()
    ##if pyVer == 2:
        ###print("PyVersion is 2\n")
        ##verinfo = p.stdout.read().rstrip().lstrip() 
    ##else:
        ###print("PyVersion is 3\n")
        ##verinfo = str(p.stdout.read().rstrip().lstrip(), encoding = "utf-8") #python3中,read到的是字符object，需要转换为str object
    #verinfo = CheckCommonFunc.CompatibleStr(p.stdout.read().rstrip().lstrip())
    ##CentOS Linux release 7.3.1611 (Core) 
    ##Red Hat Enterprise Linux Server release 5.4 (Tikanga)
    
    #for i in verinfo.split():
        #count += 1
        #if i == "release":
            #break        
    #try:
        #if count != 0:
            #ver = verinfo.split()[count]
    #except IndexError:
        #ver = 0
        #return ver
    #ver = ver.split(".")[0]
    
    #try:   
        #ver = int(ver)
    #except ValueError:
        #ver = 0       
        
    #return ver#CentOS5=RedHat5；#CentOS6 = CentOS7 = RedHat6 #外部只需判断是否等于5


##print("GetLinuxVer()")
def PraseDataFile(path):
    dataf = open(path, 'rb')
    #data = dataf.readlines()
    for line in dataf.readlines():
        print(line)
    #print(data)
    dataf.close()
    
PraseDataFile("C:\\Users\\Henrry\\Desktop\\EmbeddedLDAP.data")

