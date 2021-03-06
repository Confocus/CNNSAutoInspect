#coding=utf-8
import subprocess
import os
import time
import sys
import copy

import CheckCommonFunc
from GenExcel import PCTuple, OperExcel
from CheckCommonFunc import CentOSException
#from XXX import XXX as XXX
'''Page1'''
##############################################################      New idea       ########################################################################################
#先判断Python的版本，覆写str()函数。再去检查Linux版本，以决定执行不同的命令



#Redhat5 = CentOS5;RedHat6 = CentOS6;CentOS7
#CentOS5、RedHat5 = syslog.conf
#CentOS6、CentOS7、RedHat6 = rsyslog.conf
class CheckCentOS(object):
    
    def __init__(self):
        self.PCList = []
        self.__test = "hello"
        self.respath = "/usr/ProjectTest/res.txt"
        self.__respos = [(14 ,8), #0
                          (15 ,8),
                          (16, 8),
                          (17, 8),
                          (18 ,8),
                          (19, 8),#5
                          (20, 8),
                          (21, 8),
                          (22, 8),#8 
                          (23, 8),
                          (24, 8),
                          (25, 8),
                          (26, 8),
                          (27, 8),#13
                          (28, 8),
                          (29, 8),#15
                          (30, 8),
                          (31, 8),#17
                          (32, 8),
                          (33, 8)#19
                          ]
        
        self.__expos = [(14 ,10), 
                          (15 ,10),
                          (16, 10),
                          (17, 10),
                          (18 ,10),
                          (19, 10),
                          (20, 10),
                          (21, 10),
                          (22, 10), 
                          (23, 10),
                          (24, 10),
                          (25, 10),
                          (26, 10),
                          (27, 10),
                          (28, 10),
                          (29, 10),
                          (30, 10),
                          (31, 10),
                          (32, 10),
                          (33, 10)
                        ]
        
        self.__auditlogitems = {'*.info;mail.none;authpriv.none;cron.none':'/var/log/messages',
               'authpriv.*':'/var/log/secure',
               'mail.*':'-/var/log/maillog',
               'cron.*':'/var/log/cron'}
    
        self.__logauthitems = ["messages",
                  "secure",
                  "maillog",
                  "cron",
                  "spooler",
                  "boot.log"]
    
        self.__unnessserv = ["sendmail",
                    "ftp",
                    "telnet.socket",
                    "IMAP",
                    "POP",
                    "SMB",
                    "cups",
                    "SQL",
                    "DNS",
                    "shell",
                    "login",
                    "exec",
                    "klogin"]
    
        self.AllCommands = ["cat \/etc\/rsyslog.conf",#0
                          "last \/var\/log\/wtmp",
                          "ls -l \/var\/log",
                          "cat \/etc\/syslog.conf",#/etc/rsyslog.conf CentOS6之后
                          "cat \/etc\/passwd",
                          "cat \/etc\/shadow",#5
                          "cat \/etc\/ssh\/sshd_config",
                          "cat \/etc\/pam.d\/system-auth",#7
                          "cat \/etc\/login.defs",
                          "cat \/etc\/pam.d\/login",
                          "cat \/etc\/pam.d\/system-auth",#10
                          "ls -l \/etc\/passwd",
                          "ls -l \/etc\/shadow",
                          "ls -l \/etc\/group",
                          "umask",
                          "ps -elf|grep telnet",#15
                          "ps -elf|grep sshd",
                          "cat \/etc\/hosts.allow",
                          "cat \/etc\/hosts.deny",
                          "cat \/etc\/hosts.deny",
                          "echo $TIMEOUT",#20
                          "systemctl list-unit-files",#use this command in CentOS7 to check unnessesary service
                          "cat \/etc\/ntp.conf",
                          "cat \/etc\/resolv.conf",
                          "chkconfig --list", #use this command in CentOS6 to check unnessesary service
                          "cat \/etc\/syslog.conf",#25
                          "ls -l \/var\/adm\/authlog",
                          "ls -l \/var\/adm\/sylog"
                          ]
    
##############################################################      Just test       ########################################################################################
    def testfunc(self):
        print("This is CentOS-Check!")
    def calltestfunc(self):
        self.testfunc()
    

            
