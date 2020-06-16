# Artifical Intelligence: Homework 1 - Behavior Trees
# September 26, 2019
# Casey Culligan and Ercan Sen
# Filename: roomba.py
# Purpose: Program that simulates a Roomba, using a pre-defined behavior tree

import random

# Used global variables to represent regular spot cleaning and dusty spot 
# cleaning (inside the general cleaning) cycles
SPOT_TIME = 20
SPOT_GENERAL_TIME = 35


class Roomba:
    # Represented the blackboard as a dictionary which initially sets the 
    # default values for the 5 keys in it
    blackboard = {
        "BATTERY_LEVEL" : 100,
        "SPOT" : False,
        "GENERAL" : False,
        "DUSTY_SPOT" : False,
        "HOME_PATH" : ''
    }

    # Upon starting the program, no state has been determined
    state = 'NOTHING'

    # Class functions to access and modify blackboard items
    def getBatteryLevel(self):
        return self.blackboard["BATTERY_LEVEL"]
    def setBatteryLevel(self, value):
        """ For the purposes of this program, only decreases battery """
        self.blackboard["BATTERY_LEVEL"] -= value

    def getSpot(self):
        return self.blackboard["SPOT"]
    def setSpot(self, value):
        self.blackboard["SPOT"] = value

    def getGeneral(self):
        return self.blackboard["GENERAL"]
    def setGeneral(self, value):
        self.blackboard["GENERAL"] = value  

    def getDusty(self):
        return self.blackboard["DUSTY_SPOT"]
    def setDusty(self, value):
        self.blackboard["DUSTY_SPOT"] = value

    # These functions are used in the process of charging the Roomba
    def findHome(self):
        """ Finds the best path home, updates 'HOME_PATH' in blackboard """
        self.state = 'RUNNING' # Finding best path to home in progress
        self.blackboard["HOME_PATH"] = 'This is the best path home.' 
        self.state = 'SUCCEEDED' # Finding best path to home succeeded
    
    def goHome(self):
        """ Reads from blackboard's 'HOME_PATH', follows that path to home """
        self.state = 'RUNNING' # Going home in progress
        self.state = 'SUCCEEDED' # Going home succeeded
        return self.blackboard["HOME_PATH"]

    def dock(self):
        self.state = 'RUNNING' # Charging in progress, updates the state
        self.blackboard["BATTERY_LEVEL"] = 100
        self.state = 'SUCCEEDED' # Charging completed, updates the state

    # Function that determines whether the Roomba has enough battery 
    # to proceed with an action
    def ensureBatteryFull(self):
        if self.getBatteryLevel() < 30:
            print('Battery Level: ' + str(self.getBatteryLevel()))
            self.state = 'FAILED' # Action failed; can't go on with battery<30
            
            print('FINDING BEST PATH TO HOME')
            self.findHome()
            
            print('FOUND BEST PATH TO HOME: ' + self.blackboard["HOME_PATH"])
            self.goHome()
            
            self.dock()
            print('BATTERY FULL')

    # Function that executes items in behavior tree (from left to right)
    def executeBehaviorTree(self, spotVal, generalVal):
        if self.getBatteryLevel() < 30:
            self.state = 'SUCCEEDED' # Leftmost condition in the BT succeeded
            # Continues implementing the tasks in subtree
            self.findHome()
            self.goHome()
            self.dock()
        else: # Leftmost condition in the BT failed
            self.state = 'FAILED'
            # Won't do any of the tasks in subtree, due to composite 'Sequence'

        ### SPOT CLEANING ###
        if spotVal == True:
            for i in range(SPOT_TIME):
                self.ensureBatteryFull()
                self.setBatteryLevel(1) # Decreases battery 1% every sec.(loop)
                self.state = 'RUNNING' # Spot cleaning is in progress
                print('SPOT CLEANING RUNNING: ' + str(i+1) + ' s, BATTERY: ' +
                      str(self.getBatteryLevel()) + '%')
                # Reports battery level at the end of each second (loop)
                
            self.setSpot(False) # Writes to blackboard's 'SPOT'
            self.state = 'SUCCEEDED' # Spot cleaning succeeded
            print('SPOT CLEANING SUCCEEDED, BATTERY: ' + 
                  str(self.getBatteryLevel()) + '%')

        ### GENERAL CLEAN ###
        elif generalVal == True:
            while self.getBatteryLevel() >= 30:

                # When the battery level matches the randomly-generated integer 
                # in the range 65-100, it begins the dusty spot cleaning
                if self.getBatteryLevel() == random.randint(65, 101):
                    self.setDusty(True)
                    self.state = 'SUCCEEDED' # DUSTY condition succeeded
                    print('FOUND A DUSTY SPOT')

                    for i in range(SPOT_GENERAL_TIME):
                        if self.getBatteryLevel() < 30:
                            self.state = 'FAILED'
                            break

                        else: 
                            self.setBatteryLevel(1)
                            self.state = 'RUNNING'
                            print('DUSTY SPOT GENERAL RUNNING: ' + str(i+1) + 
                                  ' s, BATTERY: ' + str(self.getBatteryLevel()) 
                                  + '%')

                            if i == SPOT_GENERAL_TIME - 1:
                                self.setDusty(False)
                                self.state = 'SUCCEEDED'
                                print('DUSTY SPOT GENERAL SUCCEEDED, BATTERY: ' 
                                      + str(self.getBatteryLevel()) + '%')
                else:
                    self.state = 'FAILED' # DUSTY condition failed

                self.setBatteryLevel(.5) # Battery is down .5% each sec.(loop)
                if self.getBatteryLevel() < 30:
                    self.state = 'FAILED'
                    break
                self.state = 'RUNNING'
                print('GENERAL RUNNING, BATTERY: ' + 
                      str(self.getBatteryLevel()) + '%')

            self.state = 'SUCCEEDED'
            print('GENERAL SUCCEEDED, BATTERY: ' + 
                  str(self.getBatteryLevel()) + '%')
            self.setGeneral(False) # Writes to blackboard's 'GENERAL'

            # Check battery level before attempting to do anything else
            self.ensureBatteryFull()

        ### DO NOTHING ###
        else:
            self.setBatteryLevel(.1) # Battery decreases .1% when idle
            print('DO NOTHING RUNNING, BATTERY: ' + 
                  str(self.getBatteryLevel()))
            self.state = 'SUCCEEDED'
            print('DO NOTHING SUCCEEDED')

            # Check battery level before attempting to do anything else
            self.ensureBatteryFull()


# User determines the task Roomba will do
def userInteraction():
    RoombaObject = Roomba()

    command = ''

    while command != 'Q':
        command = input('Enter S for Spot Cleaning, G for General Cleaning,' +
                        ' N for Do Nothing, and Q to Quit: ')
        
        if command == 'S':
            RoombaObject.executeBehaviorTree(True, False)
        elif command == 'G':
            RoombaObject.executeBehaviorTree(False, True)
        elif command == 'N':
            RoombaObject.executeBehaviorTree(False, False)
        elif command == 'Q':
            break
        else:
            print('Please enter a valid input!')

userInteraction()