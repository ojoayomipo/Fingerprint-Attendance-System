import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import random
import pandas as pd

def update_sheet(value):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('mydata.json', scope) 
    #replace mydata.json with the name of your data file
    client = gspread.authorize(creds)
    sheetname = client.open("Raspi_data").sheet2
    
    sheetname.append_row(value)

def main():  
    data = pd.read_csv('data.csv')
    studentID = random.randint(1,5)
    
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    time = datetime.datetime.now().strftime('%H:%M')
    
    
    idlist = data.loc[:,'ID'].values.tolist()
    print(studentID)
    for index in range(len(idlist)):
        
        if idlist[index] == studentID:
#             print(index)
            studentdata = data.loc[index,:]
#         else:
#             print(index)
#             continue 
    studentdatalist = studentdata.values.tolist()
    values =[date,studentdatalist[1], studentdatalist[2], time]
    print(values)
    update_sheet(values)


if __name__ == '__main__':
    while True:
        main()
