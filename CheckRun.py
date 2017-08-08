import CheckCentOS
import CheckCommonFunc
import CheckRHEL
import CheckSolaris


if __name__ == "__main__": 
    if CheckCommonFunc.GetReleaseVer() == "":
        print("Unknow release version.")
    if CheckCommonFunc.GetReleaseVer() == "RHEL":
        CheckRHEL.CheckRHELRun()
    if CheckCommonFunc.GetReleaseVer() == "CentOS":
        CheckCentOS.CheckCentOSRun()
    if CheckCommonFunc.GetReleaseVer() == "Solaris":
        CheckSolaris.CheckSolarisRun()