import pytest

from mops.base.driver_wrapper import DriverWrapper
from mops.mixins.objects.driver import Driver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.remote.webdriver import WebDriver as Remote


@pytest.fixture
def driver_wrapper():
    options = ChromeOptions()
    selenium_driver = Driver(driver=Remote(options=options, command_executor="http://chrome:4444"))
    return DriverWrapper(selenium_driver)
