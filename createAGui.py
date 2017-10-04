from tkinter import *
from tkinter import font
import os
import socket
import pandas as pd
import numpy as np
import pandas.io.formats.excel
import xlsxwriter
from pprint import pprint as pp
from git import Repo,remote
from datetime import datetime as dtime


class manageData:  
    
    empDataBase = 'employeeList.csv'
    salarayDatabase = 'salaryDatabase.csv'
    empListSheet = 'EmployeesList'
    monthlyDataSheet = 'MonthlyData'
    excelForDisp = 'displayData.xlsx'
    gitHubLoc = 'git@github.com:tiger-syntex/TimeSheet.git'
    repotCheckout = 'H:\Repos\MohitYadavGitHub\TimeSheetV2\TimeSheet'

  
    def __init__(self,mainWinwdow):   
    
        ## check for Internet        
        self.checkInternet = self.is_conencted()
        
        ## if internet present , pull the latest version from net
        if self.checkInternet:
            self.gitPull()          
         
        ## define the colIndex for your database        
        self.colIndex = self.flattenMixList (['MonthlySalary',
                                             [str(x) for x in list(range(1,32))], 
                                             'Total_Days_Worked',                                        
                                             'Advance_Balance',
                                             'Advance_For_Month',
                                             'Salary_For_Month'])     
        
        ##  read the databases in the background when you create the class      
        self.currMonth = (pd.Period(dtime.now(), 'M')).strftime('%B %Y')       
        self.empList = self.empListRead() 
        
        #=======================================================================
        # ## create the GUI
        #=======================================================================
        ## Frames              
        frame = Frame(mainWinwdow,width = 400,height = 100)
        frame.pack()
        
        frame2 = Frame(mainWinwdow,width = 400,height = 100)
        frame2.pack(side = BOTTOM)        
        
        ## Font
        helv20 = font.Font(family="Helvetica",size=10,weight="bold")
        
        ## Button 1 to open excel
        self.openExlButton = Button(frame,font= helv20,text = "Feed Data",fg ='blue',command = self.openXlsForUpdate )
        self.openExlButton.place(x=5, y=5, relx=0.10,rely=0.2,height=50,width=120)
#         self.openExlButton.bind("<Button-1>",self.openXlsForUpdate)
        
        ## Button 2 to update database
        self.upDatabaseButton = Button(frame,font= helv20,text = "Update Database",fg ='red', command = self.updateDatabse)
        self.upDatabaseButton.place(x=5, y=5, relx=0.6,rely=0.2,height=50,width=120)
#         upDatabaseButton.bind("<Button-1>",self.updateDatabse) 

        ## Button 3 to  Add employee info
        self.addEmpButton = Button(frame2,font= helv20,text = "Employee List",fg ='blue',command = self.changeEmpList )
        self.addEmpButton.place(x=5, y=5, relx=0.10,rely=0.2,height=50,width=120)
        
  

        
     
     #==========================================================================
     # check if there is an Internet Connection
     #==========================================================================
    def  is_conencted(self):
        try:
            # connect to the host -- tells us if the host is actually
            # reachable
            socket.create_connection(("www.google.com", 80))
            return True
        except OSError:
            pass
        return False
    
    #===========================================================================
    # Pull the latest content from Server
    #===========================================================================
    def gitPull(self):
        repo = Repo(self.repotCheckout)
#         repo.delete_remote('origin')
#         origin = repo.create_remote('origin', self.gitHubLoc)
        origin = repo.remote(name='origin')
        origin.fetch()
        origin.pull(origin.refs[0].remote_head)

    #===========================================================================
    # Pull the latest content from Server
    #===========================================================================
    def gitCommitAndPush(self):
        repoLocal = Repo(self.repotCheckout)
        if repoLocal.is_dirty():
            repoLocal.git.add('--all')
            repoLocal.git.commit('-m','Database Updated')            
        origin = repoLocal.remote(name='origin')  
        origin.push(origin.refs[0].remote_head)
    
    
        
    #===========================================================================
    # Read the empDataBase
    #===========================================================================
    def empListRead(self):
        with open(self.empDataBase,'r') as ff:
            empDf = pd.read_csv(ff)      
        return (empDf)
     
     
     #==========================================================================
     # Read the Salary Databse
     #==========================================================================
    def salDataBaseRead (self):
        with open(self.salarayDatabase,'r') as ff:
            salaryDF = pd.DataFrame.from_csv(ff,parse_dates =False, index_col=[0,1])
#             salaryDF = pd.DataFrame.from_csv(ff, index_col=[0,1])
        return (salaryDF)     
             
             
    #===========================================================================
    # openXlsForUpdate : open the excel file to feed monthly data
    #===========================================================================
    def openXlsForUpdate(self):
        salaryDF = self.salDataBaseRead()             
        lastMonth = (pd.Period(dtime.now(), 'M') - 1).strftime('%B %Y') 
        listOfEmps = self.empList.EmployeeName.values
        
        newWayForIndex = pd.MultiIndex.from_product([listOfEmps,[self.currMonth,lastMonth]],names=['EmployeeName','Month'])
        
        # check if current month entry exists
        for (idx, row) in self.empList.iterrows():
            emps = row.loc['EmployeeName']
            sal = row.loc['Salary']        
            tupForMonth = (emps,self.currMonth)             
            if not(tupForMonth in salaryDF.index.tolist()):    
                # check if previous month entry exist
                tupForPrevMonth =  (emps,lastMonth)
                if tupForPrevMonth in  salaryDF.index.tolist():
                    # create dummy current month entry
                    salaryDF = self.addDummyEntryForDataFrame(salaryDF,emps,sal,self.currMonth)                    
                    print(emps,sal)
                else:
                    # create dummy this month and previous month entry                     
                    print(emps,sal)     
                    salaryDF = self.addDummyEntryForDataFrame(salaryDF,emps,sal,[lastMonth,self.currMonth])
                self.writeToSalDatabse(salaryDF)  
                      
        # Filter current month for displaying in excel, and for list of emps              
        extractDf = salaryDF.xs(self.currMonth,level=1)
        extractDf = extractDf.filter(listOfEmps,axis=0)
