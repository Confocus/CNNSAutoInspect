#coding=utf-8
import subprocess
import os
import time
import sys
import copy
import socket

class CommonCentOSException(Exception):  
    pass      
    
    
def ComOutputLog():
    pass
def ComOutputExcel():
    pass

def ComCreateResultFilePath():
    curpath = os.path.split(os.path.realpath(__file__))[0] + '/'
    logtime = str(time.time()).replace('.', '')
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    
    logpath = curpath + "log_" + logtime + ".txt"
    respath = curpath + str(hostname) + str(ip) + ".txt"
    xlpath = curpath + str(hostname) + str(ip) + ".xlsx"
    
    return logpath, respath, xlpath
    
    
def ComGetCurrentPath():
    #os.path.dirname(os.path.realpath(__file__))　
    #os.path.split(os.path.realpath(__file__))[0]
    return os.path.split(os.path.realpath(__file__))[0]


def ComGetHost():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return hostname, ip

##############################################################      GetPyVersion       ########################################################################################
def ComGetPyVersion():
    #print(sys.version_info)
    return sys.version_info[0]


##############################################################      GetLongBit       ########################################################################################
def ComGetLongBit():
    cmd = "getconf LONG_BIT"
    p = subprocess.Popen(cmd, shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    retval = p.wait()              
    pyVer = GetPyVersion()
    #if pyVer == 2:
        ##print("PyVersion is 2\n")
        #lbinfo = p.stdout.read().rstrip().lstrip() 
    #else:
        ##print("PyVersion is 3\n")
        #lbinfo = str(p.stdout.read().rstrip().lstrip(), encoding = "utf-8")   
    lbinfo = CompatibleStr(p.stdout.read().rstrip().lstrip())
    try:
        lbinfo = int(lbinfo)
    except ValueError:
        lbinfo = 0
    return lbinfo
    
def ComGetReleaseVer():
    if os.path.exists("/etc/release"):
        return "Solaris"
    
    cmd = "cat \/etc\/redhat-release"
    relinfo = ""
    p = subprocess.Popen(cmd, shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    retval = p.wait()           
    relinfo = CompatibleStr(p.stdout.read().rstrip().lstrip())
    if "CentOS" in relinfo:
        return "CentOS"
    if "Red" in relinfo:
        return "RHEL"
    return ""


##############################################################      GetLinuxVer       ########################################################################################
#Pass CentOS5_i386、CentOS6、CentOS7
def ComGetLinuxVer():#CentOS5:Python2;CentOS6:Python2;CentOS7:Python3
    count = 0
    cmd = ""
   
    if os.path.exists("/etc/release"):#Solaris
        fver = open("/etc/release")
        line = fver.readline().lstrip('\n').rstrip()
        fver.close()
        try:
            ver = int(line.split()[2].split('.')[0])
        except:
            ver = 0
        
        return ver    
    
    if os.path.exists("/etc/redhat-release"):
        cmd = "cat \/etc\/redhat-release"
    
    
    verinfo = ""
    p = subprocess.Popen(cmd, shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    retval = p.wait()           
    
    #pyVer = GetPyVersion()
    #if pyVer == 2:
        ##print("PyVersion is 2\n")
        #verinfo = p.stdout.read().rstrip().lstrip() 
    #else:
        ##print("PyVersion is 3\n")
        #verinfo = str(p.stdout.read().rstrip().lstrip(), encoding = "utf-8") #python3中,read到的是字符object，需要转换为str object
    verinfo = CompatibleStr(p.stdout.read().rstrip().lstrip())
    #CentOS Linux release 7.3.1611 (Core) 
    #Red Hat Enterprise Linux Server release 5.4 (Tikanga)
    
    for i in verinfo.split():
        count += 1
        if i == "release":
            break        
    try:
        if count != 0:
            ver = verinfo.split()[count]
    except IndexError:
        ver = 0
        return ver
    ver = ver.split(".")[0]
    
    try:   
        ver = int(ver)
    except ValueError:
        ver = 0       
        
    return ver#CentOS5=RedHat5；#CentOS6 = CentOS7 = RedHat6 #外部只需判断是否等于5


def ComCompatibleStr(s):#Sheild the difference between py2str and py3str
    pyVer = GetPyVersion()
    if pyVer == 2:
        s = s.rstrip().lstrip()
    else:
        s = str(s.strip().lstrip(), encoding = "utf-8")
    return s
    
def ComCompatibleList(l):#Sheild the difference of between py2list and py3list
    #这里传递的是引用，p.stdout.readlines()运行到这里时已经消失，所以形参l所指向的内容是空的
    content = []
    #print(l)
    pyVer = GetPyVersion()
    if pyVer == 2:
        content  = copy.deepcopy(l)
    else:
        for line in l:
            line = str(line, encoding = "utf-8")
            content.append(line.rstrip().lstrip())    
    return content

