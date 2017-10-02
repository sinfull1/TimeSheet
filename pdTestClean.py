import pandas as pd
import numpy as np
from pprint import pprint as pp
import datetime as baseDt
from datetime import datetime as dtime
from pprint import pprint as pp
from dIM import get_datetime_range
import json


def flattenMixList(inputList):
     final = []
     for i in inputList:
         if type(i) == list or type(i)== np.ndarray:
             for j in i:
                 final.append(j)
         else:
             final.append(i)
     return(final)        


## start of function

currentDate = dtime.now()
currentMonth = currentDate.month
currentYear= currentDate.year
dObj,dMon = get_datetime_range(currentYear, currentMonth)
# print (dObj,dMon )


## new try
emps = ['emp1','emp2']
months = ['08_2017','09_2017']
colIndex = flattenMixList (['MonthlySalary',
                                 dObj,
                                 'Advance Balance',
                                 'Balance For Month',
                                 'Total Salary'])

dataEntry = np.random.randint(10,size=(4,len(colIndex)))

allRows = pd.MultiIndex.from_tuples([ (x,y) for x in emps for y in months] )
newWayForRows = pd.MultiIndex.from_product([emps,months],names=['EmployeeName','Month'])
# dftry = pd.DataFrame(dataEntry,index=allRows ,columns=colIndex)
df2 = pd.DataFrame(dataEntry,index=newWayForRows ,columns=colIndex)
print (df2)

print (df2.xs('emp1',level=0))

extractDf = df2.xs('emp1',level=0)
extractDf = extractDf.rename({'08_2017':'10_2017','09_2017':'11_2017'})
print (extractDf)

## recreating a new multi DF and merging it
indexOfSubDF = extractDf.index
newEmpList = ['emp1','emp2','emp3']
newWayForRowsDup = pd.MultiIndex.from_product([newEmpList,indexOfSubDF.tolist()],names=['EmployeeName','Month'])
newData= np.concatenate((extractDf.values, extractDf.values,extractDf.values), axis=0)
newDF = pd.DataFrame(newData,index=newWayForRowsDup ,columns=colIndex)

## merged Info
df3 = pd.concat([df2,newDF], join='outer',).sort_index()
print (df3)

     

## lets try CSV
toCsv = df3.to_csv()
with open('database.txt','w') as ff:
    ff.write(toCsv)
    print(toCsv)


## read csv 
with open('database.txt','r') as ff:
    newDf = pd.DataFrame.from_csv(ff,index_col=[0,1])
    print(newDf)
