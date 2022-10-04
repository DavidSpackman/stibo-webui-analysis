import lxml.etree as etree
import json
import operator
from random import random


referencedScreen = []
allScreen = []
unusedScreen = []

items = dict()
screenItems = dict()

class Screen:
    def __init__(self, id, type):
        self.id = id
        self.type = type
        self.count = 0
    def __str__(self):
        return f"ID: {self.id}, Type: {self.type}, Count: {self.count}"


def count_this(screenID):
    global items
    if screenID not in items.keys():
        items[screenID] = 0
    else:
        items[screenID] += 1

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

def main():

    doc = etree.parse('webUI.xml')
    namespaces = {'ns':'http://stibosystems.com/step/portal-config'}


    screens = doc.xpath("//ns:screen[not(@type = 'Main' or @type = 'HomePage' or @type = 'LoginScreen')]",namespaces=namespaces)

    #Total Screens
    for screen in screens:
        screenID = screen.xpath('@id')[0]
        ScreenType = screen.xpath('@type')[0]
        #print("ScreenID",screenID)
        #print("ScreenType",ScreenType)
        allScreen.append(screenID)
        count_this(screenID)
        initialise_class(screenID, ScreenType)

    #Referenced Screens - Check 1
    for screen in screens:
        #https://www.online-toolz.com/tools/xpath-tester-online.php
        btags = screen.xpath("ns:component[@id='Main'][@type='TabControl']/ns:parameter-list/ns:component/ns:parameter[@id='DetailsScreen']/@value",namespaces=namespaces)
        for b in btags:
            # print(" - ",b)
            count_this(b)
            count_this_class(b)
            if not b in referencedScreen:
                #print("Item is in array already.")
                referencedScreen.append(b)

    #Referenced Screens - Check 2
    forwardingSwitchScreenScreen = doc.xpath("//ns:screen[@type='ForwardingSwitchScreen']/ns:parameter-list[@id='Mappings']/ns:component/ns:parameter[@id='Screen']/@value",namespaces=namespaces)
    for screen in forwardingSwitchScreenScreen:
        count_this(screen)
        count_this_class(screen)
        if not screen in referencedScreen:
            #print("Item is in array already.")
            referencedScreen.append(screen)
    
    #Referenced Screens - Check 3
    mainScreen = doc.xpath("//ns:screen[@id='main']/ns:parameter-list[@id='Mappings']/ns:component/ns:parameter[@id='Screen']/@value",namespaces=namespaces)
    for screen in mainScreen:
        #print("mainScreen", screen)
        count_this(screen)
        count_this_class(screen)
        if not screen in referencedScreen:
            #print("Item is in array already.")
            referencedScreen.append(screen)
    
    #Referenced Screens - Check 4
    homepageScreen = doc.xpath("//ns:screen[@id='homepage']/ns:parameter-list/ns:component/ns:parameter-list/ns:component/ns:parameter[@id='ResultScreen']/@value",namespaces=namespaces)
    for screen in homepageScreen:
        #print("homepageScreen", screen)
        count_this(screen)
        count_this_class(screen)
        if not screen in referencedScreen:
            #print("Item is in array already.")
            referencedScreen.append(screen)
    
    #Unused Screens
    for screen in allScreen:
        if screen not in referencedScreen:
            unusedScreen.append(screen) 

    #allScreen.sort()      
    #for allScreenitem in allScreen:
    #    print(allScreenitem)

    #referencedScreen.sort()      
    #for referencedScreenitem in referencedScreen:
    #    print(referencedScreenitem)

    #unusedScreen.sort() 
    #for unusedScreenitem in unusedScreen:
    #    print(unusedScreenitem)

    
    # sortedDict = {k: v for k, v in sorted(items.items(), key=lambda item: item[1])}
    # print(json.dumps(sortedDict, indent='\t'))

    # print()
    # print("Total Screen Count:",len(allScreen))
    # print("Referenced Screen Count:",len(referencedScreen))
    # print("(Potential) Unused Screen Count:",len(unusedScreen))

    # for key in screenItems:
    #     print(screenItems[key])

    print()
    print()


    for screenItem in (sorted(screenItems.values(), key=operator.attrgetter('count'))):
        print(screenItem)

if __name__ == '__main__': main()