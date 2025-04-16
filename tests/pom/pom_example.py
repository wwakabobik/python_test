from mops.base.element import Element
from mops.base.group import Group
from mops.base.page import Page


class GettingStarted(Group):
    def __init__(self):
        super().__init__("//*[@class='card-body']", name="Getting started card")
        self.webdriver = Element(self.locator + "/h4[.='Selenium WebDriver']", name='Selenium WebDriver')
        self.ide = Element(self.locator + "/h4[.='Selenium IDE']", name="Selenium IDE")
        self.grid = Element(self.locator + "/h4[.='Selenium Grid']", name="Selenium Grid")


class SeleniumPage(Page):
    url = "https://selenium.dev"

    def __init__(self):
        super().__init__("//h1[contains(., 'Selenium automates browsers')]",  name='Selenium page')

    getting_started = GettingStarted()
