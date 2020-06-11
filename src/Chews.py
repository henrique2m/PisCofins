import re

class Chews:
     def isMonthYear(self, string):

        newArray = re.split('-', string)

        count = len(newArray)
        
        if count != 2:
            return False
        
        modeOne = len(str(newArray[0]))
        modeTwo = len(str(newArray[1]))

        if modeOne != 2 or modeTwo != 4:
            return False

        months = ['01','02','03','04','05','06','07','08','09','10','11','12']
        
        for i in range(modeOne):
            if not newArray[0][i].isnumeric():
                return False

        countMonths = len(months)

        controller = False

        for m in range(countMonths):
            if newArray[0] == months[m]:
                controller = True
                break
        
        if not controller :
            return False 

        for y in range(modeTwo):
            if not newArray[1][y].isnumeric():
                return False

        return True