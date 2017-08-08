#coding=utf-8
import subprocess
import os
import time
import sys
import copy

import CheckCentOS
import CheckCommonFunc
from GenExcel import PCTuple, OperExcel

class CheckRHEL(CheckCentOS.CheckCentOS):
    def testfunc(self):
        print("This is RHEL-Check!")
        
    #def GetLinuxVer(self):
        #count = 0
        #cmd = "cat \/etc\/redhat-release"
        #p = subprocess.Popen(cmd, shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        #retval = p.wait()    
        
        #pyVer = self.GetPyVersion()
        #if pyVer == 2:
            #verinfo = p.stdout.read().rstrip().lstrip()
        #else:
            #verinfo = str(p.stdout.read().rstrip().lstrip(), encoding = "utf-8")
        #ver = verinfo.split()[len(verinfo.split()) - 2].split('.')[0]
        #try:   
            #ver = int(ver)
        #except ValueError:
            #ver = 0       
        #return ver #Redhat5 = CentOS5;RedHat6 = CentOS6
        
        
#if __name__ == "__main__": 
def CheckRHELRun():
    c = CheckRHEL()
    
    assert CheckCommonFunc.GetLinuxVer() != 0
    
    if os.path.exists(c.respath) == True:
        os.remove(c.respath)
    logtime = str(time.time()).replace('.', '')
    logpath = "/usr/ProjectTest/log_" + logtime + ".txt"
    
    if os.path.exists("/usr/ProjectTest") == False:
        os.mkdir("/usr/ProjectTest")    
    if os.path.exists(logpath) == True:
        os.remove(logpath)
        
    flog = open(logpath, "w")
   
    
    #print("CentOS version:" + str(CheckCommonFunc.GetLinuxVer()))
    try:    
        c.CheckAuditLog()
    except:
        flog.write("CheckAuditLog exception.\n")
    else:
        flog.write("CheckAuditLog finished.\n")
        
    try:    
        c.CheckLogAuth()
    except:
        flog.write("CheckLogAuth exception.\n")
    else:
        flog.write("CheckLogAuth finished.\n")
    
    try:
        c.CheckNetLogServConf()
    except:
        flog.write("CheckNetLogServConf exception.\n")
    else:
        flog.write("CheckNetLogServConf finished.\n")
        
    try:
        c.CheckAccountAuth()
    except:
        flog.write("CheckAccountAuth exception.\n")
    else:
        flog.write("CheckAccountAuth finished.\n")    
        
    try:    
        c.CheckUselessAccount()
    except:
        flog.write("CheckUselessAccount exception.\n")
    else:
        flog.write("CheckUselessAccount finished.\n")   
        
    try:    
        c.CheckPermitRootLogin()
    except:
        flog.write("CheckPermitRootLogin exception.\n")
    else:
        flog.write("CheckPermitRootLogin finished.\n")
        
    try:
        c.CheckPasswdComplexity()
    except:
        flog.write("CheckPasswdComplexity exception.\n")
    else:
        flog.write("CheckPasswdComplexity finished.\n")
        
    try:
        c.PasswordTimeLimit()
    except:
        flog.write("PasswordTimeLimit exception.\n")
    else:
        flog.write("PasswordTimeLimit finished.\n")
        
    try:
        c.AuthenFailedTimes()
    except:
        flog.write("AuthenFailedTimes exception.\n")
    else:
        flog.write("AuthenFailedTimes finished.\n")
        
    try:
        c.PasswdHistoryTimes()
    except:
        flog.write("PasswdHistoryTimes exception.\n")
    else:
        flog.write("PasswdHistoryTimes finished.\n")
        
    try:
        c.CheckVitalDirAuth()
    except:
        flog.write("CheckVitalDirAuth exception.\n")
    else:
        flog.write("CheckVitalDirAuth finished.\n")
        
    try:
        c.CheckUmask()
    except:
        flog.write("CheckUmask exception.\n")
    else:
        flog.write("CheckUmask finished.\n")
        
    try:
        c.CheckRemoteLogin()
    except:
        flog.write("CheckRemoteLogin exception.\n")
    else:
        flog.write("CheckRemoteLogin finished.\n")
        
    try:
        c.CheckIPRangement()
    except:
        flog.write("CheckIPRangement exception.\n")
    else:
        flog.write("CheckIPRangement finished.\n")
            
    try:
        c.CheckTimeout()
    except:
        flog.write("CheckTimeout exception.\n")
    else:
        flog.write("CheckTimeout finished.\n")
        
    try:
        c.CheckUnnessesaryServ()
    except:
        flog.write("CheckUnnessesaryServ exception.\n")
    else:
        flog.write("CheckUnnessesaryServ finished.\n")
        
    try:
        c.CheckNPTServ()
    except:
        flog.write("CheckNPTServ exception.\n")
    else:
        flog.write("CheckNPTServ finished.\n")
        
    try:
        c.CheckDNSIP()
    except:
        flog.write("CheckDNSIP exception.\n")
    else:
        flog.write("CheckDNSIP finished.\n")    
    
    try:
        oe = OperExcel()
        oe.FillContent("/home/wang/Desktop/centos2.xlsx", c.PCList)    
    except Exception as e:
        #print(e.message)
        flog.write("Operate Excel exception.\n")
    else:
        flog.write("Operate Excel finished.\n")
        
    flog.close()    
    
def Run():
    print("RHEL running.")
    
if __name__ == "__main__":
    print("start...")
    CheckRHELRun()