#coding=utf-8

'''
以下全部是针对Apache2.4的检测方法
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

from GenExcel import PCTuple, OperExcel
import CheckCommonFunc

#4/5
class CheckRHELApache():
    
    def __init__(self):
        self.respath = "/usr/ProjectTest/res.txt"
        self.conffile = "/usr/local/apache2/conf/httpd.conf"
        self.mwpath = "/usr/ProjectTest/mwres.txt"
        self.__cmd = [
            "ps -ef|grep httpd",
            "ls -ld \/usr\/local\/apache2",
            #"ls -l /etc/httpd/conf/httpd.conf",2.2
            #"ls -l /var/log/httpd",2.2
            "ls -l /usr/local/apache2/conf/httpd.conf",
            "ls -l /usr/local/apache2/logs",
            "cat /usr/local/apache2/logs/error_log",##################5
            "apachectl -v"
        ]
        self.PCList = []
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
                    (24, 8),#10
                    (25, 8),
                    (26, 8),
                    (27, 8)]
        self.__expos = [(14 ,10), #0
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
        
        
    def CheckAccount(self):#1
        rescontent = ""
        bres = False
        content = []
        f = open(self.mwpath, "a+")
        f.write("*************************Apache Account*************************\n")
        p = subprocess.Popen(self.__cmd[0], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait()  
        content = CheckCommonFunc.CompatibleList(p.stdout.readlines()) 
        for line in content:
            if "grep" not in line.split()[-2]:
                rescontent = rescontent + line.rstrip() + '\n'
                f.write(line + '\n')
        f.close()
        if rescontent == "":
            rescontent = "No Setting."
        
        pct1 = PCTuple(self.__respos[0][0], self.__respos[0][1], rescontent)
        pct2 = PCTuple(self.__expos[0][0], self.__expos[0][1], "exist" if bres == True else "unexist")
        self.PCList.append(pct1)
        self.PCList.append(pct2)        
    
    def CheckRootAuth(self):#2
        rescontent = ""
        bres = False        
        f = open(self.mwpath, "a+")
        f.write("*************************RootDir Authority*************************\n")
        p = subprocess.Popen(self.__cmd[1], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait()  
        auth = CheckCommonFunc.CompatibleStr(p.stdout.read())
        rescontent = auth.rstrip() + '\n'
        if auth.split()[0] == "drw-------." or auth.split()[0] == "drw-------":
            pass
        else:
            bres = True
        f.write(auth + '\n')
        f.close()
        
        if rescontent == "":
            rescontent = "No Setting."
            
        pct1 = PCTuple(self.__respos[1][0], self.__respos[1][1], rescontent)
        pct2 = PCTuple(self.__expos[1][0], self.__expos[1][1], "exist" if bres == True else "unexist")
        self.PCList.append(pct1)
        self.PCList.append(pct2)         
        
    
    def CheckConfAuth(self):#3
        rescontent = ""
        bres = False
        content = []
        f = open(self.mwpath, "a+")
        f.write("*************************ConfFile Authority*************************\n")        
        p = subprocess.Popen(self.__cmd[2], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait()         
        auth = CheckCommonFunc.CompatibleStr(p.stdout.read())
        f.write(auth + '\n')
        rescontent = auth.rstrip() + '\n'
        if auth.split()[0] == "-rw-------" or auth.split()[0] == "-rw-----.":
            pass
        else:
            bres = True
            
        p = subprocess.Popen(self.__cmd[3], shell = 'True', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait()         
        content = CheckCommonFunc.CompatibleList(p.stdout.readlines())       
        for line in content:
            if line.split()[0] != "-rw-r--r--." and line.split()[0] != "-rw-r--r--.":
                bres = True
                rescontent = rescontent + line.rstrip() + '\n'
            f.write(line.rstrip().lstrip() + '\n')
        f.close()
        
        if rescontent == "":
            rescontent = "No Setting."        
        
        pct1 = PCTuple(self.__respos[2][0], self.__respos[2][1], rescontent)
        pct2 = PCTuple(self.__expos[2][0], self.__expos[2][1], "exist" if bres == True else "unexist")
        self.PCList.append(pct1)
        self.PCList.append(pct2)         
  
    def Check4(self):
        pass
    def Check5(self):
        pass
    def Check6(self):
        pass
    
    
      
    def CheckCoCurNum(self):#7
        rescontent = ""
        bres = False        
        count = 0
        f = open(self.mwpath, "a+")
        f.write("*************************Cocurrent Number*************************\n")                
        cf = open(self.conffile)
        
        while 1:
            line = cf.readline()
            #print(type(line))
            
            if not line:
                break
            if "ServerLimit" in line and line.lstrip()[0] != '#':# 
                #print(line.lstrip()[0])
                rescontent = rescontent + line.rstrip() + '\n'
                f.write(line.rstrip().lstrip() + '\n')
                count += 1
            if "MaxClient" in line and line.lstrip()[0] != '#': #
                rescontent = rescontent + line.rstrip() + '\n'
                f.write(line.rstrip().lstrip() + '\n')   
                count += 1    
                
        if rescontent == "":
            rescontent = "No Setting."
            bres = True
            
        cf.close()
        f.close()
        
        pct1 = PCTuple(self.__respos[6][0], self.__respos[6][1], rescontent)
        pct2 = PCTuple(self.__expos[6][0], self.__expos[6][1], "exist" if bres == True else "unexist")
        self.PCList.append(pct1)
        self.PCList.append(pct2)          
    
    
    def CheckMethod(self):#8 http://www.iteye.com/problems/15603
        rescontent = ""
        bres = False            
        method = ""
        flag = False
        f = open(self.mwpath, "a+")
        f.write("*************************HTTP Configuration*************************\n")          
        cf = open(self.conffile)      
        
        while 1:
            line = cf.readline()    
            if not line:
                break
            if "<LimitExcept" in line and line.lstrip()[0] != '#':# 
                method = line.lstrip().rstrip()
                rescontent = method + '\n'
                if "PUT" in method or "DELETE" in method:
                    flag = True
                break
        if flag == True:
            bres = True
            f.write("Warn:HTTP Configuration.\n")
        else:
            f.write("OK.\n")    
            
        cf.close()    
        f.close()
        
        if rescontent == "":
            rescontent = "No Setting."        
        
        pct1 = PCTuple(self.__respos[7][0], self.__respos[7][1], rescontent)
        pct2 = PCTuple(self.__expos[7][0], self.__expos[7][1], "exist" if bres == True else "unexist")
        self.PCList.append(pct1)
        self.PCList.append(pct2)         
        
        
    def CheckToken(self):#9
        rescontent = ""
        bres = False
        flag = False
        f = open(self.mwpath, "a+")
        f.write("*************************Cocurrent Number*************************\n")                
        cf = open(self.conffile)
        
        while 1:
            line = cf.readline()
            
            if not line:
                break
            if ("ServerTokens" in line) and (line.lstrip()[0] != '#'):# 
                rescontent = line.rstrip() + '\n'
                lst = line.rstrip().lstrip().split()
                num = lst.index("ServerTokens")
                if(lst[num + 1] != "Prod"):
                    flag = True
                break
            
        if flag == True:
            bres = True
            f.write("Warn:Apache Version.\n")
        else:
            f.write("OK!\n")
            
        cf.close()
        f.close()
        
        if rescontent == "":
            rescontent = "No Setting."        
        
        pct1 = PCTuple(self.__respos[8][0], self.__respos[8][1], rescontent)
        pct2 = PCTuple(self.__expos[8][0], self.__expos[8][1], "exist" if bres == True else "unexist")
        self.PCList.append(pct1)
        self.PCList.append(pct2) 
        
    
    def CheckErrorDoc(self):#10
        rescontent = ""
        bres = False
        flag = False
        f = open(self.mwpath, "a+")
        f.write("*************************Cocurrent Number*************************\n")                
        cf = open(self.conffile)
        
        while 1:
            line = cf.readline()
            
            if not line:
                break
            if ("ErrorDocument" in line) and (line.lstrip()[0] != '#'):# 
                rescontent = line.rstrip() + '\n'
                lst = line.rstrip().lstrip().split()
                num = lst.index("ErrorDocument")
                if lst[num + 1] != "403" or \
                lst[num + 1] == "404" or \
                lst[num + 1] == "500":
                    flag = True
                    break
                
        if flag == True:
            bres = True
            f.write("Warn:Error Document.\n")
        else:
            f.write("OK!\n")
            
        cf.close()
        f.close()
        
        if rescontent == "":
            rescontent = "No Setting."        
        
        pct1 = PCTuple(self.__respos[9][0], self.__respos[9][1], rescontent)
        pct2 = PCTuple(self.__expos[9][0], self.__expos[9][1], "exist" if bres == True else "unexist")
        self.PCList.append(pct1)
        self.PCList.append(pct2)        
        
   
    def CheckErrorLog(self):#11
        pass
    
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
               
    
    def CheckCGI(self):#13
        rescontent = ""
        bres = False        
        flag = False
        f = open(self.mwpath, "a+")
        f.write("*************************CGI*************************\n")                
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
            
            #try:
                #if line.lstrip()[0] == '#':
                    #continue                
            #except IndexError:
                #continue 当读到文件结束时，还没有判断if not line:break，就从被except截获了，跳转到while继续读，由于已经读到结束为值，读完了又是空，出现了死循环。
                #可以运行Windows下的范例进行参考
            
            
            if not line:
                break
            if "ScriptAlias" in line and "/cgi-bin/" in line:#  and (line.lstrip()[0] != '#')
                rescontent = rescontent + line.rstrip() + '\n'
                flag = True
                break
            if "<Directory" in line and "/usr/local/apache2/cgi-bin" in line:
                rescontent = rescontent + line.rstrip() + '\n'
                flag = True
                break                
            
        if flag == True:
            bres = True
            f.write("Warn:Error Document.\n")
        else:
            f.write("OK!\n")
            
        cf.close()
        f.close()
        
        if rescontent == "":
            rescontent = "No Setting."        
        
        pct1 = PCTuple(self.__respos[12][0], self.__respos[12][1], rescontent)
        pct2 = PCTuple(self.__expos[12][0], self.__expos[12][1], "exist" if bres == True else "unexist")
        self.PCList.append(pct1)
        self.PCList.append(pct2)           
        
    
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
    CheckApacheRun()
    