##############################################################      CheckAuditLog       ########################################################################################          
    #Pass CentOS5_i386、CentOS6、CentOS7        
    def CheckAuditLog(self):
        rescontent = ""
        bres = False
        #print("start CheckAuditLog...")
        AuditLogCmd = ""
        content = []
        count = 0
        finish = []   
        log = ""
        ver = CheckCommonFunc.GetLinuxVer()
        if int(ver) == 5:
            AuditLogCmd = self.AllCommands[3]#"cat \/etc\/syslog.conf"
        else:#if ver != 5
            AuditLogCmd = self.AllCommands[0]#"cat \/etc\/rsyslog.conf"
        
        
        p1 = subprocess.Popen(AuditLogCmd, shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)#self.AllCommands[0]
        retval = p1.wait()  
        #if int(ver) == 5:
            #content = copy.deepcopy(p1.stdout.readlines())
        #else:
            #for line in p1.stdout.readlines():
                #line = str(line, encoding = "utf-8")
                #content.append(line.rstrip())
        content = CheckCommonFunc.CompatibleList(p1.stdout.readlines())
       
        f = open(self.respath, "a+")
        f.write("*************************Log Audit*************************\n")
        for line in content:
            #line = str(line, encoding = "utf-8")
            if(count == len(self.__auditlogitems)):
                break
            for item in self.__auditlogitems.keys():
                if item in line:
                    finish.append(item)
                    try:
                        itemkey = line.split()[0]
                        itemvalue = line.split()[1]
                    except IndexError:
                        continue
                    rescontent = rescontent + item + ":" + itemvalue + '\n'
                    if(self.__auditlogitems[itemkey] == itemvalue):
                        count += 1
                        #print("%s:pass.The value is %s"%(itemkey, itemvalue))
                        f.write(itemkey + ":pass.The value is " + itemvalue + "\n")
                    else:
                        #print("%s:miss"%(itemkey))
                        bres = True
                        f.write(itemkey + ":miss\n")
                    break
        
                    
        if(len(finish) == len(self.__auditlogitems)):
            f.write("All auditlog items were checked.\n")
        else:######################################################Warn######################################################
            #print("Uncheck:")
            #print(list(set(__auditlogitems.keys()).difference(set(finish)))) 
            f.write("Uncheck:" + ' '.join(list(set(self.__auditlogitems.keys()).difference(set(finish)))) + "\n")
        
        p2 = subprocess.Popen(self.AllCommands[1], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p2.wait()  
        #if int(ver) == 5:
            #log = ''.join(p2.stdout.readlines()).rstrip().lstrip()
            ##print(log)
        #else:
            #log = str(p2.stdout.read().lstrip().rstrip(), encoding = "utf-8")
        log = CheckCommonFunc.CompatibleStr(''.join(p2.stdout.readlines()).rstrip().lstrip())
        #print(log)
        rescontent = rescontent + "/var/log/wtmp:" + log
        if log.strip() != "":
            #print("Log:%s"%(log))
            f.write("Log:" + log + "\n")
        else:######################################################Warn######################################################
            #print("Log:miss")
            bres = True
            f.write("Warn:There is no log record\n")
        f.close()
        
        
        pct1 = PCTuple(self.__respos[0][0], self.__respos[0][1], rescontent)
        pct2 = PCTuple(self.__expos[0][0], self.__expos[0][1], "exist" if bres == True else "unexist")
        self.PCList.append(pct1)
        self.PCList.append(pct2)
        #print(rescontent)
    
    
##############################################################      CheckLogAuth       ########################################################################################          
    #Pass CentOS5_i386、CentOS6、CentOS7     
    def CheckLogAuth(self):
        rescontent = ""
        bres = False        
        count = 0
        content = []
        finish = []
        
        f = open(self.respath, "a+")
        f.write("*************************Log Authority*************************\n")    
        p = subprocess.Popen(self.AllCommands[2], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)   #"ls -l \/var\/log"
        retval = p.wait()           
        #ver = self.GetLinuxVer()
        #if int(ver) == 5:
            #content = copy.deepcopy(p.stdout.readlines())
        #else:
            #for line in p.stdout.readlines():
                #line = str(line, encoding = "utf-8")
                #content.append(line.rstrip())        
        content = CheckCommonFunc.CompatibleList(p.stdout.readlines())
        
        for line in content:
            if(count == len(self.__logauthitems)):
                break            
            try:
                filename = line.split()[8]
            except IndexError:
                continue
            for item in self.__logauthitems:
                if item == filename:
                    rescontent = rescontent + line.rstrip() + '\n'
                    finish.append(item)
                    count += 1
                    if(line.split()[0] == "-rw-------."):
                        #print("Authority of %s is correct"%(item))
                        f.write("Authority of " + item + " is correct.\n")
                    else:
                        #print("Warn:Authority of %s is not 600"%(item))
                        bres = True
                        f.write("Warn:Authority of " + item + " is not 600.\n")
                        #print("Warn:Authority of %s is %s"%(item,line.split()[0]))
                    break
             
        if(len(finish) == len(self.__logauthitems)):
            f.write("All seclog items were checked.\n")
        else:
            #print("Uncheck items:")
            f.write("Uncheck:" + ' '.join(list(set(self.__logauthitems).difference(set(finish)))) + "\n")
            #for i in list(set(self.__logauthitems).difference(set(finish))):
                #print(i,'','\t')            
                
        p = subprocess.Popen(self.AllCommands[26], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait()  
        authadm = CheckCommonFunc.CompatibleList(p.stdout.read())
        rescontent = rescontent + "/var/adm/authlog:" + authadm.rstrip() + '\n'
        p = subprocess.Popen(self.AllCommands[27], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait()  
        authadm = CheckCommonFunc.CompatibleList(p.stdout.read())
        rescontent = rescontent + "/var/adm/sylog:" + authadm.rstrip() + '\n'
        
        f.close()           
        
        pct1 = PCTuple(self.__respos[1][0], self.__respos[1][1], rescontent)
        pct2 = PCTuple(self.__expos[1][0], self.__expos[1][1], "exist" if bres == True else "unexist")
        self.PCList.append(pct1)
        self.PCList.append(pct2)      
        #print(rescontent)
        
        
    def CheckNetLogServConf(self):
        rescontent = ""
        bres = False        
        content = []
        bstatus = False
        argcmd = ""
        f = open(self.respath, "a+")
        f.write("*************************Net Log Server*************************\n")   
            
        ver = CheckCommonFunc.GetLinuxVer()
        if int(ver) == 5:
            argcmd = self.AllCommands[3]        
        else:
            argcmd = self.AllCommands[0] 
        p = subprocess.Popen(self.AllCommands[0], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
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
        
        pct1 = PCTuple(self.__respos[3][0], self.__respos[3][1], rescontent)
        self.PCList.append(pct1)
        #print(rescontent)
        
    def CheckAccountAuth(self):
        content = []
        rescontent = ""
        f = open(self.respath, "a+")
        f.write("*************************Account Authority*************************\n")           
        p = subprocess.Popen(self.AllCommands[4], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)   #"cat \/etc\/passwd"
        retval = p.wait()      
        content = CheckCommonFunc.CompatibleList(p.stdout.readlines())
        for line in content:
            rescontent = rescontent + line.rstrip()+ '\n'
            f.write(line.rstrip() + '\n')
        f.close()
        
        pct1 = PCTuple(self.__respos[4][0], self.__respos[4][1], rescontent)
        self.PCList.append(pct1)        
        #print(rescontent)
        
##############################################################      CheckUselessAccount       ########################################################################################          
    #Pass CentOS5_i386、CentOS6、CentOS7    
    def CheckUselessAccount(self):
        rescontent = ""
        bres = False        
        content = []
        p1 = subprocess.Popen(self.AllCommands[4], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p1.wait()         
        f = open(self.respath, "a+")
        f.write("*************************All Passwd*************************\n")  
        #ver = self.GetLinuxVer()
        #if int(ver) == 5:
            #content = copy.deepcopy(p1.stdout.readlines())
        #else:
            #for line in p1.stdout.readlines():
                #line = str(line, encoding = "utf-8")
                #content.append(line.rstrip())  
        content = CheckCommonFunc.CompatibleList(p1.stdout.readlines())
                
        for line in content:
            rescontent = rescontent + line.rstrip() + '\n'
            f.write(line.rstrip() + '\n')
        
        content = []
        p2 = subprocess.Popen(self.AllCommands[5], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p2.wait()
        
        f.write("*************************All Shadow*************************\n") 
        #if int(ver) == 5:
            #content = copy.deepcopy(p2.stdout.readlines())
        #else:
            #for line in p2.stdout.readlines():
                #line = str(line, encoding = "utf-8")
                #content.append(line.rstrip())
        content = CheckCommonFunc.CompatibleList(p2.stdout.readlines())
        
        for line in content:
            rescontent = rescontent + line.rstrip() + '\n'
            f.write(line.rstrip() + '\n')      
        f.close()

        pct1 = PCTuple(self.__respos[5][0], self.__respos[5][1], rescontent)
        self.PCList.append(pct1)
        #print(rescontent)

##############################################################      CheckPermitRootLogin       ########################################################################################          
    #Pass CentOS5_i386、CentOS6、CentOS7    
    def CheckPermitRootLogin(self):
        rescontent = ""
        bres = False        
        content = []
        finish = []
        p = subprocess.Popen(self.AllCommands[6], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait()   
        f = open(self.respath, "a+")
        f.write("*************************Root Login*************************\n") 
        #ver = self.GetLinuxVer()
        #if int(ver) == 5:
            #content = copy.deepcopy(p.stdout.readlines())
        #else:
            #for line in p.stdout.readlines():
                #line = str(line, encoding = "utf-8")
                #content.append(line.rstrip())
        content = CheckCommonFunc.CompatibleList(p.stdout.readlines())
                
        for line in content:
            if "PermitRootLogin" in line:
                log = line.lstrip().rstrip()
                
                #print(log)
                if(log[0] == '#'):
                    continue
                else:
                    finish.append(log)
                    rescontent = rescontent + log +'\n'
                    f.write(log + "\n")
        if(len(finish) == 0):
            rescontent = "Default setting.\n"
            bres = True
            f.write("Default setting.\n")
        #print("*************************Root Login*************************") 
        f.close()
        
        pct1 = PCTuple(self.__respos[6][0], self.__respos[6][1], rescontent)
        pct2 = PCTuple(self.__expos[6][0], self.__expos[6][1], "exist" if bres == True else "unexist")
        self.PCList.append(pct1)
        self.PCList.append(pct2)      
        #print(rescontent)
        
            
##############################################################      CheckPasswdComplexity       ########################################################################################          
    #Pass CentOS5_i386、CentOS6、CentOS7                
    def CheckPasswdComplexity(self):
        #print("CheckPasswdComplexity start...")
        rescontent = ""
        bres = False        
        #pam_passwdqc.so
        content = []
        log = ""
        state1 = False
        p1 = subprocess.Popen(self.AllCommands[7], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p1.wait()         
        f = open(self.respath, "a+")
        f.write("*************************Password Complexity Configuration*************************\n") 
        #ver = self.GetLinuxVer()
        #if int(ver) == 5:
            #content = copy.deepcopy(p.stdout.readlines())
        #else:
            #for line in p.stdout.readlines():
                #line = str(line, encoding = "utf-8")
                #content.append(line.rstrip())
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
            pct1 = PCTuple(self.__respos[7][0], self.__respos[7][1], rescontent)
            pct2 = PCTuple(self.__expos[7][0], self.__expos[7][1], "exist" if bres == True else "unexist")
            self.PCList.append(pct1)
            self.PCList.append(pct2)         
            #print(rescontent)
        
        
##############################################################      CheckPasswdComplexity       ########################################################################################          
    #Pass CentOS5_i386、CentOS6、CentOS7
    def PasswordTimeLimit(self):
        rescontent = ""
        bres = False        
        content = []
        MaxDays = 0
        p = subprocess.Popen(self.AllCommands[8], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait()
        f = open(self.respath, "a+")
        f.write("*************************Password Maxdays*************************\n")
        #ver = self.GetLinuxVer()
        #if int(ver) == 5:
            #content = copy.deepcopy(p.stdout.readlines())
        #else:
            #for line in p.stdout.readlines():
                #line = str(line, encoding = "utf-8")
                #content.append(line.rstrip())     
        content = CheckCommonFunc.CompatibleList(p.stdout.readlines())
        for line in content:
            if "PASS_MAX_DAYS" in line:
                #print(line)
                log = line.lstrip().rstrip()
                if log[0] == '#':
                    continue
                else:
                    MaxDays = int(log.split()[1])
                    break
        if MaxDays == 0:
            bres = True
            rescontent = "Default\n"
            f.write("PASS_MAX_DAYS:Default\n")
        else:
            rescontent = str(MaxDays) + "\n"
            f.write("PASS_MAX_DAYS:" + str(MaxDays) + "\n")
        f.close()
        
        pct1 = PCTuple(self.__respos[8][0], self.__respos[8][1], rescontent)
        pct2 = PCTuple(self.__expos[8][0], self.__expos[8][1], "exist" if bres == True else "unexist")
        self.PCList.append(pct1)
        self.PCList.append(pct2)         
        #print(rescontent)
            
##############################################################      AuthenFailedTimes       ########################################################################################
    #Pass CentOS5_i386、CentOS6、CentOS7
    def AuthenFailedTimes(self):
        rescontent = ""
        bres = False        
        content = []
        log = ""
        status = False
        p = subprocess.Popen(self.AllCommands[9], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait() 
        f = open(self.respath, "a+")
        f.write("*************************Authenorith Configuration*************************\n")
        #ver = self.GetLinuxVer()
        #if int(ver) == 5:
            #content = copy.deepcopy(p.stdout.readlines())
        #else:
            #for line in p.stdout.readlines():
                #line = str(line, encoding = "utf-8")
                #content.append(line.rstrip())         
        content = CheckCommonFunc.CompatibleList(p.stdout.readlines())        
        for line in content:
            if "auth" in line and \
               "required" in line and \
               "pam_tally2.so" in line and \
               line.lstrip()[0] != '#':
                log = line
                rescontent = rescontent + log.rstrip() + '\n'
                if  "deny=6" in line and \
                    "lock_time=1800" in line and \
                    "even_deny_root" in line and \
                    "root_unlock_time=1800" in line:
                    status = True
                    log = line
                else:
                    status = False
                break
        
        if status == True:
            f.write(log + "\n")
        else:
            bres = True
            rescontent = "No Setting.\n"
            f.write("Warn:There are something wrong about authentication failed times.\n")
        f.close()
        if rescontent == "":
            rescontent = "No Setting."
        pct1 = PCTuple(self.__respos[9][0], self.__respos[9][1], rescontent)
        pct2 = PCTuple(self.__expos[9][0], self.__expos[9][1], "exist" if bres == True else "unexist")
        self.PCList.append(pct1)
        self.PCList.append(pct2)      
        #print(rescontent)
            
##############################################################      PasswdHistoryTimes       ########################################################################################
    #Pass CentOS5_i386、CentOS6、CentOS7
    def PasswdHistoryTimes(self):
        rescontent = ""
        bres = False        
        content = []
        log = ""
        status = False
        p = subprocess.Popen(self.AllCommands[10], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait()             
        f = open(self.respath, "a+")
        f.write("*************************Effective Times*************************\n")
        #ver = self.GetLinuxVer()
        #if int(ver) == 5:
            #content = copy.deepcopy(p.stdout.readlines())
        #else:
            #for line in p.stdout.readlines():
                #line = str(line, encoding = "utf-8")
                #content.append(line.rstrip())         
        content = CheckCommonFunc.CompatibleList(p.stdout.readlines())  
        
        for line in content:
            if "password" in line and \
               "requisite" in line and \
               "pam_unix.so" in line and \
               line.lstrip()[0] != '#':
                log = line
                status = True
                rescontent = rescontent + line.rstrip() + '\n'
                break
        if status == True:
            f.write(log + "\n")
        else:
            bres = True
            rescontent = "No Setting.\n"
            f.write("Warn:There are something wrong about password-historical-times.\n")
        f.close()
        
        pct1 = PCTuple(self.__respos[10][0], self.__respos[10][1], rescontent)
        pct2 = PCTuple(self.__expos[10][0], self.__expos[10][1], "exist" if bres == True else "unexist")
        self.PCList.append(pct1)
        self.PCList.append(pct2)     
        #print(rescontent)
            
##############################################################      PasswdHistoryTimes       ########################################################################################
    #Pass CentOS5_i386、CentOS6、CentOS7
    def CheckVitalDirAuth(self):
        rescontent = ""
        bres = False        
        status1 = False
        status2 = False
        status3 = False
        auth = ""
        
        p1 = subprocess.Popen(self.AllCommands[11], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p1.wait()  
        f = open(self.respath, "a+")
        f.write("*************************Directory Authority*************************\n")
        ver = CheckCommonFunc.GetLinuxVer()
        #if p1.stdout.read().split()[0] == "-rw-r--r--.":
        #if int(ver) == 5:
            #auth = p1.stdout.read().rstrip().lstrip().split()[0]
        #else:
            #auth = str(p1.stdout.read(), encoding = "utf-8").split()[0].rstrip('.')
            
        auth = CheckCommonFunc.CompatibleStr(p1.stdout.read().rstrip().lstrip())
        rescontent = rescontent + auth.rstrip() + '\n'
        if ver == 5:
            auth = auth.split()[0]
        else:
            auth = auth.split()[0].rstrip('.')
        
            
        #print(str(p1.stdout.read(), encoding = "utf-8")) 如果这里加了这么一句，下面那句就会报IndexError
        #并不是因为split或者[0]有错，而是因为你一旦用过一次stdout中的内容，再取就取不到了
        if auth == "-rw-r--r--":
            status1 = True
            #f.write("Authority of /etc/passwd is correct.")
        else:
            bres = True
            f.write("Warn:/etc/passwd\n")
            
        auth = ""    
        p2 = subprocess.Popen(self.AllCommands[12], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p2.wait()
        #if p2.stdout.read().split()[0] == "-r--------.":
        #if int(ver) == 5:
            #auth = p2.stdout.read().rstrip().lstrip().split()[0]
        #else:
            #auth = str(p2.stdout.read(), encoding = "utf-8").split()[0].rstrip('.')  
        auth = CheckCommonFunc.CompatibleStr(p2.stdout.read().rstrip().lstrip())
        rescontent = rescontent + auth.rstrip() + '\n'
        if ver == 5:
            auth = auth.split()[0]
        else:
            auth = auth.split()[0].rstrip('.')     
            
        if auth == "-r--------":
            status2 = True
            #f.write("Authority of /etc/shadow is correct.")
        else:
            bres = True
            f.write("Warn:/etc/shadow\n")        
        
        auth = ""  
        p3 = subprocess.Popen(self.AllCommands[13], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p3.wait()          
        #if p3.stdout.read().split()[0] == "-rw-r--r--.":
        #if int(ver) == 5:
            #auth = p3.stdout.read().rstrip().lstrip().split()[0]
        #else:
            #auth = str(p3.stdout.read(), encoding = "utf-8").split()[0].rstrip('.')    
        auth = CheckCommonFunc.CompatibleStr(p3.stdout.read().rstrip().lstrip())
        rescontent = rescontent + auth.rstrip() + '\n'
        if ver == 5:
            auth = auth.split()[0]
        else:
            auth = auth.split()[0].rstrip('.')         
            
        if auth == "-rw-r--r--":
            status3 = True
            #f.write("Authority of /etc/group is correct.")
        else:
            bres = True
            f.write("Warn:/etc/group\n")            
       
        if status1 == True and status2 == True and  status3 == True:
            f.write("Vital directory authority correct.\n")
        f.close()
        
        pct1 = PCTuple(self.__respos[11][0], self.__respos[11][1], rescontent)
        pct2 = PCTuple(self.__expos[11][0], self.__expos[11][1], "exist" if bres == True else "unexist")
        self.PCList.append(pct1)
        self.PCList.append(pct2)      
        #print(rescontent)
        
##############################################################      PasswdHistoryTimes       ########################################################################################
    #Pass CentOS5_i386、CentOS6、CentOS7
    def CheckUmask(self):
        rescontent = ""
        bres = False        
        umask = ""
        p = subprocess.Popen(self.AllCommands[14], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait()   
        f = open(self.respath, "a+")
        f.write("*************************Umask*************************\n")
        #ver = self.GetLinuxVer()
        #if int(ver) == 5:
            #umask = p.stdout.read().rstrip().lstrip()
        #else:
            #umask = str(p.stdout.read().rstrip().lstrip(), encoding = "utf-8")
        umask = CheckCommonFunc.CompatibleStr(p.stdout.read().rstrip().lstrip())
        rescontent = rescontent + umask.rstrip() + '\n'
        if umask == "0027":
            f.write("Umask correct.\n")
        else:
            bres = True
            f.write("Warn:Umask.\n")
        f.close()
        #print(p.stdout.read().lstrip().rstrip())

        pct1 = PCTuple(self.__respos[12][0], self.__respos[12][1], rescontent)
        pct2 = PCTuple(self.__expos[12][0], self.__expos[12][1], "exist" if bres == True else "unexist")
        self.PCList.append(pct1)
        self.PCList.append(pct2)     
        #print(rescontent)
        
##############################################################      CheckRemoteLogin       ########################################################################################          
    #Pass CentOS5_i386、CentOS6、CentOS7   
    def CheckRemoteLogin(self):
        rescontent = ""
        bres = False        
        content = []
        status1 = False
        status2 = False
        p1 = subprocess.Popen(self.AllCommands[15], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p1.wait()   
        f = open(self.respath, "a+")
        f.write("*************************Remote Login*************************\n")
        #ver = self.GetLinuxVer()
        #if int(ver) == 5:
            #content = copy.deepcopy(p1.stdout.readlines())
        #else:
            #for line in p1.stdout.readlines():
                #line = str(line, encoding = "utf-8")
                #content.append(line.rstrip())  
        content = CheckCommonFunc.CompatibleList(p1.stdout.readlines())        
        for line in content:
            if line.split()[len(line.split()) - 1].rstrip() == "telnet" and "grep" not in line:
                rescontent = rescontent + line.rstrip() + '\n'
                bres = True
                status1 = True
                break
        
        content = []
        p2 = subprocess.Popen(self.AllCommands[16], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p2.wait()   
        #if int(ver) == 5:
            #content = copy.deepcopy(p2.stdout.readlines())
        #else:
            #for line in p2.stdout.readlines():
                #line = str(line, encoding = "utf-8")
                #content.append(line.rstrip())  
        content = CheckCommonFunc.CompatibleList(p2.stdout.readlines())
                
        for line in content:
            if "sshd" in line and "grep" not in line:
                status2 = True
                rescontent = rescontent + line.rstrip() + '\n'
                bres = True
                break
        if status1 == False:
            f.write("Telnet is closed.\n")
        else:
            f.write("Warn:Telnet.\n")
            
        if status2 == False:
            f.write("SSH is closed.\n")
        else:
            f.write("Warn:SSH.\n")
        f.close()
        
        pct1 = PCTuple(self.__respos[13][0], self.__respos[13][1], rescontent)
        pct2 = PCTuple(self.__expos[13][0], self.__expos[13][1], "exist" if bres == True else "unexist")
        self.PCList.append(pct1)
        self.PCList.append(pct2)   
        #print(rescontent)
    
    def CheckIPRangement(self):
        rescontent = ""
        p = subprocess.Popen(self.AllCommands[17], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait() 
        content = CheckCommonFunc.CompatibleList(p.stdout.readlines())  
        for line in content:
            try:
                if line.lstrip()[0] == '#':
                    continue
            except:
                continue
            else:
                rescontent = rescontent + line.lstrip() + '\n'
        
        content = []
        p = subprocess.Popen(self.AllCommands[18], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait()        
        content = CheckCommonFunc.CompatibleList(p.stdout.readlines()) 
        for line in content:
            try:
                if line.lstrip()[0] == '#':
                    continue
            except IndexError:
                continue
            else:
                rescontent = rescontent + line.lstrip() + '\n'    
        if rescontent.rstrip().lstrip() == "":
            rescontent = "No Setting.\n"
        pct1 = PCTuple(self.__respos[15][0], self.__respos[15][1], rescontent)
        self.PCList.append(pct1)
        #print(rescontent)        
    
##############################################################      CheckTimeout       ########################################################################################          
    #Pass CentOS5_i386、CentOS6、CentOS7   
    def CheckTimeout(self):
        rescontent = ""
        bres = False        
        timeout = ""
        p = subprocess.Popen(self.AllCommands[20], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait()   
        
        f = open(self.respath, "a+")
        f.write("*************************Timeout*************************\n")
        #ver = self.GetLinuxVer()
        #if int(ver) == 5:
            #timeout = p.stdout.read().rstrip().lstrip()
            ##print(timeout)
        #else:
            #timeout = str(p.stdout.read().rstrip().lstrip(), encoding = "utf-8")      
            ##print(timeout)
        timeout = CheckCommonFunc.CompatibleStr(p.stdout.read().rstrip().lstrip())   
        rescontent = timeout + '\n'
        try:
            int(timeout)
        except ValueError:#有的时候echo TIMEOUT会返回空值
            bres = True
            rescontent = "Default Setting.\n"
            f.write("NO TIMEOUT.\n")
        else:     
            if int(timeout.rstrip()) == 300:
                f.write("TIMEOUT correct.\n")
            else:
                bres = True
                f.write("Warn:TIMEOUT ERROR.\n")
        f.close()
    
        pct1 = PCTuple(self.__respos[16][0], self.__respos[16][1], rescontent)
        pct2 = PCTuple(self.__expos[16][0], self.__expos[16][1], "exist" if bres == True else "unexist")
        self.PCList.append(pct1)
        self.PCList.append(pct2)      
        #print(rescontent)
        
    def CheckUnnessesaryServ(self):
        rescontent = ""
        bres = False        
        content = []
        ver = CheckCommonFunc.GetLinuxVer()
        
        if ver == 6 or ver == 5:
            count = 0
            p = subprocess.Popen(self.AllCommands[24], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            retval = p.wait()              
            f = open(self.respath, "a+")
            f.write("*************************Unnessesary Server*************************\n")    
            content = CheckCommonFunc.CompatibleList(p.stdout.readlines())
            for line in content:
                #line = str(line, encoding = "utf-8")
                if count == len(self.__unnessserv):
                    break
                for serv in self.__unnessserv:
                    try:
                        line.split()[0]
                        line.split()[1]            
                    except IndexError:
                        continue
                    else:
                        if serv == line.split()[0]:
                            #print(serv)
                            rescontent = rescontent + line.rstrip() + '\n'
                            count += 1
                            status = False
                            for i in range(1, 8):
                                #print(line.split()[i])
                                if line.split()[i].split(':')[1] == "on":
                                    status = True
                                    break
                            if status == True:
                                bres = True
                                f.write("Warn:" + serv + "\n")
                            break
            f.close()
                
        if ver == 7:
            count = 0
            p = subprocess.Popen(self.AllCommands[21], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            retval = p.wait()  
            f = open(self.respath, "a+")
            f.write("*************************Unnessesary Server*************************\n")
            content = CheckCommonFunc.CompatibleList(p.stdout.readlines())
            #print(len(content))
            for line in content:
                #print(line)
                #line = str(line, encoding = "utf-8")  
                if count == len(self.__unnessserv):
                    break
                for serv in self.__unnessserv:
                    try:
                        line.split()[0]
                        line.split()[1]            
                    except IndexError:
                        continue
                    else:
                        if serv == line.split()[0]:
                            #print("line")
                            rescontent = rescontent + line.rstrip() + '\n'
                            count += 1
                            if line.split()[1] == "enabled":
                                bres = True
                                f.write("Warn:" + serv + "\n")
                            #print(line) 
                            break                            
            f.close()
            
        pct1 = PCTuple(self.__respos[17][0], self.__respos[17][1], rescontent)
        pct2 = PCTuple(self.__expos[17][0], self.__expos[17][1], "exist" if bres == True else "unexist")
        self.PCList.append(pct1)
        self.PCList.append(pct2)       
        #print(rescontent)
                
    def CheckNPTServ(self):
        rescontent = ""
        bres = False        
        status = False
        content = []
        serverlist = []
        log = ""
        p = subprocess.Popen(self.AllCommands[22], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait()      
        f = open(self.respath, "a+")
        f.write("*************************NPT Server*************************\n")
        #ver = self.GetLinuxVer()
        #if int(ver) == 5:
            #content = copy.deepcopy(p.stdout.readlines())
        #else:
            #for line in p.stdout.readlines():
                #line = str(line, encoding = "utf-8")
                #content.append(line.rstrip())    
        content = CheckCommonFunc.CompatibleList(p.stdout.readlines())        
        for line in content:
            try:
                line.split()[0]
            except IndexError:
                continue
            else:
                if line.split()[0] == "server":
                    log = line
                    rescontent = rescontent + log.rstrip() + '\n'
                    f.write(log + '\n')
                    status = True
                    
        #if status == True:
            #f.write(log + '\n')
        #else:
            #f.write("Warn:NPT.\n")
        if status == False:
            bres = True
            f.write("Warn:NPT.\n")
        f.close()
        
        pct1 = PCTuple(self.__respos[18][0], self.__respos[18][1], rescontent)
        pct2 = PCTuple(self.__expos[18][0], self.__expos[18][1], "exist" if bres == True else "unexist")
        self.PCList.append(pct1)
        self.PCList.append(pct2)         
        #print(rescontent)
            
    def CheckDNSIP(self):
        content = []
        rescontent = ""
        bres = False
        p = subprocess.Popen(self.AllCommands[23], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait()          
        content = CheckCommonFunc.CompatibleList(p.stdout.readlines())    
        for line in content:
            try:
                if line.lstrip()[0] == '#':
                    continue
            except IndexError:
                continue
            else:
                rescontent = rescontent + line.rstrip() + '\n'   
        
        pct1 = PCTuple(self.__respos[19][0], self.__respos[19][1], rescontent)
        self.PCList.append(pct1)    
        #print(rescontent)
                
def CheckCentOSRun():
    c = CheckCentOS()
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
   
    
    print("CentOS version:" + str(CheckCommonFunc.GetLinuxVer()))
    #c.CheckVitalDirAuth()
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
    except:
        flog.write("Operate Excel exception.\n")
    else:
        flog.write("Operate Excel finished.\n")
        
    flog.close()
    
def Run():
    print("CentOS running.")
    
if __name__ == "__main__":
    print("start...")
    CheckCentOSRun()
    
    