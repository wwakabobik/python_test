# this file contains tests

import pytest
import allure
import setup as setup
from pom import CurrencyConverter as pom
import utils as utils

# global setup
driver = setup.driver("--driver=chrome")
targetPage = 'http://www.sberbank.ru/ru/quotes/converter'
checkString = 'Калькулятор иностранных валют'

@allure.feature('Конвертер валют Сбербанка')
@allure.story('Ввод суммы для конвертации, проверка позитивной конвертации валют')
class TestConverter_01:
    @allure.step('Запуск браузера, открытие страницы, ввод корректных данных')
    def setup_method(self, method):
        setup.selfTest(driver, targetPage, checkString)
        pom.setDriver(driver)  
        pom.setupTC(1)
        pom.convertCurrency(utils.getData_Amount(1))        

    @allure.step('Проверка корректности результата')
    def test_input_amount(self):
        assert pom.getResultAmount() == utils.getData_ResultAmount(1)
        
    @allure.step('Проверка корректности указания валюты расчёта')
    def test_input_currency(self):
        assert pom.getResultCurrency() == utils.getData_ResultCurrency(1)

@allure.feature('Конвертер валют Сбербанка')
@allure.story('Проверка открытия журнала котировок')
class TestConverter_02:
    @allure.step('Запуск браузера, открытие страницы, ввод корректных данных')
    def setup_method(self, method):
        setup.selfTest(driver, targetPage, checkString)
        pom.setDriver(driver)
        pom.table_Open()      

    @allure.step('Открытие таблицы и проверка, что она открылась')
    def test_open_journal(self):
        assert pom.isTableOpen() == 0
		
@allure.feature('Конвертер валют Сбербанка')
@allure.story('Проверка неверного ввода данных')
class TestConverter_03:
    @allure.step('Запуск браузера, открытие страницы, ввод некорректных данных')
    def setup_method(self, method):
        setup.selfTest(driver, targetPage, checkString)
        pom.setDriver(driver)
        pom.setupTC(3)
        pom.convertCurrency(utils.getData_Amount(3))        

    @allure.step('Проверка, что результат не отображён')
    def test_input_amount(self):
        assert pom.isResultExists() == False
        
    @allure.step('Возврат в исходное состояние, закрытие браузера')
    def teardown_method(self, method):
        setup.closeDriver(driver)
        