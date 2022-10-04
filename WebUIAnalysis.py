import lxml.etree as etree
import json
import operator
from random import random

referencedScreen = []
allScreen = []
unusedScreen = []
screenItems = dict()

namespaces = {'ns':'http://stibosystems.com/step/portal-config'}

class Screen:
    def __init__(self, id, type):
        self.id = id
        self.type = type
        self.count = 0
    def __str__(self):
        return f"ID: {self.id}, Type: {self.type}, Count: {self.count}"

def initialise_class(screenID, ScreenType):
    global screenItems
    if screenID not in screenItems.keys():
        screenObject = Screen(screenID, ScreenType)
        #print(screenObject)
        screenItems[screenID] = screenObject
    else:
        print("Error: initialise_class")

def count_this_class(screenID):
    global screenItems
    if screenID not in screenItems.keys():
        print("Error: count_this_class:", screenID)
    else:
        screenObject = screenItems[screenID]
        screenObject.count += 1
        screenItems[screenID] = screenObject

def printList(list):
    list.sort()      
    for object in list:
       print(object)

def determineTotalScreens(screens):
    #Total Screens
    for screen in screens:
        screenID = screen.xpath('@id')[0]
        ScreenType = screen.xpath('@type')[0]
        #print("ScreenID",screenID)
        #print("ScreenType",ScreenType)
        allScreen.append(screenID)
        initialise_class(screenID, ScreenType)

def determineReferencedScreens(doc, screens):
    global namespaces

    #Referenced Screens - Check 1
    for screen in screens:
        #https://www.online-toolz.com/tools/xpath-tester-online.php
        btags = screen.xpath("ns:component[@id='Main'][@type='TabControl']/ns:parameter-list/ns:component/ns:parameter[@id='DetailsScreen']/@value",namespaces=namespaces)
        for b in btags:
            # print(" - ",b)
            count_this_class(b)
            if not b in referencedScreen:
                #print("Item is in array already.")
                referencedScreen.append(b)

    #Referenced Screens - Check 2
    forwardingSwitchScreenScreen = doc.xpath("//ns:screen[@type='ForwardingSwitchScreen']/ns:parameter-list[@id='Mappings']/ns:component/ns:parameter[@id='Screen']/@value",namespaces=namespaces)
    for screen in forwardingSwitchScreenScreen:
        count_this_class(screen)
        if not screen in referencedScreen:
            #print("Item is in array already.")
            referencedScreen.append(screen)
    
    #Referenced Screens - Check 3
    mainScreen = doc.xpath("//ns:screen[@id='main']/ns:parameter-list[@id='Mappings']/ns:component/ns:parameter[@id='Screen']/@value",namespaces=namespaces)
    for screen in mainScreen:
        #print("mainScreen", screen)
        count_this_class(screen)
        if not screen in referencedScreen:
            #print("Item is in array already.")
            referencedScreen.append(screen)
    
    #Referenced Screens - Check 4
    homepageScreen = doc.xpath("//ns:screen[@id='homepage']/ns:parameter-list/ns:component/ns:parameter-list/ns:component/ns:parameter[@id='ResultScreen']/@value",namespaces=namespaces)
    for screen in homepageScreen:
        #print("homepageScreen", screen)
        count_this_class(screen)
        if not screen in referencedScreen:
            #print("Item is in array already.")
            referencedScreen.append(screen)

def main():

    doc = etree.parse('webUI.xml')
    screens = doc.xpath("//ns:screen[not(@type = 'Main' or @type = 'HomePage' or @type = 'LoginScreen')]",namespaces=namespaces)

    determineTotalScreens(screens)
    determineReferencedScreens(doc, screens)

    #Create List of Unused Screens
    for screen in allScreen:
        if screen not in referencedScreen:
            unusedScreen.append(screen) 

    # printList(allScreen)
    # printList(referencedScreen)
    # printList(unusedScreen)

    print()
    print("Screen Metadata")
    for screenItem in (sorted(screenItems.values(), key=operator.attrgetter('count'))):
        print(screenItem)

    print()
    print("Screen Summary")
    print("Total Screen Count:", len(allScreen))
    print("Referenced Screen Count:", len(referencedScreen))
    print("(Potential) Unused Screen Count:", len(unusedScreen))

if __name__ == '__main__': main()