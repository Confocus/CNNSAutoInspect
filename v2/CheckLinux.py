#coding=utf-8

'''
1、使用命令“cat /etc/syslog.conf”查看记录*.info;mail.none;authpriv.none;cron.none /var/log/messages
authpriv.* /var/log/secure
mail.*   /var/log/maillog 
cron.*    /var/log/cron
配置是否存在，和使用命令“last   /var/log/wtmp”查看记录是否存在日志内容。
2、使用#ls  -l  /var/log查看的目录下日志文件的权限
3、访谈系统管理员是否定期（至少3个月一次转储，并至少保存6个月）
4、使用命令“cat /etc/syslog.conf”查看：*.* @xx.xx.xx.xx（xx为服务器ip地址）参数是否正确。
5、使用命令“cat  /etc/passwd ”查看并记录系统帐户列表
6、使用命令“cat  /etc/passwd和cat  /etc/shadow”查看并记录系统帐户情况。
7、使用命令“cat   /etc/ssh/sshd_config”查看并记录PermitRootLogin配置情况。
8、使用命令“cat /etc/pam.d/passwd” 查看并记录password    requisite  pam_passwdqc.so  enforce=everyone
password   requisite  pam_cracklib.so  minlen=8 lcredit=-1 ucredit=-1 ocredit=-1 dcredit=-1   pam_stack.so
password    include      system-auth
密码复杂度配置情况。
9、使用命令“cat /etc/login.defs”查看并记录PASS_MAX_DAYS的值。
10、使用命令“cat /etc/pam.d/login”查看并记录auth      required  pam_tally2.so   deny=6  lock_time=1800 even_deny_root  root_unlock_time=1800
认证失败锁定配置。
11、使用命令“cat /etc/pam.d/passwd”查看并记录password    requisite  pam_unix.so remember的值。
12、使用命令“ls -l /etc/passwd”，“/etc/shadow”“/etc/group”查看并记录权限是否为-rw-r—r—、-r--------、-rw-r—r— 。
13、使用命令“cat  /etc/bashrc”查看并记录umask的值是否为027
14、使用命令“ps -elf|grep telnet”查看记录是否存在telnet服务进程，“ps -elf|grep ssh”查看是否存在ssh服务进程。
15、使用漏洞扫描器对linux系统进行扫描，记录是否存在未进行更新漏洞。
16、使用命令“cat  /etc/hosts.allow和/etc/hosts.deny”查看并记录相关配置。
17、使用命令“cat   /etc/profile”查看并记录是否存在TIMEOUT=300；export TIMEOUT的配置
18、使用命令chkconfig --list name查看并记录各服务使用情况。
19、使用命令“cat /etc/ntp.conf”查看ntp 的配置文件是否添加NTP服务器IP地址。
20、使用命令“cat /etc/resolv.conf”来查看DNS服务器ip地址是否为企业内部DNS服务器ip地址。
'''

import subprocess
import os
import time
import sys
import copy

from GenExcel import *
from commonfunc import *
#from XXX import XXX as XXX
'''Page1'''
##############################################################      New idea       ########################################################################################
#先判断Python的版本，覆写str()函数。再去检查Linux版本，以决定执行不同的命令

######################################idea######################################
#每一条命令作为一个功能
#除非是一条命令中提取多条作为不同的检测项




