import datetime
import logging
import os
import time
import getpass

import chromedriver_autoinstaller
import selenium.common.exceptions
from fastapi import HTTPException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from .data import Collection, Week
from .scrape import scrape_week


class WebuntisDriver(webdriver.Chrome):
    LOGOUT_PAGE = "https://neilo.webuntis.com/WebUntis/saml/logout"
    LOGIN_PAGE = "https://neilo.webuntis.com/WebUntis/?school=htl1-innsbruck#/basic/login"
    TIMETABLE_PAGE = "https://neilo.webuntis.com/timetable-students-my"
    ABSENCES_PAGE = "https://neilo.webuntis.com/student-absences"
    DELAY = 5

    def __init__(self, debug: bool = False, *args, **kwargs):
        chromedriver_autoinstaller.install()

        options = Options()
        options.add_argument("--enable-javascript")
        if not debug:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')

        super().__init__(options=options, *args, **kwargs)
        self.debug = debug

        self.weeks: Collection = Collection({})
        self.current_week = datetime.datetime.now().isocalendar().week
        self.current_school = self.LOGIN_PAGE
        self.account_status: bool = False

    def close(self):
        try:
            super().close()
        except:
            pass

    def login(self, username: str = None, password: str = None):
        self.get_page(self.LOGIN_PAGE, By.ID, "app", True)
        if username is None:
            username = os.getenv("username")
            if username is None:
                username = input("Username: ")
        if password is None:
            password = os.getenv("password")
            if password is None:
                password = getpass.getpass("Password: ")
        username_field = self.find_element(
            By.XPATH, "/html/body/div/div/div/div[2]/div[1]/div/div[2]/div/div[2]/div/form/div[1]/div/input")
        password_field = self.find_element(
            By.XPATH, "/html/body/div/div/div/div[2]/div[1]/div/div[2]/div/div[2]/div/form/div[2]/div/input")
        login_button = self.find_element(
            By.XPATH, "/html/body/div/div/div/div[2]/div[1]/div/div[2]/div/div[2]/div/form/button")

        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()

        WebDriverWait(self, self.DELAY).until(expected_conditions.presence_of_element_located((By.ID, "root")))
        try:

            username_field = self.find_element(
               By.XPATH, "/html/body/div/div/div/div[2]/div[1]/div/div[2]/div/div[2]/div/form/div[1]/div/input"
            )
            print("Element found")
            self.account_status = False
            return False
        except selenium.common.exceptions.NoSuchElementException:
            self.account_status = True
            return True

    def logout(self):
        self.get_page(self.LOGOUT_PAGE, By.ID, "app")
        self.account_status = False
        return True

    def get_page(self, url: str, criteria: By | str = None, name: str = None, logging_in: bool = False):
        if self.account_status or logging_in:
            self.get(url)
            if not criteria and not name:
                time.sleep(self.DELAY)
                return
            WebDriverWait(self, self.DELAY).until(expected_conditions.presence_of_element_located((criteria, name)))
            return True
        else:
            return False

    def get_iframe(self, criteria: By | str = None, name: str = None):
        self.switch_to.frame(0)
        if not criteria and not name:
            time.sleep(self.DELAY)
            return
        WebDriverWait(self, self.DELAY).until(expected_conditions.presence_of_element_located((criteria, name)))

    def load_week(self, week: datetime.date | int = None):
        """Load a week from the webuntis website"""
        if week is None:
            week = datetime.date.today()
            self.current_week = week.isocalendar().week
        if isinstance(week, int):
            week = datetime.date.fromisocalendar(datetime.datetime.now().year, week, 1)
        if week.isocalendar().week in self.weeks:
            return
        self.get_page(self.TIMETABLE_PAGE + "/" + week.strftime("%Y-%m-%d"), By.ID, "embedded-webuntis")
        try:
            self.get_iframe(By.CLASS_NAME, "renderedEntry")
            self.weeks[week.isocalendar().week] = scrape_week(week, self.page_source)
            logging.getLogger("app").info(f"Week {week.isocalendar().week} loaded...")
        except:
            HTTPException(404, "No Data Found")

    def load_weeks(self, *weeks: int | datetime.date):
        """Load multiple weeks from the webuntis website"""
        for week in weeks:
            self.load_week(week)


if __name__ == '__main__':
    driver = WebuntisDriver()
    driver.login()
    print(driver.load_week(datetime.date.today()))
    driver.close()
