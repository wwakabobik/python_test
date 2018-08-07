# this file contains setup procedures and globals (i.g. browser environment)

import pytest
import sys
from selenium import webdriver

serviceDelay = 100
pageDelay = 5000

def pytest_addoption(parser):
    parser.addoption("--driver", action="store", default="chrome", help="Type in browser type")
    parser.addoption("--url", action="store", default="http://www.sberbank.ru/ru/quotes/converter", help="url")

@pytest.fixture(scope="module", autouse=True)
def driver(request):
    #browser = request.config.getoption("--driver")
    if "--driver" in request:
        if "--driver=chrome" in request:
            driver = webdriver.Chrome()
        elif "--driver=firefox" in request:
            driver = webdriver.Firefox()
            return driver
        else:
            print('only chrome and firefox is supported at the moment')
            sys.exit("-1")
    driver.get("about:blank")
    pageWait(driver)
    driver.maximize_window()
    return driver
        
@pytest.fixture(scope="module")
def url(request):
   return request.config.getoption("--url")
   
def serviceWait(browser):
    browser.implicitly_wait(serviceDelay)
    
def pageWait(browser):
    browser.implicitly_wait(pageDelay)
    
def selfTest(browser, targetPage, checkString):
    browser.get(targetPage)
    pageWait(browser)
    assert checkString in browser.title
    
def closeDriver(browser):
    browser.quit()