#Redhat5 = CentOS5;RedHat6 = CentOS6;CentOS7
#CentOS5、RedHat5 = syslog.conf
#CentOS6、CentOS7、RedHat6 = rsyslog.conf
class CheckLinux(object):
    
    def __init__(self):
        
        self.PCList = []
        self.LogList = []
       
        self.__xlpos = [(14 ,8), #0
                          (15 ,8),#1
                          (16, 8),
                          (17, 8),
                          (18 ,8),
                          (19, 8),#5
                          (20, 8),
                          (21, 8),
                          (22, 8),#8 
                          (23, 8),
                          (24, 8),
                          (25, 8),#11
                          (26, 8),
                          (27, 8),#13
                          (28, 8),
                          (29, 8),#15
                          (30, 8),
                          (31, 8),#17
                          (32, 8),
                          (33, 8)#19
                          ]
        
        self.__fgpos = [(14 ,10), 
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
        
        self.logpath, self.respath, self.xlpath = ComCreateResultFilePath()
        
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
    
    def CL_Syslog_Conf(self, cmdline = "/etc/syslog.conf"):
        '''
        All function name begin with "CL" which means "Check Linux"
        这里直接cat到内存，是否性能还能提升？
        '''
        
        logcontent = "\nSyslog Configuration:\n"
        xlcontent = ""
        bfragile = False
        
        ver = ComGetPyVersion()
        if ver == 6 or ver == 7:
            cmdline = "/etc/rsyslog.conf"
        
        with open(cmdline, 'r') as fsyslog:
            for line in fsyslog:
                if len(line.rstrip().lstrip()) == 0:
                    continue
                if line.rstrip()[0] == '#':
                    continue
                for item in self.__auditlogitems.keys():
                    if item in line:
                        logcontent += line
                        try:
                            itemkey = line.split()[0]
                            itemvalue = line.split()[1]
                        except IndexError:
                            continue       
                        if(self.__auditlogitems[itemkey] == itemvalue):
                            pass
                        else:
                            bfragile = True
                            xlcontent += line
                        break    
        self.LogList.append(logcontent)
        
        return xlcontent, bfragile
    
    def CL_LogRecord(self, cmdline = "last /var/log/wtmp"):
        
        logcontent = "\nLog Record:\n"
        xlcontent = ""
        bfragile = False        
        
        result = os.popen(cmdline)  
        log = ComCompatibleStr(result.read())         
        #print(log)
        if len(log.rstrip().lstrip()) == 0:
            bfragile = True
        else:
            logcontent += log
            xlcontent = log
        self.LogList.append(logcontent)
        
        return xlcontent, bfragile
            
    
    def CL_Audit_Log(self):
        
        xlcontent, bfragile = self.CL_Syslog_Conf()
        xlcontent2, bfragile2 = self.CL_LogRecord()
        
        xlcontent += xlcontent2
        bfragile = bfragile or bfragile2
        
        if xlcontent == "":
            xlcontent = "unset"
        #self.LogList.append(logcontent)
        retlist = ConstructPCTuple(self.__xlpos[0], xlcontent, self.__fgpos[0], bfragile)
        self.PCList.append(retlist[0])
        self.PCList.append(retlist[1])  
        
        
##############################################################      CheckLogAuth       ########################################################################################          
    #Pass CentOS5_i386、CentOS6、CentOS7 
    
    def CL_Logfile_Auth(self, cmdline = "ls -l /var/log"):
        
        logcontent = "\nLog file authority:\n"
        xlcontent = ""
        bfragile = False
             
        count = 0
        finish = []
        
        result = os.popen(cmdline)  
        content = ComCompatibleList(result.readlines())          
        
        for line in content:
            if(count == len(self.__logauthitems)):
                break            
            try:
                filename = line.split()[8]
            except IndexError:
                continue
            for item in self.__logauthitems:
                if item == filename:
                    logcontent += line
                    xlcontent += item + ":" + line.split()[0] + '\n'
                    finish.append(item)
                    count += 1
                    if(line.split()[0] == "-rw-------."):
                        pass
                    else:
                        bfragile = True
                    break
             
        if(len(finish) < len(self.__logauthitems)):
            bfragile = True
        
        if xlcontent == "":
            xlcontent = "unset"        
        self.LogList.append(logcontent)
        retlist = ConstructPCTuple(self.__xlpos[1], xlcontent, self.__fgpos[1], bfragile)
        self.PCList.append(retlist[0])
        self.PCList.append(retlist[1])         
        
        #print(logcontent)
        #print(retlist[0][2])
        #print(retlist[1][2])
        
        
    def CL_NetLogServer_Conf(self, cmdline = "cat /etc/syslog.conf"):
        
        logcontent = "\nNetLog Server:\n"
        xlcontent = ""
        bfragile = False
        
        ver = ComGetLinuxVer()
        if ver == 6 or ver == 7: 
            cmdline = "cat /etc/rsyslog.conf"
        
        result = os.popen(cmdline)  
        content = ComCompatibleList(result.readlines())           
        
        for line in content:
            if "*.* @" in line and line.lstrip()[0] != '#':
                logcontent += line + '\n'
                xlcontent += line + '\n'
        
        if len(xlcontent.rstrip().lstrip()) == 0:
            xlcontent = "unset."
        
        self.LogList.append(logcontent)
        retlist = ConstructPCTuple(self.__xlpos[3], xlcontent, self.__fgpos[3], bfragile)
        self.PCList.append(retlist[0])
        
        
        
        
    def CL_PasswdUser(self, cmdline = "cat /etc/passwd"):
        '''
        注册名：口令：用户标识号：组标识号：用户名：用户主目录：命令解释程序 
        This function is only used to get the user of passwd.
        '''
        
        logcontent = "\nPasswd user:\n"
        xlcontent = "passwd:"
        bfragile = False        
        userset = set()
        
        result = os.popen(cmdline)  
        content = ComCompatibleList(result.readlines())  
        
        for line in content:
            logcontent += line
            userset.add(line.split(':')[0])
        
        for i in userset:
            xlcontent += i + ';'
        xlcontent += '\n'
        
        self.LogList.append(logcontent)
        
        return xlcontent
    
    def CL_PasswdUser_Caller(self): #item 5
        '''
        Consider that PasswdUser maybe called with another function, I define this caller function 
        to parse the return of CL_PasswdUser.
        '''
        bfragile = False
        
        xlcontent = self.CL_PasswdUser()
        
        if len(xlcontent.rstrip().lstrip()) == 0:
            xlcontent = "unset."       
            
        retlist = ConstructPCTuple(self.__xlpos[4], xlcontent, self.__fgpos[4], bfragile)
        self.PCList.append(retlist[0])        
        
    
    def CL_ShadowUser(self, cmdline = "cat /etc/shadow"):
        ''' 
        This function is only used to get the user of shadow.
        ''' 
        
        logcontent = "\nShadow user:\n"
        xlcontent = "shadow:"
        bfragile = False        
        userset = set() 
        
        result = os.popen(cmdline)  
        content = ComCompatibleList(result.readlines())  
        
        for line in content:
            logcontent += line
            userset.add(line.split(':')[0])
        
        for i in userset:
            xlcontent += i + ';'
        xlcontent += '\n'    
        
        self.LogList.append(logcontent)
    
        return xlcontent    
    
    def CL_PasswdShadowUser_Caller(self):   #item 6
        
        bfragile = False
        
        xlcontent = self.CL_PasswdUser()
        xlcontent += self.CL_ShadowUser()
        
        if len(xlcontent.rstrip().lstrip()) == 0:
            xlcontent = "unset."        
        
        retlist = ConstructPCTuple(self.__xlpos[5], xlcontent, self.__fgpos[5], bfragile)
        self.PCList.append(retlist[0])        
        
                 
    #Pass CentOS5_i386、CentOS6、CentOS7    
    def CL_PermitRoot_Login(self, cmdline = "cat /etc/ssh/sshd_config"):
        logcontent = "\nPermit root login:\n"
        xlcontent = ""
        bfragile = False         
        
        result = os.popen(cmdline)  
        content = ComCompatibleList(result.readlines())         
        
        for line in content:
            if len(line.lstrip().rstrip()) == 0:
                continue
            if line.lstrip()[0] == '#':
                continue
            if "PermitRootLogin" in line:
                logcontent += line + '\n'
                xlcontent += line
                if line.split()[1] == "yes":
                    bfragile = True
                break
        
        if len(xlcontent.rstrip().lstrip()) == 0:
            xlcontent = "unset."     
            
        self.LogList.append(logcontent)
        retlist = ConstructPCTuple(self.__xlpos[6], xlcontent, self.__fgpos[6], bfragile)
        self.PCList.append(retlist[0])    
        self.PCList.append(retlist[1]) 
        
                        
    #Pass CentOS5_i386、CentOS6、CentOS7                
    def CL_Passwd_Complexity(self, cmdline = "cat /etc/pam.d/system-auth"):
        logcontent = "\nPassword complexity:\n"
        xlcontent = ""
        bfragile = False
        
        result = os.popen(cmdline)  
        content = ComCompatibleList(result.readlines())         
        
        for line in content:
            if len(line.lstrip().rstrip()) == 0:
                continue
            if line.lstrip()[0] == '#':
                continue
            if "password" in line and "requisite" in line and "pam_passwdqc.so" in line:
                logcontent += line + '\n'
                xlcontent += line + '\n'
                if "enforce=everyone" not in line:
                    bfragile = True
                continue
            if "password" in line and "requisite" in line and "pam_cracklib.so" in line:
                logcontent += line + '\n'
                xlcontent += line + '\n'
                if "minlen=8" in line and "lcredit=-1" in line and "ucredit=-1" in line and \
                   "ocredit=-1" in line and "dcredit=-1" in line:
                    pass
                else:
                    bfragile = True
                continue
            if "password" in line and "include" in line and "pam_stack.so" in line:
                logcontent += line + '\n'
                xlcontent += line + '\n'
                if "system-auth" not in line:
                    bfragile = True
                continue
        
        if len(xlcontent.rstrip().lstrip()) == 0:
            xlcontent = "unset."
            bfragile = True       
            
        self.LogList.append(logcontent)
        retlist = ConstructPCTuple(self.__xlpos[7], xlcontent, self.__fgpos[7], bfragile)
        self.PCList.append(retlist[0])    
        self.PCList.append(retlist[1]) 
        
        #print(logcontent)
        #print(retlist[0][2])
        #print(retlist[1][2])
                      
    #Pass CentOS5_i386、CentOS6、CentOS7
    def CL_Pass_Maxdays(self, cmdline = "cat /etc/login.defs"):
        
        logcontent = "\nPassword time limit:\n"
        xlcontent = ""
        bfragile = False         
    
        result = os.popen(cmdline)  
        content = ComCompatibleList(result.readlines())            
        
        for line in content:
            if len(line.lstrip().rstrip()) == 0:
                continue
            if line.lstrip()[0] == '#':
                continue
            if "PASS_MAX_DAYS" in line:
                logcontent += line + '\n'
                xlcontent += line.split()[1]
                if int(line.split()[1]) < 90:
                    bfragile = True
                break
            
        if len(xlcontent.rstrip().lstrip()) == 0:
            xlcontent = "unset."
            bfragile = True      
            
        self.LogList.append(logcontent)
        retlist = ConstructPCTuple(self.__xlpos[8], xlcontent, self.__fgpos[8], bfragile)
        self.PCList.append(retlist[0])    
        self.PCList.append(retlist[1])
        
        
    def CL_VitalFile_Auth(self):
        '''
        Parse passwd、shadow and group three file together
        '''
        
        logcontent = "\nVital file authority:\n"
        xlcontent = ""
        bfragile = False        
        
        ret = cmd_ls_l("/etc/passwd")
        logcontent += ret + '\n'
        xlcontent = "passwd:" + ret.split()[0]
        if ret.split()[0] != "-rw-r--r--" or ret.split()[0] != "-rw-r--r--.":
            bfragile = True
        
        ret = cmd_ls_l("/etc/shadow")
        logcontent += ret + '\n'
        xlcontent += "shadow:" + ret.split()[0]
        if ret.split()[0] != "-r--------" or ret.split()[0] != "-r--------.":
            bfragile = True        
        
        ret = cmd_ls_l("/etc/group")
        logcontent += ret + '\n'
        xlcontent += "group:" + ret.split()[0]
        if ret.split()[0] != "-rw-r--r--" or ret.split()[0] != "-rw-r--r--.":
            bfragile = True        
        
        if len(xlcontent.rstrip().lstrip()) == 0:
            xlcontent = "unset."     
            
        self.LogList.append(logcontent)
        retlist = ConstructPCTuple(self.__xlpos[11], xlcontent, self.__fgpos[11], bfragile)
        self.PCList.append(retlist[0])    
        self.PCList.append(retlist[1])        
        
        
    #Pass CentOS5_i386、CentOS6、CentOS7
    def CL_Authen_FailedTimes(self, cmdline = "cat /etc/pam.d/login"):
        logcontent = "\nAuthen failed times:\n"
        xlcontent = ""
        bfragile = False
    
        result = os.popen(cmdline)  
        content = ComCompatibleList(result.readlines())   
        
        for line in content:
            if len(line.lstrip().rstrip()) == 0:
                continue
            if line.lstrip()[0] == '#':
                continue
            if "auth" in line and "required" in line and "pam_tally2.so" in line:
                logcontent += line + '\n'
                xlcontent += line + '\n'           
                if  "deny=6" in line and "lock_time=1800" in line and "even_deny_root" in line and \
                    "root_unlock_time=1800" in line:    
                    pass
                else:
                    bfragile = True
        
        if len(xlcontent.rstrip().lstrip()) == 0:
            xlcontent = "unset."
            bfragile = True
            
        self.LogList.append(logcontent)
        retlist = ConstructPCTuple(self.__xlpos[9], xlcontent, self.__fgpos[9], bfragile)
        self.PCList.append(retlist[0])    
        self.PCList.append(retlist[1])   
        
        #print(logcontent)
        #print(retlist[0][2])
        #print(retlist[1][2])        
        
    def CL_Passwd_HistroyTimes(self, cmdline = "cat /etc/pam.d/passwd"):
        logcontent = "\nPassword history times:\n"
        xlcontent = ""
        bfragile = False  
        
        result = os.popen(cmdline)  
        content = ComCompatibleList(result.readlines()) 
        
        for line in content:
            if len(line.rstrip().lstrip()) == 0:
                continue
            if line.lstrip()[0] == '#':
                continue
            if "password" in line and "requisite" in line and "pam_unix.so" in line:
                logcontent += line + '\n'
                for i in line.split():
                    if "remember" in i:
                        xlcontent = i
                        if len(i.split('=')) > 1 and int(i.split('=')[1]) >= 5:
                            pass
                        else:
                            bfragile = True
                            
        if len(xlcontent.rstrip().lstrip()) == 0:
            xlcontent = "unset."
            bfragile = True
            
        self.LogList.append(logcontent)
        retlist = ConstructPCTuple(self.__xlpos[10], xlcontent, self.__fgpos[10], bfragile)
        self.PCList.append(retlist[0])    
        self.PCList.append(retlist[1])             
                        
        #print(logcontent)
        #print(retlist[0][2])
        #print(retlist[1][2])                        
            
    #Pass CentOS5_i386、CentOS6、CentOS7
    def CL_Umask(self, cmdline = "umask"):
        logcontent = "\nUmask:\n"
        xlcontent = ""
        bfragile = False  
        
        result = os.popen(cmdline)  
        umask = ComCompatibleStr(result.readline()) 
        
        logcontent += umask + '\n'
        xlcontent += umask
        
        if umask != "0027":
            bfragile = True
            
        if len(xlcontent.rstrip().lstrip()) == 0:
            xlcontent = "unset."
            bfragile = True
            
        self.LogList.append(logcontent)
        retlist = ConstructPCTuple(self.__xlpos[12], xlcontent, self.__fgpos[12], bfragile)
        self.PCList.append(retlist[0])    
        self.PCList.append(retlist[1])             
                        
             
              
    #Pass CentOS5_i386、CentOS6、CentOS7   
    def CL_Check_Serv(self, serv = "telnet"):
        logcontent = "\nTelnet service:\n"
        xlcontent = ""
        bfragile = False  
        
        cmdline = "ps -elf|grep " + serv
        
        result = os.popen(cmdline)  
        content = ComCompatibleList(result.readlines())
        for line in content:
            #print(line)
            if serv in line.split()[-1]  and "grep" not in line:
                logcontent += line + '\n'
                xlcontent += line + '\n'
                bfragile = True
        
        self.LogList.append(logcontent)
        return xlcontent, bfragile
    
    def CL_RemoteLogin_Serv(self, cmdline = ""):
        xlcontent, bfragile = self.CL_Check_Serv()
        xlcontent1, bfragile1 = self.CL_Check_Serv("ssh")
        xlcontent +='\n' + xlcontent1
        bfragile = bfragile or bfragile1
        
        if len(xlcontent.rstrip().lstrip()) == 0:
            xlcontent = "unset."
            
        retlist = ConstructPCTuple(self.__xlpos[13], xlcontent, self.__fgpos[13], bfragile)
        self.PCList.append(retlist[0])    
        self.PCList.append(retlist[1])      
    
    
    def CL_IP_Rangement(self):
        logcontent = "\nDeny and allow IP rangement:\n"
        xlcontent = ""
        bfragile = False 
        
        for line in cmd_cat("/etc/hosts.allow"):
            #print(line)
            if len(line.lstrip().rstrip()) == 0:
                continue
            if line.rstrip()[0] == "#":
                continue
            logcontent += line + '\n'
            xlcontent += line + '\n'
        
        for line in cmd_cat("/etc/hosts.allow"):
            #print(line)
            if len(line.lstrip().rstrip()) == 0:
                continue
            if line.rstrip()[0] == "#":
                continue
            logcontent += line + '\n'
            xlcontent += line + '\n'
            
        if len(xlcontent.rstrip().lstrip()) == 0:
            xlcontent = "unset."    
            
        self.LogList.append(logcontent)
        retlist = ConstructPCTuple(self.__xlpos[15], xlcontent, self.__fgpos[15], bfragile)
        self.PCList.append(retlist[0])    
        self.PCList.append(retlist[1]) 
        
        #print(logcontent)
        #print(retlist[0][2])
        #print(retlist[1][2])           
        
             
    #Pass CentOS5_i386、CentOS6、CentOS7   
    def CL_Timeout(self, cmdline = "echo $TIMEOUT"):
        logcontent = "\nDeny and allow IP rangement:\n"
        xlcontent = ""
        bfragile = False 
        
        result = os.popen(cmdline)  
        timeout = ComCompatibleStr(result.readline())
        if timeout != "300":
            bfragile = True
        
        logcontent += timeout + '\n'
        xlcontent += timeout
        
        if len(xlcontent.rstrip().lstrip()) == 0:
            xlcontent = "unset."
            
        self.LogList.append(logcontent)
        retlist = ConstructPCTuple(self.__xlpos[16], xlcontent, self.__fgpos[16], bfragile)
        self.PCList.append(retlist[0])    
        self.PCList.append(retlist[1]) 
        
        
        
    def CL_Unnecessesary_Serv(self, cmdline = "chkconfig --list"):
        logcontent = "\nUnnecessary Service:\n"
        xlcontent = ""
        bfragile = False
        count = 0
        
        ver = ComGetLinuxVer()
        
        if ver == 7:
            cmdline = "systemctl list-unit-files"
            result = os.popen(cmdline)  
            content = ComCompatibleList(result.readlines()) 
            for line in content:
                if len(line.lstrip().rstrip()) == 0:
                    break
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
                            logcontent += line + '\n'
                            count += 1
                            if line.split()[1] == "enabled":
                                xlcontent += line + '\n'
                                bfragile = True
                            break              
        else:
            result = os.popen(cmdline)  
            content = ComCompatibleList(result.readlines())    
            
            for line in content:
                if len(line.lstrip().rstrip()) == 0:
                    break
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
                            logcontent += line.rstrip() + '\n'
                            count += 1
                            for i in range(1, 8):
                                if line.split()[i].split(':')[1] == "on":
                                    xlcontent += line + '\n'
                                    bfragile = True
                                    break
                            break               
        
        if len(xlcontent.rstrip().lstrip()) == 0:
            xlcontent = "unset."        
        
        self.LogList.append(logcontent)
        retlist = ConstructPCTuple(self.__xlpos[17], xlcontent, self.__fgpos[17], bfragile)
        self.PCList.append(retlist[0])    
        self.PCList.append(retlist[1])  
        
            
        
                
    def CL_NPT_Serv(self, cmdline = "cat /etc/ntp.conf"):
        logcontent = "\nNTP Service:\n"
        xlcontent = ""
        bfragile = False
        
        result = os.popen(cmdline)  
        content = ComCompatibleList(result.readlines()) 
        
        for line in content:
            if len(line.rstrip().lstrip()) == 0:
                continue
            if line.lstrip()[0] == '#':
                continue
            if line.split()[0] == "server":
                logcontent += line + '\n'
                xlcontent += line + '\n'
                
        if len(xlcontent.rstrip().lstrip()) == 0:
            xlcontent = "unset."
            bfragile = True
            
        self.LogList.append(logcontent)
        retlist = ConstructPCTuple(self.__xlpos[18], xlcontent, self.__fgpos[18], bfragile)
        self.PCList.append(retlist[0])    
        self.PCList.append(retlist[1])    
        
        #print(logcontent)
        #print(retlist[0][2])
        #print(retlist[1][2])            
        
        
    def CL_DNS_IP(self, cmdline = "cat /etc/resolv.conf"):
        
        logcontent = "\nDNS resolv conf:\n"
        xlcontent = ""
        bfragile = False     
        
        result = os.popen(cmdline)  
        content = ComCompatibleList(result.readlines()) 
        
        for line in content:
            if len(line.rstrip().lstrip()) == 0:
                continue
            if line.lstrip()[0] == '#':
                continue
            logcontent += line + '\n'
            xlcontent += line +'\n'
            
        if len(xlcontent.rstrip().lstrip()) == 0:
            xlcontent = "unset."
            bfragile = True
            
        self.LogList.append(logcontent)
        retlist = ConstructPCTuple(self.__xlpos[19], xlcontent, self.__fgpos[19], bfragile)
        self.PCList.append(retlist[0])    
        self.PCList.append(retlist[1])           
        
        #print(logcontent)
        #print(retlist[0][2])
        #print(retlist[1][2])        
        
    def CL_GenTxtLog(self):
        with open(self.respath, 'w') as ftxt:
            for line in self.LogList:
                ftxt.write(line)        
                
def CheckLinuxRun():
    
    try:
        c = CheckLinux()
    except CommonNoExcelTemplate as e:
        print("NoExcelTemplate exception:" + repr(e) + "\n")
        sys.exit(0)    
    else:
        print("Load excel template success.\n")
        
        
    assert ComGetLinuxVer() != 0
    
    if os.path.exists(c.respath) == True:
        os.remove(c.respath)         
    
    with open(c.logpath, 'w') as flog:
        
        try:    
            c.CL_Audit_Log()
        except Exception as e:
            flog.write("CheckAuditLog exception:" + repr(e) + "\n")
        else:
            flog.write("CheckAuditLog finished.\n") 
            
        try:    
            c.CL_Logfile_Auth()
        except Exception as e:
            flog.write("CheckLogFileAuth exception:" + repr(e) + "\n")
        else:
            flog.write("CheckLogFileAuth finished.\n")             
            
        try:    
            c.CL_NetLogServer_Conf()
        except Exception as e:
            flog.write("CheckNetLogServer exception:" + repr(e) + "\n")
        else:
            flog.write("CheckNetLogServer finished.\n")             
            
        try:    
            c.CL_PasswdUser_Caller()
        except Exception as e:
            flog.write("CheckPasswdUser exception:" + repr(e) + "\n")
        else:
            flog.write("CheckPasswdUser finished.\n") 
            
        try:    
            c.CL_PasswdShadowUser_Caller()
        except Exception as e:
            flog.write("CheckPasswdShadowUser exception:" + repr(e) + "\n")
        else:
            flog.write("CheckPasswdShadowUser finished.\n")             
            
        try:    
            c.CL_PermitRoot_Login()
        except Exception as e:
            flog.write("CheckPermitRoot exception:" + repr(e) + "\n")
        else:
            flog.write("CheckPermitRoot finished.\n")         
            
        try:    
            c.CL_Passwd_Complexity()
        except Exception as e:
            flog.write("CheckPasswdComplexity exception:" + repr(e) + "\n")
        else:
            flog.write("CheckPasswdComplexity finished.\n")  
            
        try:    
            c.CL_Pass_Maxdays()
        except Exception as e:
            flog.write("CheckPasswdMaxdays exception:" + repr(e) + "\n")
        else:
            flog.write("CheckPasswdMaxdays finished.\n")        
            
        try:    
            c.CL_Authen_FailedTimes()
        except Exception as e:
            flog.write("CheckAuthenFailedTimes exception:" + repr(e) + "\n")
        else:
            flog.write("CheckAuthenFailedTimes finished.\n")    
            
        try:    
            c.CL_Passwd_HistroyTimes()
        except Exception as e:
            flog.write("CheckPasswdHistoryTimes exception:" + repr(e) + "\n")
        else:
            flog.write("CheckPasswdHistoryTimes finished.\n") 
            
        try:    
            c.CL_VitalFile_Auth()
        except Exception as e:
            flog.write("CheckVitalFileAuth exception:" + repr(e) + "\n")
        else:
            flog.write("CheckVitalFileAuth finished.\n") 
            
        try:    
            c.CL_Umask()
        except Exception as e:
            flog.write("CheckUmask exception:" + repr(e) + "\n")
        else:
            flog.write("CheckUmask finished.\n") 
            
        try:    
            c.CL_RemoteLogin_Serv()
        except Exception as e:
            flog.write("CheckRemoteLoginService exception:" + repr(e) + "\n")
        else:
            flog.write("CheckRemoteLoginService finished.\n")             
            
        try:    
            c.CL_IP_Rangement()
        except Exception as e:
            flog.write("CheckIPRangement exception:" + repr(e) + "\n")
        else:
            flog.write("CheckIPRangement finished.\n") 
            
        try:    
            c.CL_Timeout()
        except Exception as e:
            flog.write("CheckTimeout exception:" + repr(e) + "\n")
        else:
            flog.write("CheckTimeout finished.\n")
            
        try:    
            c.CL_Unnecessesary_Serv()
        except Exception as e:
            flog.write("CheckUnnecessaryService exception:" + repr(e) + "\n")
        else:
            flog.write("CheckUnnecessaryService finished.\n")  
            
        try:    
            c.CL_NPT_Serv()
        except Exception as e:
            flog.write("CheckNPTService exception:" + repr(e) + "\n")
        else:
            flog.write("CheckNPTService finished.\n") 
            
        try:    
            c.CL_DNS_IP()
        except Exception as e:
            flog.write("CheckDNSService exception:" + repr(e) + "\n")
        else:
            flog.write("CheckDNSService finished.\n")   
            
        try:
            FillContent(c.xlpath, c.PCList)
        except Exception as e:
            flog.write("Operate Excel exception:" + repr(e) + "\n")
        else:
            flog.write("Operate Excel finished.\n")             
            
    c.CL_GenTxtLog()
    
def Run():
    print("CentOS running.")
    
if __name__ == "__main__":
    print("LinuxCheck start...")
    CheckLinuxRun()
    
