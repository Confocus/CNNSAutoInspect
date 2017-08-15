##coding=utf-8
import subprocess
import os
import time
import sys
import copy

from CheckLinux import *
from commonfunc import *
from GenExcel import *

class CheckRHEL(CheckLinux):
    pass

def CheckRHELRun():
    
    try:
        c = CheckRHEL()
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
    

#if __name__ == "__main__":
    #print("RHELCheck start...")
    #CheckRHELRun()