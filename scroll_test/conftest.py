from selenium import webdriver
import pytest


@pytest.fixture(autouse=True, scope="session")
def driver():
    my_driver = webdriver.Chrome()
    yield my_driver
    my_driver.close()
    my_driver.quit()
