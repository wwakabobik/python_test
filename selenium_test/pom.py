# this file describes POM of  http://www.sberbank.ru/ru/quotes/converter
# not all objects and method are defined, it's for demo use only

from selenium import webdriver
import pom as pom
import setup as setup
import utils as utils

class CalculatorPOM:
    ##### objects #####
    # input
    # converter
    amountField = driver.find_element_by_xpath("//input[@data-reactid='.0.$1.$0.0.1.0.0.0']")
    #currencyInField = 
    #currencyOutField = 
    #sourceField =
    #recieveField =
    #exchangeField =
    #packageField =
    #timeField = 
    #timeButton =
    # graph
    #dateFromField =
    #dateToField =
    #dateFromButton =
    #dateToButton = 
    # actions
    calculateButton = driver.find_element_by_xpath("//button[@data-reactid='.0.$1.$0.6.0']")
    #redrawButton = 
    # output
    # converter
    calculatedAmountField = driver.find_element_by_xpath("//span[@data-reactid='.0.$1.$1.1.0']")
    calculatedCurrencyField = driver.find_element_by_xpath("//span[@data-reactid='.0.$1.$1.1.1']")
    # graph
    #sourceCurrencyField =
    #destCurrencyField =
    #buyField =
    #sellField =
    #buyChangeField =
    #sellChangeField =
    #timestampField =
    #textCurrencyField =
    #urls
    #printURL =
    #tableURL = 
    #downloadURL =
    #closeURL = 
    
#methods
def setDriver(browser):
    driver=browser
    
def calculate_Click():
    calculateButton.click()
    
def amount_Click():
    amountField.Click()
    
def amount_Clear():
    amountField.clear()

def amount_Fill(input):
    amountField.send_keys(input)

def currencyIn_Fill():
    #TODO

def currencyOut_Fill():
    #TODO

def table_Open():
    #TODO
    
def isTableOpen():
    #TODO
    
def getResultAmount():
    return calculatedAmountField.text
    
def getResultCurrency():
    return calculatedCurrencyField.text

def isResultExists():
    try:
        driver.find_element_by_xpath("//span[@data-reactid='.0.$1.$1.1.0']")
    except NoSuchElementException:
        return False
    return True

#typical actions
def setupTC(number):
    #setupSettings(utils.getData_currencyIN(TCNumber), utils.getData_currencyOut(TCNumber), utils.getData_source(TCNumber), utils.getData_recieve(TCNumber), utils.getData_exchange(TCNumber), util.getData_package(TCNumber), util.getData_time(TCNumber))
    setupSettings(utils.getData_currencyIN(TCNumber), utils.getData_currencyOut(TCNumber))

def setupSettings(currencyIn, CurrencyOut, source, recieve, exchange, package, time):
    if currencyIn is not None 
        pom.CurrencyIn_Fill(currencyIn)
    if currencyOut is not None 
        pom.CurrencyOut_Fill(currencyOut)
    #if source is not None 
        #pom.source_Fill(source)
    #if recieve is not None 
        #pom.recieve_Fill(recieve)
    #if exchange is not None 
        #pom.exchange_Fill(exchange)
    #if package is not None 
        #pom.package_Fill(package)
    #if time is not None 
        #pom.time_Fill(time)

def convertCurrency(amount)
    pom.amount_Click()
    pom.amount_Clear()
    pom.amount_Send(amount)
    pom.calculate_Click()
    pageWait(driver)