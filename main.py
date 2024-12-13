from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from time import time
from typing import List
from threading import Event
from threading import Thread
import random


DRIVER_PATH: str = "/usr/bin/chromedriver";
WEB_PATH: str = "https://orteil.dashnet.org/cookieclicker/";

COOKIES_ACCEPT_TAG: str = "p.fc-button-label";
SELECT_LANG_TAG: str = "langSelect-PL";
COOKIE_TAG: str = "bigCookie";
UPGRADE_TAG: str = ".product.unlocked.enabled";

ACCEPT_COOKIES_WAIT_TIME: int = 1;
SELECT_LANG_WAIT_TIME: int = 3;
BUY_INTERVAL: int = 5;
MAIN_LOOP_INTERVAL: int = 1;


def sleep(wait_for: int):
    event = Event();
    event.wait(wait_for)


class DriverController:
    def __init__(self):
        service = Service(DRIVER_PATH);

        self.__driver: WebDriver = webdriver.Chrome(service=service);
        self.__driver.get(WEB_PATH)


    def element_by_id(self, id: str) -> WebElement:
        return self.__driver.find_element(By.ID, id);
    

    def element_by_class_name(self, class_name: str) -> WebElement:
        return self.__driver.find_element(By.CSS_SELECTOR, class_name);


    def elements_list_by_class_name(self, class_name: str) -> List[WebElement]:
        return self.__driver.find_elements(By.CSS_SELECTOR, class_name);


class ClickerLogic:
    def __init__(self, driver: DriverController):
        self.__driver = driver;

    
    def accept_cookies(self) -> None:
        element = self.__driver.element_by_class_name(COOKIES_ACCEPT_TAG);
        element.click();


    def select_lang(self) -> None:
        element = self.__driver.element_by_id(SELECT_LANG_TAG);
        element.click();


    def __click_cookie(self) -> None:
        element = self.__driver.element_by_id(COOKIE_TAG);

        while True:
            element.click();


    def __buy(self) -> None:
        while True:
            try:
                upgrades = self.__get_upgrades();

                self.__select_random_upgrade(upgrades);
                sleep(BUY_INTERVAL)

            except Exception as e:
                pass
    

    def __get_upgrades(self) -> List[WebElement]:
        return self.__driver.elements_list_by_class_name(UPGRADE_TAG);
    

    def __select_random_upgrade(self, upgrades: List[WebElement]):
        upgrades = random.choice(upgrades)
        upgrades.click();


    def clicker_thread(self) -> None :
        thread = Thread(target=self.__click_cookie, daemon=True)
        thread.start()


    def buyer_thread(self) -> None:
        thread = Thread(target=self.__buy, daemon=True)
        thread.start()


if __name__ == "__main__":
    driver = DriverController();
    clicker = ClickerLogic(driver);
    
    clicker.accept_cookies();
    sleep(ACCEPT_COOKIES_WAIT_TIME);

    clicker.select_lang();
    sleep(SELECT_LANG_WAIT_TIME);

    clicker.clicker_thread();
    clicker.buyer_thread();

    while True:
        sleep(MAIN_LOOP_INTERVAL);