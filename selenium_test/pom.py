# this file describes POM of  http://www.sberbank.ru/ru/quotes/converter
# not all objects and method are defined, it's for demo use only

import utils as utils

# note: it's better to create separate class for this main page of calculator,
# probably for modal window also needed separate class, for footer and header

class CurrencyConverter:
    # define driver global within this pom
    driver = None

    ####################################### objects ###########################
	# try to name it in one style
    # we're using functions insted of variables, due to we'll get objects at 
	# runtime and mostly once, therefore it's not needed to store them in 
	# variables to be accessable from anywhere
    def getAmount_Field(driver):
        return driver.find_element_by_xpath("//div[@class='rates-aside__filter-block-line-right input']/form/input")

    def getCalculate_Button(driver):
        return driver.find_element_by_xpath("//div[@class='rates-aside__filter-block rates-aside__filter-block_mode_converter']/button")
    
    def getResultAmount_Field(driver):
        return driver.find_element_by_xpath("//div[@class='rates-converter-result__total']/span[3]")
    
    def getTableOpen_Link(driver):
        return driver.find_element_by_xpath("//div[@class='rates-details__links print-invisible']/span[2]")
    
    def getTable_Header(driver):
        return driver.find_element_by_xpath("//div[@class='modal-content']/h2")
    
    ####################################### methods ###########################
    def setDriver(browser):
        global driver
        driver=browser
    
    def calculate_Click():
        calculateButton = CurrencyConverter.getCalculate_Button(driver)
        #button is not visible due to hover footer, therefore, scroll down using js
        driver.execute_script("arguments[0].click();", calculateButton)
    
    def amount_Click():
        amountField = CurrencyConverter.getAmount_Field(driver)
        amountField.click()
    
    def amount_Clear():
        amountField = CurrencyConverter.getAmount_Field(driver)
        amountField.clear()

    def amount_Fill(input):
        amountField = CurrencyConverter.getAmount_Field(driver)
        amountField.send_keys(input)

    def currencyIn_Fill(CurrencyType):
        dummy = "TBD"
        #TODO

    def currencyOut_Fill(CurrencyType):
        dummy = "TBD"
        #TODO

    def table_Open():
        CurrencyConverter.getTableOpen_Link(driver).click()
    
    def isTableOpen():
        if "Таблица изменения котировок" not in CurrencyConverter.getTable_Header(driver).text:
            return -1
        else:
            return 0
    
    def getResultAmount():
        calculatedAmountField = CurrencyConverter.getResultAmount_Field(driver)
        resultText = calculatedAmountField.get_attribute('innerHTML')
        resultText = resultText[0:-4]
        return resultText
    
    def getResultCurrency():
        calculatedCurrencyField = CurrencyConverter.getResultAmount_Field(driver)
        resultText = calculatedCurrencyField.get_attribute('innerHTML')
        resultText = resultText[len(resultText)-3:len(resultText)]
        return resultText

    def isResultExists():
        try:
            CurrencyConverter.getResultAmount_Field(driver)
        except NoSuchElementException:
            return -1
        return 0

    ############################ typical actions ##############################
    def setupTC(TCNumber):
        #commented out due to not all functions are implemented yet
        #setupSettings(utils.getData_currencyIn(TCNumber), utils.getData_currencyOut(TCNumber), utils.getData_source(TCNumber), utils.getData_recieve(TCNumber), utils.getData_exchange(TCNumber), util.getData_package(TCNumber), util.getData_time(TCNumber))
        CurrencyConverter.setupSettings(utils.getData_currencyIn(TCNumber), utils.getData_currencyOut(TCNumber))

    def setupSettings(currencyIn, currencyOut): #, source, recieve, exchange, package, time):
    # here is commented out several calls and params due to they're not implemented yet
        CurrencyConverter.currencyIn_Fill(currencyIn)
        CurrencyConverter.currencyOut_Fill(currencyOut)
        #CurrencyConverter.source_Fill(source)
        #CurrencyConverter.recieve_Fill(recieve)
        #CurrencyConverter.exchange_Fill(exchange)
        #CurrencyConverter.package_Fill(package)
        #CurrencyConverter.time_Fill(time)

    def convertCurrency(amount):
        CurrencyConverter.amount_Click()
        CurrencyConverter.amount_Clear()
        CurrencyConverter.amount_Fill(amount)
        CurrencyConverter.calculate_Click()
