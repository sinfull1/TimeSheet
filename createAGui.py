from tkinter import *
from tkinter import font
import os
import socket
import pandas as pd
import pandas.io.formats.excel
import xlsxwriter
from pprint import pprint as pp



class manageData:  
    
    empDataBase = 'employeeList.csv'
    salarayDatabase = 'salaryDatabse.csv'
    empListSheet = 'EmployeesList'
    templateInXl = 'Template'
    excelForDisp = 'displayData.xlsx'
    
      
    def __init__(self,mainWinwdow):
          
        ##  read the databases in the background when you create the class             
        self.empList = self.empListRead()
        
        ## check for Internet
        self.checkInternet = self.is_conencted()
         
        
        ## create the GUI
       
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
    # Read the empDataBase
    #===========================================================================
    def empListRead(self):
        with open(self.empDataBase,'r') as ff:
            newDf = pd.read_csv(ff)
 #             pp (dir(newDf.index))
            return (newDf)
    
         
    #===========================================================================
    # openXlsForUpdate : open the excel file to feed monthly data
    #===========================================================================
    def openXlsForUpdate(self):
        print ('open excel here')
#         excelFile = 'template.xlsx'
#         os.startfile(excelFile)


    #===========================================================================
    # updateDatabse : update the employee salary database for data in excel
    #===========================================================================
    def updateDatabse(self):
        print('ok')
        
                

    #===========================================================================
    # addEmployee : add an employee to the employee database
    # Idea here is to open the excel to display all data from csv, and update 
    # the excel with employee list after its closed and update is clicked 
    #===========================================================================
    def changeEmpList(self):
        print('ok')
        # reset the header style of pandas
        pandas.io.formats.excel.header_style = None
        
        # write content to excel
        xlsWr = pd.ExcelWriter(self.excelForDisp) 
        self.empList.to_excel(xlsWr,self.empListSheet,index = False, header = True)
        
        # format the sheet
        wb = xlsWr.book
        ws = xlsWr.sheets[self.empListSheet]
        format = wb.add_format({'bold': True, 'font_color': 'white', 'align':'center','font_size':'14','bg_color':'blue'})
        ws.set_row(0,20,format)        
        ws.set_column('A:A',25)
        
        # save the sheet 
        xlsWr.save()    
        
        # open the file
        os.startfile(self.excelForDisp)
    #===========================================================================
         
        
              
mainWinwdow = Tk()
classObj = manageData(mainWinwdow)
print(classObj.empList)
mainWinwdow.mainloop()