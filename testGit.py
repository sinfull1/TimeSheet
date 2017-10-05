import pandas as pd
import numpy as np

##from git import Repo,remote
##
##
##def gitPull(gitHubLoc,repotCheckout):
##    repoLocal = Repo(repotCheckout)
##    origin = repo.remote(name='origin')
##    origin.fetch()
##    print(origin.refs[0])
##    #origin.pull(origin.refs[0].remote_head)
##
##gitHubLoc = 'git@github.com:tiger-syntex/TimeSheet.git'
##repotCheckout = 'H:\Repos\MohitYadavGitHub\TimeSheetV2\TimeSheet'
##gitPull(gitHubLoc,repotCheckout)
##

def flattenMixList(inputList):
 final = []
 for i in inputList:
     if type(i) == list or type(i)== np.ndarray:
         for j in i:
             final.append(j)
     else:
         final.append(i)
 return(final)     

empDataBase = 'employeeList.csv'
salarayDatabase = 'salaryDatabase.csv'
empListSheet = 'EmployeesList'
monthlyDataSheet = 'MonthlyData'
excelForDisp = 'displayData_test.xlsx'
gitHubLoc = 'git@github.com:tiger-syntex/TimeSheet.git'
repotCheckout = 'H:\Repos\MohitYadavGitHub\TimeSheetV2\TimeSheet'
currMonth = 'October 2017'

colIndex = flattenMixList (['MonthlySalary',
                                     [str(x) for x in list(range(1,32))], 
                                     'Total_Days_Worked',                                        
                                     'Advance_Balance',
                                     'Advance_For_Month',
                                     'Salary_For_Month'])  

salDataFromExcelForMonth = pd.read_excel(excelForDisp,currMonth,index_col=[0])
rowMultiIndices = pd.MultiIndex.from_product([salDataFromExcelForMonth.index.values,[currMonth]],names=['EmployeeName','Month'])
newDFtoadd = pd.DataFrame (salDataFromExcelForMonth.values,index=rowMultiIndices,columns=colIndex)
