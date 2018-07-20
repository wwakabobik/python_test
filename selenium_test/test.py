# this file contains tests

import pytest
import allure
import setup as setup
import pom as pom
import utils as utils

driver = setup.driver()

@allure.feature('Конвертер валют Сбербанка')
@allure.story('Ввод суммы для конвертации, проверка позитивной конвертации валют')
class TestConverter_01:
    @allure.step('Запуск браузера, открытие и загрузка страницы с кальулятором')
    def setup_method(self, method):
        setup.selfTest(driver)
        pom.setDriver(driver)        

    @allure.step('Возврат в исходное состояние, закрытие браузера')
    def teardown_method(self, method):
        setup.closeDriver()

    @allure.step('Ввод валидных данных в поле ввода суммы и проверка результата')
    def test_input_amount(self):
        pom.setupTC(1)
        pom.convertCurrency(utils.getData_Amount(1))
        assert pom.getResultAmount() == utils.getData_ResultAmount(1)
        
    @allure.step('Проверка корректности указания валюты расчёта')
    def test_input_currency(self)
        assert pom.getResultCurrency() == utils.getData_ResultCurrency(1)

@allure.feature('Конвертер валют Сбербанка')
@allure.story('Проверка неверного ввода данных')
class TestConverter_02:
    @allure.step('Запуск браузера, открытие и загрузка страницы с кальулятором')
    def setup_method(self, method):
        setup.selfTest(driver)
        pom.setDriver(driver)        

    @allure.step('Возврат в исходное состояние, закрытие браузера')
    def teardown_method(self, method):
        setup.closeDriver()

    @allure.step('Ввод невалидных данных в поле ввода суммы и проверка результата')
    def test_input_amount(self):
        pom.setupTC(2)
        pom.convertCurrency(utils.getData_Amount(2))
        assert pom.isResultExists() == False
        
@allure.feature('Конвертер валют Сбербанка')
@allure.story('Проверка открытия журнала котировок')
class TestConverter_03:
    @allure.step('Запуск браузера, открытие и загрузка страницы с кальулятором')
    def setup_method(self, method):
        setup.selfTest(driver)
        pom.setDriver(driver)        

    @allure.step('Возврат в исходное состояние, закрытие браузера')
    def teardown_method(self, method):
        setup.closeDriver()

    @allure.step('Открытие таблицы и проверка, что она открылась')
    def test_open_journal(self):
        pom.table_Open()
		setup.pageWait(driver)
        assert pom.isTableOpen() == True