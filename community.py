#
# Student Name: Rares Popa
# Student ID  : 19159700
#
# community.py: Class which contains object models
#

from datetime import datetime

#House object
class House():

    #CONSTRUCTOR
    def __init__(self,number,suburb):
        self.residents = 1
        self.number = number
        self.suburb = suburb
        self.usage_day = []
        self.usage_kwh = []
        self.solar_day = []
        self.solar_kwh = []
        self.appliance = []

    #SETTERS

    #Adding Usage details
    def addUsage(self, date, kwh):
        #Create datetime object
        datetime_object = datetime.strptime(date, '%d %m %Y %H:%M:%S') 
        self.usage_day.append(datetime_object)
        self.usage_kwh.append(kwh)

    #Adding Usage details
    def addSolar(self, date, kwh):
        #Create datetime object
        datetime_object = datetime.strptime(date, '%d %m %Y %H:%M:%S') 
        self.solar_day.append(datetime_object)
        self.solar_kwh.append(kwh)

    #Adding new appliances
    def addAppliance(self, applicance):
        self.appliance.append(applicance)
        print("Success! Added a " + applicance.getName())

    #Updating resident information
    def changeResidents(self, amount):
        self.residents = amount

    #GETTERS

    def getNumber(self):
        return self.number

    def getSuburb(self):
        return self.suburb

    def getKwhUsage(self):
        return self.usage_kwh

    def getDateUsage(self):
        return self.usage_day

    def getKwhSolar(self):
        return self.solar_kwh

    def getDateSolar(self):
        return self.solar_day

    def getAppliance(self):
        return self.appliance

    #FUNCTIONS 

    #Check to see is appliance exists and if found
    #print out the information
    def containsAppliance(self, name):
        found = False
        for a in self.appliance:
            if a.getName().upper() == name.upper():
                print("Found: " + str(a))
                found = a
        return found

#Appliance object
class Appliance():

    #CONSTRUCTOR
    def __init__(self,name,usage,activity):
        self.name = name
        self.usage = usage
        self.activity = activity

    #GETTERS 

    def getName(self):
        return self.name

    def getActivity(self):
        return self.activity

    def getUsage(self):
        return self.usage

    #FUNCTIONS
    def showRating(self):
        #Convert activity array to float instead of string
        activityFloat = [float(i) for i in self.activity]
        #The energy E in kilowatt-hours (kWh) is equal to the power P in watts (W),
        #times the time period t in hours (hr) divided by 1000:
        summed = int(((sum(activityFloat) * float(self.usage)) / 1000.0) * 365.0)
        print("\nFound: " + str(self))
        print("       Rating: " + str(summed) + "kWh per year")

    #TOSTRING
    def __str__(self):
        activitylist = ','.join(self.activity)
        return self.name + " | " + self.usage + "W | " + activitylist