import os
import csv
import random
import datetime
def csv_writer(data, path):
    """
    Write data to a CSV file path
    check for duplicate entries
    """
    if os.path.exists(path):
        employee_list = read_employee_data(path)
        unique_key= [e.name+str(e.phone) for e in employee_list]
        with open(path,  "a", newline="") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            for line in data:
                if (line[0]+line[4] in unique_key):
                    print("Duplicate employee")
                    continue
                else:
                    writer.writerow(line)
    else:
        with open(path,  "w", newline="") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            for line in data:
                writer.writerow(line)
        print("Wrting Done")

class Employee:
    """
    Employee Object
    """
    def __init__(self, *args):
        self.name =args[0]
        self.salary = args[1]
        self.startDate =args[2]
        if args[3] is None:
            self.endDate = '9999999'
        else:
            self.endDate = args[3]
        self.phone = args[4]
        self.time = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")

    def toString(self):
        return self.name + "," + str(self.salary) + "," + str(self.startDate) + ","+ str(self.endDate) + "," + str(self.phone)
    def toArray(self):
        return [self.name, str(self.salary), str(self.startDate),  str(self.endDate), str(self.phone), self.time]


def persist_employee_data(employee_list,csv_file_path):
        csv_writer([x.toArray() for x in employee_list], csv_file_path)


def read_employee_data(csv_file_path):
     employee_list =[]
     with open(csv_file_path, "r") as file_obj:
         reader = csv.reader(file_obj)
         for row in reader:
             e = Employee(*tuple(row))
             employee_list.append(e)
     print( "Read total of " + str(len(employee_list)) + "  employees")
     return employee_list

#def update_employee_data(csv_file_path):



def gen_rand_emp():
    employee_list =[]
    for i in range(0, 10):
        e = Employee('Employee' + str(random.randint(0, 20)), random.randint(0, 100), 20170831, None, random.randint(99,100))

        employee_list.append(e)
    return employee_list

persist_employee_data(gen_rand_emp(), os.getcwd() + "\Employee.csv")
employee_list = read_employee_data(os.getcwd() + "\Employee.csv")
[print(x.toString()) for x in employee_list]
fileobj=open(os.getcwd() + "\Employee.csv","wb+")
if not fileobj.closed:
    print("file is already opened,closing")
    fileobj.close()