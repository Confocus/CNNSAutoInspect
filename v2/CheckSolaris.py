#coding=utf-8

'''
1、syslog.conf
2、没有 /etc/login.defs得不到MAX_PASS_DAYS /etc/default/passwd 中的MAXWEEK
3、查看服务使用命令svcs -a
4、ntp设置 cat /etc/inet/ntp.server
5、设置root 密码 使用sudo passwd root 命令
6、系统会自动检测,intel的cpu就用32的内核，amd64的就用64的内核

'''

import subprocess
import os
import time
import sys
import copy
from commonfunc import *
from CheckLinux import *
from GenExcel import *

class CheckSolaris(CheckLinux):
    def __init__(self):
        super(CheckSolaris, self).__init__()
        self.__morecmd = [#"cat /etc/syslog.conf",#0
            "cat /etc/default/passwd",
            "svcs -a",
            "cat /etc/inet/ntp.client",
            "cat /etc/pam.d/passwd"
        ]
        
    def CS_Passwd_Complexity(self, cmdline = "cat /etc/pam.d/passwd"):
        super(CheckSolaris, self).CL_Passwd_Complexity(cmdline)
    
    def CS_Pass_Maxdays(self, cmdline = "cat /etc/default/passwd"):
        
        logcontent = "\nPassword time limit:\n"
        xlcontent = ""
        bfragile = False        
        
        result = os.popen(cmdline)  
        content = ComCompatibleList(result.readlines())  
        
        for line in content:
            if len(line.rstrip().lstrip()) == 0:
                continue
            if line.lstrip()[0] == '#':
                continue
            if "MAXWEEKS" in line:
                if line.rstrip()[-1] == '=':
                    xlcontent = "unset"
                    bfragile = True
                    break
                else:
                    MaxDays = int(line.split('=')[1]) * 7
                    xlcontent += str(MaxDays) + '\n'
                    logcontent += str(MaxDays) + '\n'
                    break
            
        if MaxDays < 90:
            bfragile = True
        if len(xlcontent.rstrip().lstrip()) == 0:
            xlcontent = "unset."
            bfragile = True      
            
        self.LogList.append(logcontent)
        retlist = ConstructPCTuple(self.__xlpos[8], xlcontent, self.__fgpos[8], bfragile)
        self.PCList.append(retlist[0])    
        self.PCList.append(retlist[1])     
        
        print(logcontent)
        print(retlist[0][2])
        print(retlist[1][2])
        
       
        
        
    def CheckUnnessesaryServ(self):
        rescontent = ""
        bres = False             
        content = []
        #count = 0
        p = subprocess.Popen(self.__morecmd[2], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait()              
        f = open(self.respath, "a+")
        f.write("*************************Unnessesary Server*************************\n")    
        content = CheckCommonFunc.CompatibleList(p.stdout.readlines())
        
        for line in content:
            for serv in self._CheckCentOS__unnessserv:
                try:
                    line.split()[0]
                    line.split()[2]            
                except IndexError:
                    continue
                else:
                    if serv in line.split()[2]:
                        rescontent = rescontent + line.rstrip() + '\n'
                        if line.split()[0] != "disabled":
                            bres = False
                            f.write("Warn:" + line.split()[2] + "\n")
                        break
        f.close()
        pct1 = PCTuple(self._CheckCentOS__respos[17][0], self._CheckCentOS__respos[17][1], rescontent)
        pct2 = PCTuple(self._CheckCentOS__expos[17][0], self._CheckCentOS__expos[17][1], "exist" if bres == True else "unexist")
        self.PCList.append(pct1)
        self.PCList.append(pct2)    
    
    def CheckNPTServ(self):
        rescontent = ""
        bres = False         
        status = False
        content = []
        serverlist = []
        log = ""
        p = subprocess.Popen(self.__morecmd[3], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait()      
        f = open(self.respath, "a+")
        f.write("*************************NPT Server*************************\n")
        
        content = CheckCommonFunc.CompatibleList(p.stdout.readlines())        
        for line in content:
            try:
                line.split()[0]
            except IndexError:
                continue
            else:
                if line.split()[0] == "server":
                    log = line
                    serverlist.append(log)
                    status = True
                    
        if status == True:
            for i in serverlist:
                rescontent = rescontent + i.rstrip() + '\n'
                f.write(i + '\n')
        else:
            bres = True
            rescontent = "No Setting."
            f.write("Warn:NPT.\n")
        f.close()
        pct1 = PCTuple(self._CheckCentOS__respos[18][0], self._CheckCentOS__respos[18][1], rescontent)
        pct2 = PCTuple(self._CheckCentOS__expos[18][0], self._CheckCentOS__expos[18][1], "exist" if bres == True else "unexist")
        self.PCList.append(pct1)
        self.PCList.append(pct2)          
        

        


    def testfunc(self):
        print(self._CheckCentOS__test)#访问父类私有属性的一种方式————name mangling
        

def CheckSolarisRun():
    c = CheckSolaris()
    #c.CheckUnnessesaryServ()
    assert CheckCommonFunc.GetLinuxVer() != 0
    
    #if os.path.exists(CheckCentOS.respath) == True:
        #os.remove(CheckCentOS.respath)
    if os.path.exists(c.respath) == True:
        os.remove(c.respath)    
    logtime = str(time.time()).replace('.', '')
    logpath = "/usr/ProjectTest/log_" + logtime + ".txt"
    
    if os.path.exists("/usr/ProjectTest") == False:
        os.mkdir("/usr/ProjectTest")    
    if os.path.exists(logpath) == True:
        os.remove(logpath)
        
    flog = open(logpath, "w")
   
    
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
        oe.FillContent("/usr/ProjectTest/centos2.xlsx", c.PCList)    
    except:
        flog.write("Operate Excel exception.\n")
    else:
        flog.write("Operate Excel finished.\n")
        
    flog.close()

if __name__ == "__main__":
    print("start...")
    CheckSolarisRun()