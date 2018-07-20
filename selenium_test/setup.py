# this file contains setup procedures and globals (i.g. browser environment)

import pytest
from selenium import webdriver

serviceDelay = 100
pageDelay = 5000

def pytest_addoption(parser):
    parser.addoption("--driver", action="store", default="chrome", help="Type in browser type")
    parser.addoption("--url", action="store", default="http://www.sberbank.ru/ru/quotes/converter", help="url")

@pytest.fixture(scope="module", autouse=True)
def driver(request):
    browser = request.config.getoption("--driver")
    if browser == 'chrome':
        browser = webdriver.Chrome()
        browser.get("about:blank")
        pageWait(browser)
        browser.maximize_window()
        return browser
    else:
        print 'only chrome is supported at the moment'
        
@pytest.fixture(scope="module")
def url(request):
   return request.config.getoption("--url")
   
def serviceWait(browser)
    browser.implicitly_wait(serviceDelay)
    
def pageWait(browser)
    browser.implicitly_wait(pageDelay)
    
def selfTest(browser)
    driver.get('http://www.sberbank.ru/ru/quotes/converter')
    pageWait(browser)
    assert 'Калькулятор иностранных валют' in driver.title
    
def closeDriver(browser)
    browser.quit()