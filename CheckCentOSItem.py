#coding=utf-8
import subprocess
import os
import time
import sys
import copy


##############################################################      New idea       ########################################################################################
#先判断Python的版本，覆写str()函数。再去检查Linux版本，以决定执行不同的命令



#Redhat5 = CentOS5;RedHat6 = CentOS6;CentOS7
class CheckCentOS:
    respath = "/usr/ProjectTest/res.txt"
    
    __auditlogitems = {'*.info;mail.none;authpriv.none;cron.none':'/var/log/messages',
               'authpriv.*':'/var/log/secure',
               'mail.*':'-/var/log/maillog',
               'cron.*':'/var/log/cron'}
    
    __logauthitems = ["messages",
                  "secure",
                  "maillog",
                  "cron",
                  "spooler",
                  "boot.log"]
    
    __unnessserv = ["sendmail",
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
    
    __AllCommands = ["cat \/etc\/rsyslog.conf",
                          "last \/var\/log\/wtmp",
                          "ls -l \/var\/log",
                          "cat \/etc\/syslog.conf",
                          "cat \/etc\/passwd",#5
                          "cat \/etc\/shadow",
                          "cat \/etc\/ssh\/sshd_config",
                          "cat \/etc\/pam.d\/system-auth",
                          "cat \/etc\/login.defs",
                          "cat \/etc\/pam.d\/login",#10
                          "cat \/etc\/pam.d\/system-auth",
                          "ls -l \/etc\/passwd",
                          "ls -l \/etc\/shadow",
                          "ls -l \/etc\/group",
                          "umask",#15
                          "ps -elf|grep telnet",
                          "ps -elf|grep sshd",
                          "cat \/etc\/hosts.allow",
                          "cat \/etc\/hosts.deny",
                          "cat \/etc\/hosts.deny",#20
                          "echo $TIMEOUT",
                          "systemctl list-unit-files",#use this command in CentOS7 to check unnessesary service
                          "cat \/etc\/ntp.conf",
                          "cat \/etc\/resolv.conf",
                          "chkconfig --list",#25 #use this command in CentOS6 to check unnessesary service
                          "cat \/etc\/syslog.conf"
                          ]
    
##############################################################      Just test       ########################################################################################
    def testfunc(self):
        print("This is CentOS-Check!")
    def calltestfunc(self):
        self.testfunc()
    
##############################################################      GetPyVersion       ########################################################################################
    def GetPyVersion(self):
        #print(sys.version_info)
        return sys.version_info[0]
    
    
##############################################################      GetLinuxVer       ########################################################################################
    #Pass CentOS5_i386、CentOS6、CentOS7
    def GetLinuxVer(self):#CentOS5:Python2;CentOS6:Python2;CentOS7:Python3
        count = 0
        cmd = "cat \/etc\/redhat-release"
        p = subprocess.Popen(cmd, shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait()           
        
        pyVer = self.GetPyVersion()
        if pyVer == 2:
            #print("PyVersion is 2\n")
            verinfo = p.stdout.read().rstrip().lstrip() 
        else:
            #print("PyVersion is 3\n")
            verinfo = str(p.stdout.read().rstrip().lstrip(), encoding = "utf-8") #python3中,read到的是字符object，需要转换为str object
        
        for i in verinfo.split():
            count += 1
            if i == "release":
                break        
        try:
            if count != 0:
                ver = verinfo.split()[count]
        except IndexError:
            ver = 0
        else:
            ver = ver.split(".")[0]
           
        return ver
            
            
##############################################################      CheckAuditLog       ########################################################################################          
    #Pass CentOS5_i386、CentOS6、CentOS7        
    def CheckAuditLog(self):
        ver = self.GetLinuxVer()
        AuditLogCmd = ""
        content = []
        count = 0
        finish = []   
        log = ""
        if int(ver) == 5:
            AuditLogCmd = "cat \/etc\/syslog.conf"
        else:#if ver != 5
            AuditLogCmd = "cat \/etc\/rsyslog.conf"
        
        
        p1 = subprocess.Popen(AuditLogCmd, shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)#self.__AllCommands[0]
        retval = p1.wait()  
        #p1.stdout.readlines()使用一次就会清空掉管道
        if int(ver) == 5:
            content = copy.deepcopy(p1.stdout.readlines())
        else:
            for line in p1.stdout.readlines():
                line = str(line, encoding = "utf-8")
                content.append(line.rstrip())
       
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
                    if(self.__auditlogitems[itemkey] == itemvalue):
                        count += 1
                        #print("%s:pass.The value is %s"%(itemkey, itemvalue))
                        f.write(itemkey + ":pass.The value is " + itemvalue + "\n")
                    else:
                        #print("%s:miss"%(itemkey))
                        f.write(itemkey + ":miss\n")
                    break
                    
        if(len(finish) == len(self.__auditlogitems)):
            f.write("All auditlog items were checked.\n")
        else:######################################################Warn######################################################
            #print("Uncheck:")
            #print(list(set(__auditlogitems.keys()).difference(set(finish)))) 
            f.write("Uncheck:" + ' '.join(list(set(self.__auditlogitems.keys()).difference(set(finish)))) + "\n")
        
        p2 = subprocess.Popen(self.__AllCommands[1], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p2.wait()  
        if int(ver) == 5:
            log = ''.join(p2.stdout.readlines()).rstrip().lstrip()
            #print(log)
        else:
            log = str(p2.stdout.read().lstrip().rstrip(), encoding = "utf-8")
            
        if log.strip() != "":
            #print("Log:%s"%(log))
            f.write("Log:" + log + "\n")
        else:######################################################Warn######################################################
            #print("Log:miss")
            f.write("Warn:There is no log record\n")
        f.close()
        
    
    
    
##############################################################      CheckLogAuth       ########################################################################################          
    #Pass CentOS5_i386、CentOS6、CentOS7     
    def CheckLogAuth(self):
        count = 0
        content = []
        finish = []
        p = subprocess.Popen(self.__AllCommands[2], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait()   
        #global respath
        f = open(self.respath, "a+")
        f.write("*************************Log Authority*************************\n")    
        ver = self.GetLinuxVer()
        if int(ver) == 5:
            content = copy.deepcopy(p.stdout.readlines())
        else:
            for line in p.stdout.readlines():
                line = str(line, encoding = "utf-8")
                content.append(line.rstrip())        
        
        for line in content:
            if(count == len(self.__logauthitems)):
                break            
            try:
                filename = line.split()[8]
            except IndexError:
                continue
            for item in self.__logauthitems:
                if item == filename:
                    finish.append(item)
                    count += 1
                    if(line.split()[0] == "-rw-------."):
                        #print("Authority of %s is correct"%(item))
                        f.write("Authority of " + item + " is correct.\n")
                    else:
                        #print("Warn:Authority of %s is not 600"%(item))
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
        f.close()           
        
        
        
    def CheckLogServConf(self):
        p = subprocess.Popen(self.__AllCommands[3], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait()           
        
    def CheckAccountAuth(self):
        p = subprocess.Popen(self.__AllCommands[4], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait()           
        
##############################################################      CheckUselessAccount       ########################################################################################          
    #Pass CentOS5_i386、CentOS6、CentOS7    
    def CheckUselessAccount(self):
        content = []
        p1 = subprocess.Popen(self.__AllCommands[4], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p1.wait()         
        f = open(self.respath, "a+")
        f.write("*************************All Passwd*************************\n")  
        ver = self.GetLinuxVer()
        if int(ver) == 5:
            content = copy.deepcopy(p1.stdout.readlines())
        else:
            for line in p1.stdout.readlines():
                line = str(line, encoding = "utf-8")
                content.append(line.rstrip())  
                
        for line in content:
            f.write(line.rstrip() + '\n')
        
        content = []
        p2 = subprocess.Popen(self.__AllCommands[5], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p2.wait()
        
        f.write("*************************All Shadow*************************\n") 
        if int(ver) == 5:
            content = copy.deepcopy(p2.stdout.readlines())
        else:
            for line in p2.stdout.readlines():
                line = str(line, encoding = "utf-8")
                content.append(line.rstrip())
                
        for line in content:
            f.write(line.rstrip() + '\n')      
        f.close()


##############################################################      CheckPermitRootLogin       ########################################################################################          
    #Pass CentOS5_i386、CentOS6、CentOS7    
    def CheckPermitRootLogin(self):
        content = []
        finish = []
        p = subprocess.Popen(self.__AllCommands[6], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait()   
        f = open(self.respath, "a+")
        f.write("*************************Root Login*************************\n") 
        ver = self.GetLinuxVer()
        if int(ver) == 5:
            content = copy.deepcopy(p.stdout.readlines())
        else:
            for line in p.stdout.readlines():
                line = str(line, encoding = "utf-8")
                content.append(line.rstrip())
                
        for line in content:
            if "PermitRootLogin" in line:
                log = line.lstrip().rstrip()
                #print(log)
                if(log[0] == '#'):
                    continue
                else:
                    finish.append(log)
                    f.write(log + "\n")
        if(len(finish) == 0):
            f.write("Default setting.\n")
        #print("*************************Root Login*************************") 
        f.close()
        
            
##############################################################      CheckPasswdComplexity       ########################################################################################          
    #Pass CentOS5_i386、CentOS6、CentOS7                
    def CheckPasswdComplexity(self):
        #pam_passwdqc.so
        content = []
        log = ""
        state1 = False
        p = subprocess.Popen(self.__AllCommands[7], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait()         
        f = open(self.respath, "a+")
        f.write("*************************Password Configuration*************************\n") 
        ver = self.GetLinuxVer()
        if int(ver) == 5:
            content = copy.deepcopy(p.stdout.readlines())
        else:
            for line in p.stdout.readlines():
                line = str(line, encoding = "utf-8")
                content.append(line.rstrip())
                
        for line in content:
            if "password" in line and  \
            "requisite" in line and \
            "pam_passwdqc.so" in line and\
            "enforce=everyone" in line: 
                state1 = True
        if state1 == False:
            f.write("Warn:There are problem in password-complexity setting.\n")
            f.close()
            return False
        p = subprocess.Popen(self.__AllCommands[7], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait()      
        content = []
        if int(ver) == 5:
            content = copy.deepcopy(p.stdout.readlines())
        else:
            for line in p.stdout.readlines():
                line = str(line, encoding = "utf-8")
                content.append(line.rstrip())        
                
        for line in p.stdout.readlines():
            line = str(line.rstrip().lstrip(), encoding = "utf-8")
            #print(line)
            if "pam_cracklib.so" in line and \
               "password" in line and \
               "requisite" in line and \
               "minlen=8" in line and \
               "lcredit=-1" in line and \
               "ucredit=-1" in line and \
               "ocredit=-1" in line and \
               "dcredit=-1" in line:
                state1 = True
                break
        
        if state1 == False:
            f.write("Warn:There are problem in password-complexity setting.\n")
            #f.close()
            #return False        
        else:
            f.write("Password-complexity setting correct.\n")
        f.close()
        
##############################################################      CheckPasswdComplexity       ########################################################################################          
    #Pass CentOS5_i386、CentOS6、CentOS7
    def PasswordTimeLimit(self):
        content = []
        MaxDays = 0
        p = subprocess.Popen(self.__AllCommands[8], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait()
        f = open(self.respath, "a+")
        f.write("*************************Password Maxdays*************************\n")
        ver = self.GetLinuxVer()
        if int(ver) == 5:
            content = copy.deepcopy(p.stdout.readlines())
        else:
            for line in p.stdout.readlines():
                line = str(line, encoding = "utf-8")
                content.append(line.rstrip())          
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
            f.write("PASS_MAX_DAYS:Default\n")
        else:
            f.write("PASS_MAX_DAYS:" + str(MaxDays) + "\n")
        f.close()
            
##############################################################      AuthenFailedTimes       ########################################################################################
    #Pass CentOS5_i386、CentOS6、CentOS7
    def AuthenFailedTimes(self):
        content = []
        log = ""
        status = False
        p = subprocess.Popen(self.__AllCommands[9], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait() 
        f = open(self.respath, "a+")
        f.write("*************************Authenorith Configuration*************************\n")
        ver = self.GetLinuxVer()
        if int(ver) == 5:
            content = copy.deepcopy(p.stdout.readlines())
        else:
            for line in p.stdout.readlines():
                line = str(line, encoding = "utf-8")
                content.append(line.rstrip())         
                
        for line in content:
            if "auth" in line and \
               "required" in line and \
               "pam_tally2.so" in line and \
               "deny=6" in line and \
               "lock_time=1800" in line and \
               "even_deny_root" in line and \
               "root_unlock_time=1800" in line:
                status = True
                log = line
                break
        
        if status == True:
            f.write(log + "\n")
        else:
            f.write("Warn:There are something wrong about authentication failed times.\n")
        f.close()
            
##############################################################      PasswdHistoryTimes       ########################################################################################
    #Pass CentOS5_i386、CentOS6、CentOS7
    def PasswdHistoryTimes(self):
        content = []
        log = ""
        status = False
        p = subprocess.Popen(self.__AllCommands[10], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait()             
        f = open(self.respath, "a+")
        f.write("*************************Effective Times*************************\n")
        ver = self.GetLinuxVer()
        if int(ver) == 5:
            content = copy.deepcopy(p.stdout.readlines())
        else:
            for line in p.stdout.readlines():
                line = str(line, encoding = "utf-8")
                content.append(line.rstrip())         
                
        for line in content:
            if "password" in line and \
               "requisite" in line and \
               "pam_unix.so" in line and \
               "remember" in line:
                log = line
                status = True
                break
        if status == True:
            f.write(log + "\n")
        else:
            f.write("Warn:There are something wrong about password-historical-times.\n")
        f.close()
            
            
##############################################################      PasswdHistoryTimes       ########################################################################################
    #Pass CentOS5_i386、CentOS6、CentOS7
    def CheckVitalDirAuth(self):
        status1 = False
        status2 = False
        status3 = False
        auth = ""
        
        p1 = subprocess.Popen(self.__AllCommands[11], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p1.wait()  
        f = open(self.respath, "a+")
        f.write("*************************Directory Authority*************************\n")
        ver = self.GetLinuxVer()
        #if p1.stdout.read().split()[0] == "-rw-r--r--.":
        if int(ver) == 5:
            auth = p1.stdout.read().rstrip().lstrip().split()[0]
        else:
            auth = str(p1.stdout.read(), encoding = "utf-8").split()[0].rstrip('.')  
        
        #print(str(p1.stdout.read(), encoding = "utf-8")) 如果这里加了这么一句，下面那句就会报IndexError
        #并不是因为split或者[0]有错，而是因为你一旦用过一次stdout中的内容，再取就取不到了
        if auth == "-rw-r--r--":
            status1 = True
            #f.write("Authority of /etc/passwd is correct.")
        else:
            f.write("Warn:/etc/passwd\n")
            
        auth = ""    
        p2 = subprocess.Popen(self.__AllCommands[12], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p2.wait()
        #if p2.stdout.read().split()[0] == "-r--------.":
        if int(ver) == 5:
            auth = p2.stdout.read().rstrip().lstrip().split()[0]
        else:
            auth = str(p2.stdout.read(), encoding = "utf-8").split()[0].rstrip('.')  
        if auth == "-r--------":
            status2 = True
            #f.write("Authority of /etc/shadow is correct.")
        else:
            f.write("Warn:/etc/shadow\n")        
        
        auth = ""  
        p3 = subprocess.Popen(self.__AllCommands[13], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p3.wait()          
        #if p3.stdout.read().split()[0] == "-rw-r--r--.":
        if int(ver) == 5:
            auth = p3.stdout.read().rstrip().lstrip().split()[0]
        else:
            auth = str(p3.stdout.read(), encoding = "utf-8").split()[0].rstrip('.')           
        if auth == "-rw-r--r--":
            status3 = True
            #f.write("Authority of /etc/group is correct.")
        else:
            f.write("Warn:/etc/group\n")            
       
        if status1 == True and status2 == True and  status3 == True:
            f.write("Vital directory authority correct.\n")
        f.close()
        
##############################################################      PasswdHistoryTimes       ########################################################################################
    #Pass CentOS5_i386、CentOS6、CentOS7
    def CheckUmask(self):
        umask = ""
        p = subprocess.Popen(self.__AllCommands[14], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait()   
        f = open(self.respath, "a+")
        f.write("*************************Umask*************************\n")
        ver = self.GetLinuxVer()
        if int(ver) == 5:
            umask = p.stdout.read().rstrip().lstrip()
        else:
            umask = str(p.stdout.read().rstrip().lstrip(), encoding = "utf-8")
            
        if umask == "0027":
            f.write("Umask correct.\n")
        else:
            f.write("Warn:Umask.\n")
        f.close()
        #print(p.stdout.read().lstrip().rstrip())

##############################################################      CheckRemoteLogin       ########################################################################################          
    #Pass CentOS5_i386、CentOS6、CentOS7   
    def CheckRemoteLogin(self):
        content = []
        status1 = False
        status2 = False
        p1 = subprocess.Popen(self.__AllCommands[15], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p1.wait()   
        f = open(self.respath, "a+")
        f.write("*************************Remote Login*************************\n")
        ver = self.GetLinuxVer()
        if int(ver) == 5:
            content = copy.deepcopy(p1.stdout.readlines())
        else:
            for line in p1.stdout.readlines():
                line = str(line, encoding = "utf-8")
                content.append(line.rstrip())  
                
        for line in content:
            if line.split()[len(line.split()) - 1].rstrip() == "telnet" and "grep" not in line:
                status1 = True
                break
        
        content = []
        p2 = subprocess.Popen(self.__AllCommands[16], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p2.wait()   
        if int(ver) == 5:
            content = copy.deepcopy(p2.stdout.readlines())
        else:
            for line in p2.stdout.readlines():
                line = str(line, encoding = "utf-8")
                content.append(line.rstrip())  
                
        for line in content:
            if "sshd" in line and "grep" not in line:
                status2 = True
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
    
    
    def CheckIPRangement(self):
        pass
    
##############################################################      CheckTimeout       ########################################################################################          
    #Pass CentOS5_i386、CentOS6、CentOS7   
    def CheckTimeout(self):
        timeout = ""
        p = subprocess.Popen(self.__AllCommands[20], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait()   
        
        f = open(self.respath, "a+")
        f.write("*************************Timeout*************************\n")
        ver = self.GetLinuxVer()
        if int(ver) == 5:
            timeout = p.stdout.read().rstrip().lstrip()
            #print(timeout)
        else:
            timeout = str(p.stdout.read().rstrip().lstrip(), encoding = "utf-8")      
            #print(timeout)
            
        try:
            int(timeout)
        except ValueError:#有的时候echo TIMEOUT会返回空值
            f.write("NO TIMEOUT.\n")
        else:     
            if int(timeout.rstrip()) == 300:
                f.write("TIMEOUT correct.\n")
            else:
                f.write("Warn:TIMEOUT ERROR.\n")
        f.close()
    
        
    def CheckUnnessesaryServ(self):
        ver = self.GetLinuxVer()
        if ver == 6 or ver == 5:
            count = 0
            p = subprocess.Popen(self.__AllCommands[24], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            retval = p.wait()              
            f = open(self.respath, "a+")
            f.write("*************************Unnessesary Server*************************\n")            
            for line in p.stdout.readlines():
                line = str(line, encoding = "utf-8")
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
                            count += 1
                            status = False
                            for i in range(1, 8):
                                #print(line.split()[i])
                                if line.split()[i].split(':')[1] == "on":
                                    status = True
                                    break
                            if status == True:
                                f.write("Warn:" + serv + "\n")
                            break
            f.close()
                
        if ver == 7:
            count = 0
            p = subprocess.Popen(self.__AllCommands[21], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            retval = p.wait()  
            f = open(self.respath, "a+")
            f.write("*************************Unnessesary Server*************************\n")
            for line in p.stdout.readlines():
                line = str(line, encoding = "utf-8")
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
                            count += 1
                            if line.split()[1] == "enabled":
                                f.write("Warn:" + serv + "\n")
                            #print(line) 
                            break                            
            f.close()
                
    def CheckNPTServ(self):
        status = False
        content = []
        log = ""
        p = subprocess.Popen(self.__AllCommands[22], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait()      
        f = open(self.respath, "a+")
        f.write("*************************NPT Server*************************\n")
        ver = self.GetLinuxVer()
        if int(ver) == 5:
            content = copy.deepcopy(p.stdout.readlines())
        else:
            for line in p.stdout.readlines():
                line = str(line, encoding = "utf-8")
                content.append(line.rstrip())    
                
        for line in content:
            try:
                line.split()[0]
            except IndexError:
                continue
            else:
                if line.split()[0] == "server":
                    log = line
                    status = True
                    break
        if status == True:
            f.write(log + '\n')
        else:
            f.write("Warn:NPT.\n")
        f.close()

            
    def CheckDNSIP(self):
        p = subprocess.Popen(self.__AllCommands[23], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait()          

                
if __name__ == "__main__":
    
    c = CheckCentOS()
    assert c.GetLinuxVer != 0
    
    if os.path.exists(CheckCentOS.respath) == True:
        os.remove(CheckCentOS.respath)
    logtime = str(time.time()).replace('.', '')
    logpath = "/usr/ProjectTest/log_" + logtime + ".txt"
    
    if os.path.exists("/usr/ProjectTest") == False:
        os.mkdir("/usr/ProjectTest")    
    if os.path.exists(logpath) == True:
        os.remove(logpath)
        
    flog = open(logpath, "w")
   
    
    print("CentOS version:" + str(c.GetLinuxVer()))
    #c.GetPyVersion()
    #c.CheckNPTServ()
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
        c.CheckUselessAccount()
    except:
        flog.write("CheckUselessAccount exception.\n")
        
    try:    
        c.CheckPermitRootLogin()
    except:
        flog.write("CheckUselessAccount exception.\n")
        
    try:
        c.CheckPasswdComplexity()
    except:
        flog.write("CheckPasswdComplexity exception.\n")
        
    try:
        c.PasswordTimeLimit()
    except:
        flog.write("PasswordTimeLimit exception.\n")
        
    try:
        c.AuthenFailedTimes()
    except:
        flog.write("AuthenFailedTimes exception.\n")
        
    try:
        c.PasswdHistoryTimes()
    except:
        flog.write("PasswdHistoryTimes exception.\n")
        
    try:
        c.CheckVitalDirAuth()
    except:
        flog.write("CheckVitalDirAuth exception.\n")
        
    try:
        c.CheckUmask()
    except:
        flog.write("CheckUmask exception.\n")
        
    try:
        c.CheckRemoteLogin()
    except:
        flog.write("CheckRemoteLogin exception.\n")
        
    try:
        c.CheckTimeout()
    except:
        flog.write("CheckTimeout exception.\n")
        
    try:
        c.CheckUnnessesaryServ()
    except:
        flog.write("CheckUnnessesaryServ exception.\n")
        
    try:
        c.CheckNPTServ()
    except:
        flog.write("CheckNPTServ exception.\n")
    
    flog.close()