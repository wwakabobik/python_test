# this file contains different utils and functions to support testing

from bs4 import BeautifulSoup as Soup

# setup
def getFileName(TCNumber):
    return str("TC" + str(TCNumber) + ".xml")

# common	
def getTags(TCNumber, TagName):
    filename = getFileName(TCNumber)
    infile = open(filename,"r")
    contents = infile.read()
    soup = Soup(contents,'xml')
    tags = soup.find(TagName)
    return tags

#get fields
def getData_currencyIn(TCNumber):
    titles=getTags(TCNumber, "ConverterSetup")
    return titles.find("currencyIn").get_text()

def getData_currencyOut(TCNumber):
    titles=getTags(TCNumber, "ConverterSetup")
    return titles.find("currencyOut").get_text()
    
def getData_source(TCNumber):
    titles=getTags(TCNumber, "ConverterSetup")
    return titles.find("source").get_text()
    
def getData_recieve(TCNumber):
    titles=getTags(TCNumber, "ConverterSetup")
    return titles.find("recieve").get_text()
    
def getData_exchange(TCNumber):
    titles=getTags(TCNumber, "ConverterSetup")
    return titles.find("exchange").get_text()
    
def getData_package(TCNumber):
    titles=getTags(TCNumber, "ConverterSetup")
    return titles.find("package").get_text()
    
def getData_time(TCNumber):
    titles=getTags(TCNumber, "ConverterSetup")
    return titles.find("time").get_text()

# input
def getData_Amount(TCNumber):
    titles=getTags(TCNumber, "Amount")
    return titles.find("amount").get_text()
    
# result
def getData_ResultAmount(TCNumber):
    titles=getTags(TCNumber, "Result")
    return titles.find("amount").get_text()
    
def getData_ResultCurrency(TCNumber):
    titles=getTags(TCNumber, "Result")
    return titles.find("currency").get_text()
