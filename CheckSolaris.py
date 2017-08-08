#coding=utf-8

#syslog.conf
#没有 /etc/login.defs得不到MAX_PASS_DAYS /etc/default/passwd 中的MAXWEEK
#查看服务使用命令svcs -a
#ntp设置 cat /etc/inet/ntp.server
#
#设置root 密码 使用sudo passwd root 命令
#系统会自动检测,intel的cpu就用32的内核，amd64的就用64的内核

import subprocess
import os
import time
import sys
import copy
import CheckCommonFunc
import CheckCentOS
from GenExcel import PCTuple, OperExcel

class CheckSolaris(CheckCentOS.CheckCentOS):
    def __init__(self):
        super(CheckSolaris, self).__init__()
        self.__morecmd = [
            "cat /etc/syslog.conf",#0
            "cat /etc/default/passwd",
            "svcs -a",
            "cat /etc/inet/ntp.client",
            "cat /etc/pam.d/passwd"#4
        ]
        
    def CheckAuditLog(self):
        rescontent = ""
        bres = False        
        content = []
        count = 0
        finish = []   
        log = ""
        
        p1 = subprocess.Popen(self.__morecmd[0], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)#self.__AllCommands[0]
        retval = p1.wait()  
        
        content = CheckCommonFunc.CompatibleList(p1.stdout.readlines())
       
        f = open(self.respath, "a+")
        f.write("*************************Log Audit*************************\n")
        for line in content:
            if(count == len(self._CheckCentOS__auditlogitems)):#子类并没有继承父类的私有变量，所以不能直接self.__auditlogitems。如果是self.auditlogitems则允许
                break
            for item in self._CheckCentOS__auditlogitems.keys():#self.__auditlogitems
                if item in line:
                    finish.append(item)
                    try:
                        itemkey = line.split()[0]
                        itemvalue = line.split()[1]
                    except IndexError:
                        continue
                    rescontent = rescontent + item + ":" + itemvalue + '\n'
                    if(self._CheckCentOS__auditlogitems[itemkey] == itemvalue):
                        count += 1
                        #print("%s:pass.The value is %s"%(itemkey, itemvalue))
                        f.write(itemkey + ":pass.The value is " + itemvalue + "\n")
                    else:
                        bres = True
                        #print("%s:miss"%(itemkey))
                        f.write(itemkey + ":miss\n")
                    break
                    
        if(len(finish) == len(self._CheckCentOS__auditlogitems)):
            f.write("All auditlog items were checked.\n")
        else:######################################################Warn######################################################
            #print("Uncheck:")
            #print(list(set(__auditlogitems.keys()).difference(set(finish)))) 
            f.write("Uncheck:" + ' '.join(list(set(self._CheckCentOS__auditlogitems.keys()).difference(set(finish)))) + "\n")
        
        p2 = subprocess.Popen(self.AllCommands[1], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p2.wait()  
        
        log = CheckCommonFunc.CompatibleStr(''.join(p2.stdout.readlines()).rstrip().lstrip())
        #print(log)
        rescontent = rescontent + "/var/log/wtmp:" + log
        if log.strip() != "":
            #print("Log:%s"%(log))
            f.write("Log:" + log + "\n")
        else:######################################################Warn######################################################
            #print("Log:miss")
            f.write("Warn:There is no log record\n")
        f.close()
        
        pct1 = PCTuple(self._CheckCentOS__respos[0][0], self._CheckCentOS__respos[0][1], rescontent)
        pct2 = PCTuple(self._CheckCentOS__expos[0][0], self._CheckCentOS__expos[0][1], "exist" if bres == True else "unexist")
        self.PCList.append(pct1)
        self.PCList.append(pct2)        
    
    def CheckNetLogServConf(self):
        rescontent = ""
        bres = False        
        content = []
        bstatus = False
        argcmd = ""
        f = open(self.respath, "a+")
        f.write("*************************Net Log Server*************************\n")   
            
        p = subprocess.Popen(self.__morecmd[0], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait()             
        
        content = CheckCommonFunc.CompatibleList(p.stdout.readlines())
        for line in content:
            if "*.* @" in line and line.lstrip()[0] != '#':
                #print(line)
                rescontent = rescontent + line.rstrip()+ '\n'
                f.write(line.rstrip() + '\n')
                bstatus = True
        if bstatus == False:
            rescontent = "Default setting" + '\n'
            f.write("Default setting" + '\n')            
        f.close()
        
        pct1 = PCTuple(self._CheckCentOS__respos[3][0], self._CheckCentOS__respos[3][1], rescontent)
        self.PCList.append(pct1)    
    
    def CheckPasswdComplexity(self):
        #print("CheckPasswdComplexity start...")
        rescontent = ""
        bres = False        
        #pam_passwdqc.so
        content = []
        log = ""
        state1 = False
        p1 = subprocess.Popen(self.__morecmd[0], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p1.wait()         
        f = open(self.respath, "a+")
        f.write("*************************Password Complexity Configuration*************************\n") 
        content = CheckCommonFunc.CompatibleList(p1.stdout.readlines())
        try:  
            for line in content:
                if "password" in line and  \
                "requisite" in line and \
                "pam_passwdqc.so" in line and\
                line.lstrip()[0] != '#': 
                    rescontent = rescontent + line.rstrip() + '\n'
                    if "enforce=everyone" in line:
                        state1 = True
                    else:
                        state1 = False
            if state1 == False:
                f.write("Warn1:There are problem in password-complexity setting.\n")
                #rescontent = "No Setting.\n"
                bres = True
                #return False
                #raise CentOSException()
        
            for line in content:
                if "pam_cracklib.so" in line and \
                   "password" in line and \
                   "requisite" in line and \
                   line.lstrip()[0] != '#':
                    rescontent = rescontent + line.rstrip() + '\n'
                    if "minlen=8" in line and "lcredit=-1" in line and \
                       "ucredit=-1" in line and "ocredit=-1" in line and \
                       "dcredit=-1" in line:
                        state1 = True
                    else:   
                        state1 = False
                    break
            
            if state1 == False:
                bres = True
                #rescontent = "No Setting.\n"
                f.write("Warn2:There are problem in password-complexity setting.\n")
                #f.close()
                #return False        
            else:
                f.write("Password-complexity setting correct.\n") 
                
            for line in content:
                if "password" in line and "include" in line and \
                   "pam_stack.so" in line and line.lstrip()[0] != '#':
                    rescontent = rescontent + line.rstrip() + '\n'
                    if "system-auth" in line:
                        state1 = True
                    else:
                        state1 = False
            if state1 == False:
                bres = True
                #rescontent = "No Setting.\n"
                f.write("Warn3:There are problem in password-complexity setting.\n")
                #f.close()
                #return False        
            else:
                f.write("Password-complexity setting correct.\n")             
        except:
            pass
        finally:
            f.close()
            if rescontent == "":
                rescontent == "No Setting."
            pct1 = PCTuple(self._CheckCentOS__respos[7][0], self._CheckCentOS__respos[7][1], rescontent)
            pct2 = PCTuple(self._CheckCentOS__expos[7][0], self._CheckCentOS__expos[7][1], "exist" if bres == True else "unexist")
            self.PCList.append(pct1)
            self.PCList.append(pct2)         
            #print(rescontent) 
    
    def PasswordTimeLimit(self):
        rescontent = ""
        bres = False         
        content = []
        MaxDays = 0
        p = subprocess.Popen(self.__morecmd[1], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait()
        f = open(self.respath, "a+")
        f.write("*************************Password Maxdays*************************\n")
    
        content = CheckCommonFunc.CompatibleList(p.stdout.readlines())
        for line in content:
            if "MAXWEEKS" in line:
                log = line.lstrip().rstrip()
                if log[0] == '#':
                    continue
                elif log[len(log) - 1] == '=':
                    continue
                else:
                    MaxDays = int(log.split('=')[1])
                    break
        if MaxDays == 0:
            bres = True
            rescontent = "Default Setting."
            f.write("PASS_MAX_DAYS:Default\n")
        else:
            rescontent = str(MaxDays * 7) + '\n'
            f.write("PASS_MAX_DAYS:" + str(MaxDays * 7) + "\n")
        f.close()
        pct1 = PCTuple(self._CheckCentOS__respos[8][0], self._CheckCentOS__respos[8][1], rescontent)
        pct2 = PCTuple(self._CheckCentOS__expos[8][0], self._CheckCentOS__expos[8][1], "exist" if bres == True else "unexist")
        self.PCList.append(pct1)
        self.PCList.append(pct2)        
        
        
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