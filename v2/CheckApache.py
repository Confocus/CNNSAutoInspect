#coding=utf-8

'''
以下全部是针对Apache2.4的检测方法;以CentOS作为运行系统。

1、检查httpd.conf配置文件，检查是否使用独立帐号运行Apache，使用如下命令：
#ps –ef |grep httpd  //查看是否以独立帐号运行Apache。

2、使用ls命令查看Apache主目录权限，是否设置仅root可读写。

3、#ls -l /usr/local/apache2/conf/httpd.conf  //查看httpd.conf的权限是否设置为600；
  #ls -l /usr/local/apache2/logs/*.log  //查看日志文件的权限是否设置为644。
  
4、vi /usr/local/apache2/conf/httpd.conf
查看是否设置Apache可访问目录。

5、删除无用文件，使用如下命令：
#ls -l /usr/local/apache2/htdocs/  //查看缺省的HTML文件是否删除；
#ls -l /usr/local/apache2/cgi-bin/  //查看缺省的 CGI 脚本是否删除；
#ls -l /usr/local/apache2/manual  //查看Apache 说明文件是否删除；
#ls -l /path/to/httpd-2.2.4*   //查看源代码文件是否删除。

6、访问http://ip/xxx, xxx为存在的目录，当xxx目录下没有默认首页文件时，浏览器是否显示该目录下的可用文件列表和子目录。

7、 cat /usr/local/apache2/conf/httpd.conf
查看配置文件是否合理设置。

8、cat /usr/local/apache2/conf/httpd.conf
检查相关配置项是否包含PUT、DELETE等危险方法：
<LimitExcept GET POST > 
Deny from all
</LimitExcept>

9、cat /usr/local/apache2/conf/httpd.conf
检查“ServerTokens OS”是否修改为“ServerTokens  Prod”。

10、cat /usr/local/apache2/conf/httpd.conf
检查是否自定义403、404、500错误页面。

11、 #ls –l /usr/local/apache2/logs  //查看Apache日志文件
  #cat /usr/local/apache2/logs/error_log  //查看错误日志的内容
  
12、使用命令“apachectl -v”查看Apache版本号，与http://httpd.apache.org/download.cgi网站上的版本号进行对比，根据实际情况决定是否进行版本更新。

13、使用命令“cat /usr/local/apache2/conf/httpd.conf”查看配置文件，检查相关的配置项是否已按参考配置要求正确注释：
  #ScriptAlias /cgi-bin/ "/usr/local/apache2/cgi-bin/"
  #<Directory"/usr/local/apache2/cgi-bin">
  #AllowOverride None
  #Options None
  #Order allow,deny
  #Allow from all
  #</Directory>
  
14、 cat /usr/local/apache2/conf/httpd.conf
检查是否添加了“TraceEnable off”配置项。
'''

import os
import time
import sys

from GenExcel import PCTuple, ConstructPCTuple
from commonfunc import *

