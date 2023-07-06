from os import getcwd
from time import sleep

import pytest

DELAY = 5  # delay to be human-friendly

""" TEST DATA """

elements_under_test = (
    {
        "id": "Vertical scroll",
        "result": True,
        "page": "element_with_vertical_scroll.html",
    },
    {
        "id": "Horizontal scroll",
        "result": True,
        "page": "element_with_horizontal_scroll.html",
    },
    {"id": "Both scroll", "result": True, "page": "element_with_both_scroll.html"},
    {"id": "No scroll", "result": False, "page": "element_with_no_scroll.html"},
)

locator = '//*[contains(@class, "scroll")]'

pages_under_test = (
    {"id": "Vertical scroll", "result": True, "page": "page_with_vertical_scroll.html"},
    {
        "id": "Horizontal scroll",
        "result": True,
        "page": "page_with_horizontal_scroll.html",
    },
    {"id": "Both scroll", "result": True, "page": "page_with_both_scroll.html"},
    {"id": "No scroll", "result": False, "page": "page_with_no_scroll.html"},
)

""" FRAMEWORK PART """


def is_element_vertical_scrollable_js(driver, element):
    return driver.execute_script(
        "return arguments[0].scrollHeight > arguments[0].offsetHeight;", element
    )


def is_element_horizontal_scrollable_js(driver, element):
    return driver.execute_script(
        "return arguments[0].scrollWidth > arguments[0].offsetWidth;", element
    )


def is_element_scrollable_var_1(driver, element):
    return is_element_vertical_scrollable_js(
        driver, element
    ) or is_element_horizontal_scrollable_js(driver, element)


def is_element_vertical_scrollable(element):
    scroll_height = int(element.get_attribute("scrollHeight"))
    offset_height = int(element.get_attribute("offsetHeight"))
    return scroll_height > offset_height


def is_element_horizontal_scrollable(element):
    scroll_width = int(element.get_attribute("scrollWidth"))
    offset_width = int(element.get_attribute("offsetWidth"))
    return scroll_width > offset_width


def is_element_scrollable_var_2(element):
    return is_element_horizontal_scrollable(element) or is_element_vertical_scrollable(
        element
    )


def is_page_horizontal_scrollable(driver):
    return driver.execute_script(
        "return document.documentElement.scrollWidth >"
        " document.documentElement.clientWidth;"
    )


def is_page_vertical_scrollable(driver):
    return driver.execute_script(
        "return document.documentElement.scrollHeight >"
        " document.documentElement.clientHeight;"
    )


def is_page_scrollable(driver):
    return is_page_vertical_scrollable(driver) or is_page_horizontal_scrollable(driver)


""" TEST PART """


@pytest.fixture(params=pages_under_test, ids=[f'{c["id"]}' for c in pages_under_test])
def get_page_under_test(driver, request):
    case = request.param.copy()
    file_name = f'file://{getcwd()}/pages/{case["page"]}'
    driver.get(file_name)
    sleep(DELAY)

    return driver, case["result"]


@pytest.fixture(
    params=elements_under_test, ids=[f'{c["id"]}' for c in elements_under_test]
)
def get_element_under_test(driver, request):
    case = request.param.copy()
    file_name = f'file://{getcwd()}/pages/{case["page"]}'
    driver.get(file_name)
    element = driver.find_element_by_xpath(locator)
    sleep(DELAY)

    return driver, element, case["result"]


def test_element_is_scrollable_v1(get_element_under_test):
    driver, element, expected = get_element_under_test
    assert is_element_scrollable_var_1(driver, element) == expected


def test_element_is_scrollable_v2(get_element_under_test):
    driver, element, expected = get_element_under_test
    assert is_element_scrollable_var_2(element) == expected


def test_page_is_scrollable(get_page_under_test):
    driver, expected = get_page_under_test
    assert is_page_scrollable(driver) == expected
