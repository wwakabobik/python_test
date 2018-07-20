# this file contains different utils and functions to support testing

from BeautifulSoup import BeautifulStoneSoup as Soup

# setup
def getFileName(TCNumber):
	return String("TC" + String(TCNumber) + ".xml")

def getData_currencyIN(TCNumber):
    filename = getFileName(TCNumber)
	soup = Soup(open(filename))
	for tag in soup.findAll('ConverterSetup'):
    return tag.find('ConverterSetup:currencyIN').text

def getData_currencyOut(TCNumber):
    filename = getFileName(TCNumber)
	soup = Soup(open(filename))
	for tag in soup.findAll('ConverterSetup'):
    return tag.find('ConverterSetup:currencyOut').text
	
def getData_source(TCNumber):
    filename = getFileName(TCNumber)
	soup = Soup(open(filename))
	for tag in soup.findAll('ConverterSetup'):
    return tag.find('ConverterSetup:source').text
	
def getData_recieve(TCNumber):
    filename = getFileName(TCNumber)
	soup = Soup(open(filename))
	for tag in soup.findAll('ConverterSetup'):
    return tag.find('ConverterSetup:recieve').text
	
def getData_exchange(TCNumber):
    filename = getFileName(TCNumber)
	soup = Soup(open(filename))
	for tag in soup.findAll('ConverterSetup'):
    return tag.find('ConverterSetup:exchange').text
	
def getData_package(TCNumber):
    filename = getFileName(TCNumber)
	soup = Soup(open(filename))
	for tag in soup.findAll('ConverterSetup'):
    return tag.find('ConverterSetup:package').text
	
def getData_time(TCNumber):
    filename = getFileName(TCNumber)
	soup = Soup(open(filename))
	for tag in soup.findAll('ConverterSetup'):
    return tag.find('ConverterSetup:time').text

# input
def getData_Amount(TCNumber):
    filename = getFileName(TCNumber)
	soup = Soup(open(filename))
	for tag in soup.findAll('Amount'):
    return tag.find('Amount:amount').text
	
# result
def getData_ResultAmount(TCNumber):
    filename = getFileName(TCNumber)
	soup = Soup(open(filename))
	for tag in soup.findAll('Result'):
    return tag.find('Result:amount').text
	
def getData_ResultCurrency(TCNumber):
    filename = getFileName(TCNumber)
	soup = Soup(open(filename))
	for tag in soup.findAll('Result'):
    return tag.find('Result:currency').text