class CheckCentOSApache():
    
    def __init__(self):
        
        #self.httpditem = ["Directory", "/usr/local/apache2/cgi-bin"]
        self.httpdpath = "/usr/local/apache2/conf/httpd.conf"
        self.__cmd = [
            "ps -ef|grep httpd",
            "ls -ld \/usr\/local\/apache2",
            "ls -l /usr/local/apache2/conf/httpd.conf",
            "ls -l /usr/local/apache2/logs",
            "cat /usr/local/apache2/logs/error_log",##################5
            "apachectl -v"
        ]
        self.PCList = []
        self.LogList = []
        self.__xlpos = [(14 ,8), #0
                    (15 ,8),
                    (16, 8),
                    (17, 8),
                    (18 ,8),
                    (19, 8),#5
                    (20, 8),
                    (21, 8),
                    (22, 8),#8 
                    (23, 8),
                    (24, 8),#10
                    (25, 8),
                    (26, 8),#12
                    (27, 8)]
        self.__fgpos = [(14 ,10), #0
                   (15 ,10),
                   (16, 10),
                   (17, 10),
                   (18 ,10),
                   (19, 10),#5
                   (20, 10),
                   (21, 10),
                   (22, 10),#8 
                   (23, 10),
                   (24, 10),
                   (25, 10),
                   (26, 10),
                   (27, 10)]
        
        self.logpath, self.respath, self.xlpath = ComCreateResultFilePath()
        
        self.serverlimit = ""
        self.maxclient = ""
        self.limitexcept = ""
        self.servertokens = ""
        self.errordoc = []
        self.cigbin = []
        self.accessdir = []
        
        self.CA_Parse_HTTPD()
        
    def CA_Parse_HTTPD(self, httpdpath = "/usr/local/apache2/conf/httpd.conf"):   #httpd.conf exists in this path by default.
        '''
           CA means Check apache
           HTTPD means httpd.conf file
           long function name can avoid collision with functions in other module
        '''
        
        #result = os.popen(cmdline)  #考虑到文件可能较大，不使用管道
        #res = result.read() 
        
        with open(httpdpath, 'r') as hf:
            '''
            key items:
            "Directory", "ServerLimit", "MaxClient", "<LimitExcept", "ErrorDocument", "/usr/local/apache2/cgi-bin"
            '''
    
            for line in hf:
                if len(line.lstrip().rstrip()) == 0:
                    continue
                if line.lstrip()[0] == '#':
                    continue
                
                if "ServerLimit" in line:
                    self.serverlimit = line.rstrip()
                    continue
                if "MaxClient" in line:
                    self.maxclient = line.rstrip()
                    continue
                if "ServerTokens" in line:
                    self.servertokens = line.rstrip()
                    continue
                
                if "LimitExcept " in line:
                    self.limitexcept = line.rstrip()
                    print(self.limitexcept)
                    continue
                
                if "ErrorDocument" in line:
                    self.errordoc.append(line.rstrip())
                    continue
                
                if "/usr/local/apache2/cgi-bin" in line: 
                    if "ScriptAlias" in line:
                        self.cigbin.append(line.lstrip().rstrip())
                    elif "Directory" in line:
                        while len(line.lstrip().rstrip()) != 0 and line.lstrip()[0] != '#' and "</Directory>" not in line:
                            self.cigbin.append(line.rstrip())
                            line = hf.next() 
                        self.cigbin.append("</Directory>")
                    continue
                
                if "<Directory " in line:#"Require all granted"
                    '''http://www.jb51.net/article/64280.htm'''
                    
                    count = 0
                    bflag = False
                    
                    while len(line.lstrip().rstrip()) != 0 and line.lstrip()[0] != '#' and "</Directory>" not in line:
                        if "Require all granted" in line:
                            bflag = True
                        self.accessdir.append(line.rstrip())  
                        count += 1
                        line = hf.next()
                    self.accessdir.append("</Directory>")
                    count += 1
                    if bflag == False: #回退
                        while(count != 0):
                            self.accessdir.pop()
                            count -= 1
                    else:
                        count = 0
                        bflag = False
                
                
        
    def CA_Check_Account(self):#1
        
        logcontent = "\nApache account\n"
        xlcontent = ""
        bfragile = False
        accountset = set()
        
        #p = subprocess.Popen(self.__cmd[0], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        #retval = p.wait()  
        #content = ComCompatibleList(p.stdout.readlines())   
        result = os.popen(self.__cmd[1])  
        content = ComCompatibleList(result.readlines()) 
        
        for line in content:
            if "grep" not in line.split()[-2]:
                logcontent += line + '\n'   
                accountset.add(line.split()[0])
                
        for i in accountset:
            xlcontent += i + '\n'
            
        if len(accountset) == 0:
            xlcontent = "No account."
            
        self.LogList.append(logcontent)
        retlist = ConstructPCTuple(self, self.__xlpos[0], xlcontent, self.__fgpos[0], bfragile)
        self.PCList.append(retlist[0])         
           
    
    def CA_RootDir_Auth(self):#2
        logcontent = "\nRootDir authority:\n"
        xlcontent = ""
        bfragile = False        
        
        #p = subprocess.Popen(self.__cmd[1], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        #retval = p.wait()  
        #auth = CheckCommonFunc.CompatibleStr(p.stdout.read())
        result = os.popen(self.__cmd[1])  
        rootdirauth = ComCompatibleStr(result.readline())         
        
        logcontent += rootdirauth + '\n'
        if rootdirauth.split()[0] == "drw-------." or rootdirauth.split()[0] == "drw-------":
            pass
        else:
            bfragile = True
        
        xlcontent = rootdirauth.split()[0]
        
        self.LogList.append(logcontent)
        retlist = ConstructPCTuple(self, self.__xlpos[1], xlcontent, self.__fgpos[1], bfragile)
        self.PCList.append(retlist[0])     
        self.PCList.append(retlist[1])
        
    
    def CA_HTTPD_Logs_Auth(self):
        '''
        The authority of httpd and the authority of logs are both considered in this 
        check item, but i don't know whether it will be devided into two items. So, 
        this function consists of CA_HTTPD_Auth and CA_Logs_Auth.
        '''
        
        xlcontent, bfragile = self.CA_HTTPD_Auth()
        xlcontent += self.CA_Logs_Auth()
        
        retlist = ConstructPCTuple(self, self.__xlpos[2], xlcontent, self.__fgpos[2], bfragile)
        self.PCList.append(retlist[0])     
        self.PCList.append(retlist[1])   
        
        print(xlcontent)
        print(retlist[0][2])
        print(retlist[1][2])    
    
    def CA_HTTPD_Auth(self, cmdline = "ls -l /usr/local/apache2/conf/httpd.conf"):#3
        
        logcontent = "\nHTTPD configure authority:\n"
        xlcontent = ""
        bfragile = False         
               
        result = os.popen(cmdline)     
        httpdauth = ComCompatibleStr(result.readline())
        
        logcontent += httpdauth
        
        if httpdauth.split()[0] == "-rw-------" or httpdauth.split()[0] == "-rw-----.":
            pass
        else:
            bfragile = True
        
        xlcontent = "httpd.conf : " + httpdauth.split()[0] + '\n'
        
        self.LogList.append(logcontent)
        #retlist = ConstructPCTuple(self, self.__xlpos[2], xlcontent, self.__fgpos[2], bfragile)
        #self.PCList.append(retlist[0])     
        #self.PCList.append(retlist[1])
        
        return xlcontent, bfragile
               
        
    def CA_Logs_Auth(self, cmdline = "ls -l /usr/local/apache2/logs"):
        
        logcontent = "\nLogs authority:\n"
        xlcontent = ""
        bfragile = False         
            
        result = os.popen(cmdline)     
        content = ComCompatibleList(result.readlines())  
        
        for line in content:
            if len(line.split()) <= 2:
                continue
            logcontent += line + '\n'
            xlcontent += line.split()[-1] + ' : ' + line.split()[0] + '\n'
            
        if xlcontent == "":
            xlcontent = "No log."
            
        self.LogList.append(logcontent)
        #retlist = ConstructPCTuple(self, self.__xlpos[2], xlcontent, self.__fgpos[2], bfragile)
        #self.PCList.append(retlist[0])     
        #self.PCList.append(retlist[1])    
       
        return  xlcontent
         
    
    #def CA_LOG_Auth(self):
        #p = subprocess.Popen(self.__cmd[3], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        #retval = p.wait()         
        #content = CheckCommonFunc.CompatibleList(p.stdout.readlines())       
        #for line in content:
            #if line.split()[0] != "-rw-r--r--." and line.split()[0] != "-rw-r--r--.":
                #bres = True
                #rescontent = rescontent + line.rstrip() + '\n'
            #f.write(line.rstrip().lstrip() + '\n')
        #f.close()
        
        #if rescontent == "":
            #rescontent = "No Setting."        
        
        #pct1 = PCTuple(self.__respos[2][0], self.__respos[2][1], rescontent)
        #pct2 = PCTuple(self.__expos[2][0], self.__expos[2][1], "exist" if bres == True else "unexist")
        #self.PCList.append(pct1)
        #self.PCList.append(pct2)                 
  
    def CA_Access_Dir(self):
        
        logcontent = "\nAccess Directory:\n"
        xlcontent = ""
        bfragile = False
        
        if len(self.accessdir) == 0:
            xlcontent = "Default."
        else:
            bfragile = True
            for line in self.accessdir:
                logcontent += line + '\n'
                xlcontent += line + '\n'
                
        self.LogList.append(logcontent)
        retlist = ConstructPCTuple(self, self.__xlpos[3], xlcontent, self.__fgpos[3], bfragile)
        self.PCList.append(retlist[0])      
        
    
    def Check5(self):
        pass
    def Check6(self):
        pass
    
    
      
    def CA_Concurrent_Num(self):#7
        '''
        This function is used to parse ServerLimit and MaxClient.
        Format as follow: 
        ServerLimit 16
        MaxClient 16
        '''
        
        logcontent = "\nConcurrent number:\n"
        xlcontent = "" 
        bfragile = False
        
        logcontent += self.serverlimit + '\n'
        logcontent += self.maxclient +'\n'
        xlcontent += self.serverlimit + '\n'
        xlcontent += self.maxclient 
        
        if len(xlcontent.rstrip()) == 0:
            xlcontent = "unset"
        self.LogList.append(logcontent)
        retlist = ConstructPCTuple(self, self.__xlpos[6], xlcontent, self.__fgpos[6], bfragile)
        self.PCList.append(retlist[0])
 
    
    def CA_HTTP_Method(self):#8 http://www.iteye.com/problems/15603
        '''
        This function is used to check if dangerous methods were forbidden.
        Formate as follow:
        <LimitExcept GET HEAD POST PUT DELETE TRACE OPTIONS>
        Order Allow,Deny
        Deny from all
        </LimitExcept> 
        '''        
        
        logcontent = "\nHTTP method:\n"
        xlcontent = ""
        bfragile = False
        
        logcontent += self.limitexcept + '\n'
        for method in self.limitexcept.lstrip('<').rstrip('>').split():
            if method == "LimitExcept":
                continue
            xlcontent += method + ' '
            if "PUT" == method or "DELETE" == method:
                bfragile = True
        
        if len(xlcontent.rstrip()) == 0:
            xlcontent = "unset"
        self.LogList.append(logcontent)
        retlist = ConstructPCTuple(self, self.__xlpos[7], xlcontent, self.__fgpos[7], bfragile)
        self.PCList.append(retlist[0])
        self.PCList.append(retlist[1])        
        
        
    def CA_Server_Token(self):#9
        
        logcontent = "\nServer Tokens:\n"
        xlcontent = ""
        bfragile = False
        
        if len(self.servertokens) == 0:
            xlcontent = "unset"
        else:
            logcontent += self.servertokens
            xlcontent = self.servertokens
            num = self.servertokens.split().index("ServerTokens") 
            if self.servertokens.split()[num + 1] != "Prod":
                bfragile = True
        
        self.LogList.append(logcontent)
        retlist = ConstructPCTuple(self, self.__xlpos[8], xlcontent, self.__fgpos[8], bfragile)
        self.PCList.append(retlist[0])
        self.PCList.append(retlist[1])          
        
    
    def CA_ErrorDoc(self):#10
        '''
        This function is used to check if error webpages were customize.
        Formate as follow:
        ErrorDocument 500 http://foo.example.com/cgi-bin/tester 
        '''         
        
        logcontent = "\nError document:\n"
        xlcontent = ""
        bfragile = False
        
        for error in self.errordoc:
            logcontent += error + '\n'
        for error in self.errordoc:
            if "403" in error or "404" in error or "500" in error:
                xlcontent += error + '\n'
                bfragile = True
        
        if len(xlcontent.rstrip()) == 0:
            xlcontent = "unset"   
            
        self.LogList.append(logcontent)
        retlist = ConstructPCTuple(self, self.__xlpos[9], xlcontent, self.__fgpos[9], bfragile)
        self.PCList.append(retlist[0])
        self.PCList.append(retlist[1]) 

        
        
    def CA_Logs_ErrorLogs_Content(self):
        
        bfragile = False
        xlcontent = self.CA_Logs_Content()
        xlcontent += self.CA_ErrorLogs_Content()
        
        retlist = ConstructPCTuple(self, self.__xlpos[10], xlcontent, self.__fgpos[10], bfragile)
        self.PCList.append(retlist[0])
        
    
    def CA_Logs_Content(self, cmdline = "ls -l /usr/local/apache2/logs"):
        
        logcontent = "\nLogs content:\n"
        xlcontent = ""
        bfragile = False        
        
        result = os.popen(cmdline)     
        content = ComCompatibleList(result.readlines())  
        
        for line in content:
            logcontent += line + '\n'
        
        xlcontent = logcontent
        
        self.LogList.append(logcontent)
        return xlcontent
        
    def CA_ErrorLogs_Content(self, cmdline = "cat /usr/local/apache2/logs/error_log"):
        
        logcontent = "\nErrorlogs content:\n"
        xlcontent = ""
        bfragile = False     
        
        result = os.popen(cmdline)     
        content = ComCompatibleList(result.readlines())  
        
        for line in content:
            logcontent += line + '\n'
            
        xlcontent = logcontent
        
        return xlcontent
        
    
    def CheckApacheVer(self):#12
        rescontent = ""
        bres = False
        content = []
        f = open(self.mwpath, "a+")
        f.write("*************************Apache Version*************************\n")
        
        p = subprocess.Popen(self.__cmd[5], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait()  
        
        content = CheckCommonFunc.CompatibleList(p.stdout.readlines()) 
        
        for i in content:
            rescontent = rescontent + i.rstrip() + '\n'
            f.write(i.rstrip().lstrip() + '\n')
            
        f.close()
        
        pct1 = PCTuple(self.__respos[11][0], self.__respos[11][1], rescontent)
        self.PCList.append(pct1)
               
    
    def CA_CGI(self):#13
        '''
        This function is used to check if cgi was deleted.
        Formate as follow:
        #<Directory"/usr/local/apache2/cgi-bin">
        #AllowOverride None
        #Options None
        #Order allow,deny
        #Allow from all
        #</Directory> 
        '''         
    
        logcontent = "\nCGI:\n"        
        xlcontent = ""
        bfragile = False        
        
        for line in self.cigbin:
            logcontent += line + '\n'
        
        if len(self.cigbin) == 0:
            pass
        else:
            bfragile = True
            for line in self.cigbin:
                xlcontent += line + '\n'
        
        self.LogList.append(logcontent)
        retlist = ConstructPCTuple(self, self.__xlpos[12], xlcontent, self.__fgpos[12], bfragile)
        self.PCList.append(retlist[0])
        self.PCList.append(retlist[1])        
        
    
    def CheckTrace(self):#14
        rescontent = ""
        bres = False             
        flag = False
        f = open(self.mwpath, "a+")
        f.write("*************************Trace*************************\n")                
        cf = open(self.conffile, "r")
        
        while 1:
            line = cf.readline()
            #print(line)
            try:
                if line.lstrip()[0] == '#':
                    continue                            
            except IndexError:#读到文件结束才会有这个错误
                if(len(line) == 0):
                    break
                else:
                    continue
            if not line:
                break
            if "TraceEnable" in line:
                rescontent = line.rstrip() + '\n'
                if "off" in line:
                    flag = True
                break
            
        if flag == True:
            bres = True
            f.write("Warn:Trace.\n")
        else:
            f.write("OK!\n")
            
        cf.close()
        f.close()
        
        if rescontent == "":
            rescontent = "No Setting."        
        
        pct1 = PCTuple(self.__respos[13][0], self.__respos[13][1], rescontent)
        pct2 = PCTuple(self.__expos[13][0], self.__expos[13][1], "exist" if bres == True else "unexist")
        self.PCList.append(pct1)
        self.PCList.append(pct2)      
        
        
def CheckApacheRun():
    c = CheckRHELApache()
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
    
    try:    
        c.CheckAccount()
    except:
        flog.write("CheckAccount exception.\n")
    else:
        flog.write("CheckAccount finished.\n")    
        
    try:    
        c.CheckRootAuth()
    except:
        flog.write("CheckRootAuth exception.\n")
    else:
        flog.write("CheckRootAuth finished.\n")    
        
    try:    
        c.CheckConfAuth()
    except:
        flog.write("CheckConfAuth exception.\n")
    else:
        flog.write("CheckConfAuth finished.\n")     
    
    try:    
        c.CheckCoCurNum()
    except:
        flog.write("CheckCoCurNum exception.\n")
    else:
        flog.write("CheckCoCurNum finished.\n")     
        
    try:    
        c.CheckMethod()
    except:
        flog.write("CheckMethod exception.\n")  
    else:
        flog.write("CheckMethod finished.\n")  
        
    try:    
        c.CheckToken()
    except:
        flog.write("CheckToken exception.\n")
    else:
        flog.write("CheckToken finished.\n")  
        
    try:    
        c.CheckErrorDoc()
    except:
        flog.write("CheckErrorDoc exception.\n")
    else:
        flog.write("CheckErrorDoc finished.\n")
    
    try:    
        c.CheckErrorLog()
    except:
        flog.write("CheckErrorLog exception.\n")
    else:
        flog.write("CheckErrorLog finished.\n")
        
    try:    
        c.CheckApacheVer()
    except:
        flog.write("CheckApacheVer exception.\n")
    else:
        flog.write("CheckApacheVer finished.\n")
        
    try:    
        c.CheckCGI()
    except:
        flog.write("CheckCGI exception.\n")
    else:
        flog.write("CheckCGI finished.\n")
        
    try:    
        c.CheckTrace()
    except:
        flog.write("CheckTrace exception.\n")
    else:
        flog.write("CheckTrace finished.\n")
    
    try:
        oe = OperExcel()
        oe.FillContent("/home/wang/Desktop/centos2.xlsx", c.PCList)    
    except:
        flog.write("Operate Excel exception.\n")
    else:
        flog.write("Operate Excel finished.\n")
        
    flog.close()
    
    
if __name__ == "__main__":
    print("start...")
    c = CheckCentOSApache()
    c.CA_Logs_ErrorLogs_Content()
    