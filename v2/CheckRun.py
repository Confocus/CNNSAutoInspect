from CheckCentOS import *
from CheckRHEL import *
from CheckSolaris import *
from commonfunc import *

if __name__ == "__main__": 
    
    if ComGetReleaseVer() == "":
        print("Unknow release version.")
    if ComGetReleaseVer() == "RHEL":
        CheckRHELRun()
    if ComGetReleaseVer() == "CentOS":
        CheckCentOSRun()
    if ComGetReleaseVer() == "Solaris":
        CheckSolarisRun()