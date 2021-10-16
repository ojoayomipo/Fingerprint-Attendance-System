import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import random
import pandas as pd
import time
import board
import busio
from digitalio import DigitalInOut, Direction
import adafruit_fingerprint
import serial
uart = serial.Serial("/dev/ttyAMA0", baudrate=57600, timeout=1)

finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)


def update_sheet(value):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('mydata.json', scope) 
    #replace mydata.json with the name of your data file
    client = gspread.authorize(creds)
    sheetname = client.open("Raspi_data").sheet1
    
    sheetname.append_row(value)

def get_fingerprint():
    """Get a finger print image, template it, and see if it matches!"""
    print("Waiting for image...")
    while finger.get_image() != adafruit_fingerprint.OK:
        pass
    print("Templating...")
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        return False
    print("Searching...")
    if finger.finger_search() != adafruit_fingerprint.OK:
        return False
    return True


# pylint: disable=too-many-branches
def get_fingerprint_detail():
    """Get a finger print image, template it, and see if it matches!
    This time, print out each error instead of just returning on failure"""
    print("Getting image...", end="", flush=True)
    i = finger.get_image()
    if i == adafruit_fingerprint.OK:
        print("Image taken")
    else:
        if i == adafruit_fingerprint.NOFINGER:
            print("No finger detected")
        elif i == adafruit_fingerprint.IMAGEFAIL:
            print("Imaging error")
        else:
            print("Other error")
        return False

    print("Templating...", end="", flush=True)
    i = finger.image_2_tz(1)
    if i == adafruit_fingerprint.OK:
        print("Templated")
    else:
        if i == adafruit_fingerprint.IMAGEMESS:
            print("Image too messy")
        elif i == adafruit_fingerprint.FEATUREFAIL:
            print("Could not identify features")
        elif i == adafruit_fingerprint.INVALIDIMAGE:
            print("Image invalid")
        else:
            print("Other error")
        return False

    print("Searching...", end="", flush=True)
    i = finger.finger_fast_search()
    # pylint: disable=no-else-return
    # This block needs to be refactored when it can be tested.
    if i == adafruit_fingerprint.OK:
        print("Found fingerprint!")
        return True
    else:
        if i == adafruit_fingerprint.NOTFOUND:
            print("No match found")
        else:
            print("Other error")
        return False


def main():
    
    data = pd.read_csv('data.csv')
    
    
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    time = datetime.datetime.now().strftime('%H:%M')
    
    print("----------------")
    if finger.read_templates() != adafruit_fingerprint.OK:
        raise RuntimeError("Failed to read templates")
    print("Fingerprint templates:", finger.templates)
    print("e) enroll print")
    print("f) find print")
    print("d) delete print")
    print("----------------")
    #c = input("> ")

#     if c == "e":
#         enroll_finger(get_num())
#     if c == "f":
    if get_fingerprint():
        print("Detected #", finger.finger_id, "with confidence", finger.confidence)
        studentID = finger.finger_id
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
    else:
        print("Finger not found")
    
    


if __name__ == '__main__':
    while True:
        main()

