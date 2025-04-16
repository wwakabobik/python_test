from pom.pom_example import SeleniumPage


def test_simplest(driver_wrapper):
    page = SeleniumPage()
    page.open_page()
    page.wait_page_loaded()

    assert page.is_page_opened()
    assert page.getting_started.webdriver.is_visible()
    assert page.getting_started.webdriver.text == "Selenium WebDriver"
