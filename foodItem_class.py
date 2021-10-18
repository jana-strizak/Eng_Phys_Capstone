# //==============================//
# // Haley Glavina - October 2019 //
# // Handy Pantry User Interface  //
# //==============================//

# This program defines all the foodItem class to be referenced amongst Handy Pantry UI files.

from datetime import date
#from PIL import Image
from math import floor

class foodItem():
    def __init__(self):
        self.name = ""
        self.foodGrp = 3
        self.expDate = None
        self.img = None
        self.inDate = date.today()
        self.expDate = date(1, 1, 1)
        self.templateNum = None

    # Changes the expiry date
    def setExpiry(fooditem,year,month,day):
        fooditem.expDate = date(year,month,day)
        return

    # Determines how long an item has until expiry
    def timeTilExpiry(fooditem):
        # timeLeft = [year, month, day]
        timeLeft = [0, 0, 0]
        timeLeft[2] = (fooditem.expDate - fooditem.inDate).days
        #print("Tot days left: ", timeLeft[2])
        currYear = (date.today()).year

        # Determine years left until expiry
        if timeLeft[2] > 365:
            timeLeft[0] = floor(timeLeft[2]/365.0)

        # Determine days and months left until expiry
        timeLeft[2] = timeLeft[2]%365 - 1
        #print("Days before subbing out months: ", timeLeft[2])
        daysInMonth = [31,29,31,30,31,30,31,31,30,31,30,31]
        # j is the index of the current month
        j = (date.today()).month - 1

        # Determine if expiry is at least one month in the future from the jth month. If so, increment months til expiry, and decrement days til expiry by the number of days in the jth month.
        for i in range(12):
            if j==12:
                j = 0
            if (timeLeft[2] > daysInMonth[j]):
                timeLeft[1] += 1
                #print("Month: ", timeLeft[1])
                if (i == 2 & (currYear % 4)):
                    timeLeft[2] = timeLeft[2] - 28
                else:
                    timeLeft[2] = timeLeft[2] - daysInMonth[j]
                    #print("Days after subbing a month: ", timeLeft[2])
            j+=1

        return timeLeft


    # Returns true if an item is expired
    def isExpired(fooditem):
        return ((fooditem.expDate - date.today()).days < 0)

    # Adds a date object to the current date. Returns their sum as a date object.
    def addDate(dateDiff):
        td = date.today()
        mth = 0
        dy = td.day + dateDiff.day

        daysInMonth = [31,29,31,30,31,30,31,31,30,31,30,31]
        # Determine day sum, incrementing the months sum if the days are greater than a month 
        while (dy > daysInMonth[td.month]):
            dy = dy - daysInMonth[(td.month + mth) % 12]
            mth +=1

        # Sum months and years
        mth = mth + td.month + dateDiff.month
        yr = td.year + dateDiff.year + floor(mth/13)
        if (mth > 12):
            mth = mth % 12

        return date(yr,mth,dy)



