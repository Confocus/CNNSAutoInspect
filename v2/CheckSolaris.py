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
        
    def CS_Unnecessesary_Serv(self, cmdline = "svcs -a"):
        logcontent = "\nUnnecessary Service:\n"
        xlcontent = ""
        bfragile = False
        count = 0    
        
        result = os.popen(cmdline)  
        content = ComCompatibleList(result.readlines())          
        
        for line in content:
            for serv in self._CheckLinux__unnessserv:
                try:
                    line.split()[0]
                    line.split()[2]            
                except IndexError:
                    continue
                else:
                    if serv in line.split()[2]:
                        logcontent += line + '\n'
                        xlcontent += line + '\n'
                        if line.split()[0] != "disabled":
                            bfragile = True
                        break            
                    
                    
        self.LogList.append(logcontent)
        retlist = ConstructPCTuple(self.__xlpos[17], xlcontent, self.__fgpos[17], bfragile)
        self.PCList.append(retlist[0])    
        self.PCList.append(retlist[1])     
    
        print(logcontent)
        print(retlist[0][2])
        print(retlist[1][2])    
        
    def CS_(self, cmdline = "cat /etc/inet/ntp.client"):
        super(CheckSolaris, self).CL_NPT_Serv(cmdline)        
        
    def testfunc(self):
        print(self._CheckCentOS__test)#访问父类私有属性的一种方式————name mangling
        

#def CheckSolarisRun():
    #c = CheckSolaris()
    ##c.CheckUnnessesaryServ()
    #assert CheckCommonFunc.GetLinuxVer() != 0
    
    ##if os.path.exists(CheckCentOS.respath) == True:
        ##os.remove(CheckCentOS.respath)
    #if os.path.exists(c.respath) == True:
        #os.remove(c.respath)    
    #logtime = str(time.time()).replace('.', '')
    #logpath = "/usr/ProjectTest/log_" + logtime + ".txt"
    
    #if os.path.exists("/usr/ProjectTest") == False:
        #os.mkdir("/usr/ProjectTest")    
    #if os.path.exists(logpath) == True:
        #os.remove(logpath)
        
    #flog = open(logpath, "w")
   
    
    #try:    
        #c.CheckAuditLog()
    #except:
        #flog.write("CheckAuditLog exception.\n")
    #else:
        #flog.write("CheckAuditLog finished.\n")
        
    #try:    
        #c.CheckLogAuth()
    #except:
        #flog.write("CheckLogAuth exception.\n")
    #else:
        #flog.write("CheckLogAuth finished.\n")
    
    #try:
        #c.CheckNetLogServConf()
    #except:
        #flog.write("CheckNetLogServConf exception.\n")
    #else:
        #flog.write("CheckNetLogServConf finished.\n")
        
    #try:
        #c.CheckAccountAuth()
    #except:
        #flog.write("CheckAccountAuth exception.\n")
    #else:
        #flog.write("CheckAccountAuth finished.\n")    
        
    #try:    
        #c.CheckUselessAccount()
    #except:
        #flog.write("CheckUselessAccount exception.\n")
    #else:
        #flog.write("CheckUselessAccount finished.\n")   
        
    #try:    
        #c.CheckPermitRootLogin()
    #except:
        #flog.write("CheckPermitRootLogin exception.\n")
    #else:
        #flog.write("CheckPermitRootLogin finished.\n")
        
    #try:
        #c.CheckPasswdComplexity()
    #except:
        #flog.write("CheckPasswdComplexity exception.\n")
    #else:
        #flog.write("CheckPasswdComplexity finished.\n")
        
    #try:
        #c.PasswordTimeLimit()
    #except:
        #flog.write("PasswordTimeLimit exception.\n")
    #else:
        #flog.write("PasswordTimeLimit finished.\n")
        
    #try:
        #c.AuthenFailedTimes()
    #except:
        #flog.write("AuthenFailedTimes exception.\n")
    #else:
        #flog.write("AuthenFailedTimes finished.\n")
        
    #try:
        #c.PasswdHistoryTimes()
    #except:
        #flog.write("PasswdHistoryTimes exception.\n")
    #else:
        #flog.write("PasswdHistoryTimes finished.\n")
        
    #try:
        #c.CheckVitalDirAuth()
    #except:
        #flog.write("CheckVitalDirAuth exception.\n")
    #else:
        #flog.write("CheckVitalDirAuth finished.\n")
        
    #try:
        #c.CheckUmask()
    #except:
        #flog.write("CheckUmask exception.\n")
    #else:
        #flog.write("CheckUmask finished.\n")
        
    #try:
        #c.CheckRemoteLogin()
    #except:
        #flog.write("CheckRemoteLogin exception.\n")
    #else:
        #flog.write("CheckRemoteLogin finished.\n")
        
    #try:
        #c.CheckIPRangement()
    #except:
        #flog.write("CheckIPRangement exception.\n")
    #else:
        #flog.write("CheckIPRangement finished.\n")
            
    #try:
        #c.CheckTimeout()
    #except:
        #flog.write("CheckTimeout exception.\n")
    #else:
        #flog.write("CheckTimeout finished.\n")
        
    #try:
        #c.CheckUnnessesaryServ()
    #except:
        #flog.write("CheckUnnessesaryServ exception.\n")
    #else:
        #flog.write("CheckUnnessesaryServ finished.\n")
        
    #try:
        #c.CheckNPTServ()
    #except:
        #flog.write("CheckNPTServ exception.\n")
    #else:
        #flog.write("CheckNPTServ finished.\n")
        
    #try:
        #c.CheckDNSIP()
    #except:
        #flog.write("CheckDNSIP exception.\n")
    #else:
        #flog.write("CheckDNSIP finished.\n")    
    
    #try:
        #oe = OperExcel()
        #oe.FillContent("/usr/ProjectTest/centos2.xlsx", c.PCList)    
    #except:
        #flog.write("Operate Excel exception.\n")
    #else:
        #flog.write("Operate Excel finished.\n")
        
    #flog.close()


def CheckSolarisRun():
    
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


if __name__ == "__main__":
    print("start...")
    CheckSolarisRun()