#         sorted(list())

        # Math Operations before displaying
        
        # write content to excel       
        xlsWr = pd.ExcelWriter(self.excelForDisp) 
        extractDf.to_excel(xlsWr,self.currMonth)
        xlsWr.save()   
        os.startfile(self.excelForDisp)
        
#         excelFile = 'template.xlsx'
#         os.startfile(excelFile)
    
    
    #===========================================================================
    # addDummyEntryForDataFrame :  create a dummy entry for dataframe
    #===========================================================================
    def addDummyEntryForDataFrame(self,baseFrame,empName,salary,monthsInput):
        
        if type(monthsInput) == list:
            newWayForIndex = pd.MultiIndex.from_product([[empName],monthsInput],names=['EmployeeName','Month'])
            dataEntry = self.flattenMixList([salary,np.zeros(len(self.colIndex)-1)])
            dataEntry = [np.array(dataEntry),np.array(dataEntry)]
            ndf = pd.DataFrame(dataEntry,index=newWayForIndex ,columns=self.colIndex)
            baseFrame = pd.concat([baseFrame,ndf], join='inner',).sort_index()
        else:
            newWayForIndex = pd.MultiIndex.from_product([[empName],[monthsInput]],names=['EmployeeName','Month'])
            dataEntry = [salary,np.zeros(len(colIndex)-1)]
            ndf = pd.DataFrame(dataEntry,index=self.colIndex ,columns=newWayForIndex)
            ndf = ndf.T        
            baseFrame = pd.concat([baseFrame,ndf], join='inner',).sort_index()        

        return baseFrame
        
        

    #===========================================================================
    # updateDatabse : update the employee salary database for data in excel
    #===========================================================================
    def updateDatabse(self):
               
        ## part 1 : update the employee list, based on excel
        xlFileToRead = pd.ExcelFile(self.excelForDisp)
        if xlFileToRead.sheet_names[0] == self.empListSheet:
            
            # update the employee list and Salary
            empList = pd.read_excel(self.excelForDisp,self.empListSheet)
            empList.to_csv(self.empDataBase,index = False)
            # you just wrote to the database, read it again
            self.empList = self.empListRead() 
            
        elif xlFileToRead.sheet_names[0] == self.currMonth:
            
            # read the salary database and try to drop the current month info if 
            # present,since it will be updated in the next steps
            salaryDF = self.salDataBaseRead() 
            salaryDF.drop(self.currMonth,level = 'Month',inplace=True)
            
            # read the current month data from excel and format it to be added
            salDataFromExcelForMonth = pd.read_excel(self.excelForDisp,self.currMonth,index_col=[0])
            rowMultiIndices = pd.MultiIndex.from_product([salDataFromExcelForMonth.index.values,[self.currMonth]],names=['EmployeeName','Month'])
            newDFtoadd = pd.DataFrame (salDataFromExcelForMonth.values,index=rowMultiIndices,columns=self.colIndex)
            
            # add current month data to base dataFrame
            salaryDF =  pd.concat([salaryDF,newDFtoadd], join='inner',).sort_index()   
            
            # write as csv to database            
            self.writeToSalDatabse(salaryDF)  

        else:
            print('error, xls doesnt have the data')    

        self.gitCommitAndPush()
        
        
    #===========================================================================
    # writeToSalDatabse : write to Salary Database
    #===========================================================================
    def writeToSalDatabse(self,dataFrameToWrite):
        # write as csv to database            
        toCsv = dataFrameToWrite.to_csv()
        with open(self.salarayDatabase,'w') as ff:
            ff.write(toCsv)    
            
            

    #===========================================================================
    # addEmployee : add an employee to the employee database
    # Idea here is to open the excel to display all data from csv, and update 
    # the excel with employee list after its closed and update is clicked 
    #===========================================================================
    def changeEmpList(self):
        
        self.empList = self.empListRead()
        # reset the header style of pandas
        pandas.io.formats.excel.header_style = None
        
        # write content to excel
        xlsWr = pd.ExcelWriter(self.excelForDisp) 
        self.empList.to_excel(xlsWr,self.empListSheet,index = False, header = True)
        
        # format the sheet
        wb = xlsWr.book
        ws = xlsWr.sheets[self.empListSheet]
        format = wb.add_format({'bold': True, 'font_color': 'white', 'align':'center','font_size':'12','bg_color':'blue'})
        ws.set_row(0,20,format)        
        ws.set_column('A:A',25)
        
        # save the sheet 
        xlsWr.save()    
        
        # open the file
        os.startfile(self.excelForDisp)
    #===========================================================================
         
     
     
    ## Helpers ##
    #=======================================================================
    # 
    #=======================================================================    
    def flattenMixList(self,inputList):
     final = []
     for i in inputList:
         if type(i) == list or type(i)== np.ndarray:
             for j in i:
                 final.append(j)
         else:
             final.append(i)
     return(final)        

              
mainWinwdow = Tk()
classObj = manageData(mainWinwdow)
mainWinwdow.mainloop()