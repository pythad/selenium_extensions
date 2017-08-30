from functools import partial

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from selenium_extensions.drivers import chrome_driver
from selenium_extensions.drivers import firefox_driver

from selenium_extensions.helpers import kill_virtual_display

from selenium_extensions.exceptions import SeleniumExtensionsException


def shut_down(driver):
    '''Shuts down the driver and its virtual display

    Args:
        driver (selenium.webdriver.): Selenium webdriver to stop.

    Example:
        ::

            from selenium import webdriver
            from selenium_extensions.core import shut_down


            driver = webdriver.Chrome()
            ...
            shut_down(driver)
    '''
    driver.quit()
    try:
        kill_virtual_display(driver.display)
    except (AttributeError, TypeError):
        # Display is either None or there is no display at all
        pass


def scroll(driver, scroll_element=None):
    '''Scrolls the current page or the Selenium WebElement if one is provided

    Args:
        driver (selenium.webdriver.): Selenium webdriver to use.
        scroll_element (selenium.webdriver.remote.webelement.WebElement): Selenium webelement to scroll.

    Examples:
        ::

            from selenium import webdriver
            from selenium_extensions.core import scroll


            driver = webdriver.Chrome()
            scroll(driver)

        ::

            from selenium import webdriver
            from selenium_extensions.core import scroll


            driver = webdriver.Chrome()
            ...
            pop_up = driver.find_element_by_class_name('ff_pop_up')
            scroll(driver, pop_up)
    '''
    if scroll_element:
        driver.execute_script(
            'arguments[0].scrollTop = arguments[0].scrollHeight;', scroll_element)
    else:
        driver.execute_script(
            'document.body.scrollTop = document.body.scrollHeight;')


def click_on_element(driver, element_locator):
    '''Clicks on a Selenium element represented by ``element_locator``

    Args:
        element_locator ((selenium.webdriver.common.by.By., str)): element locator described using `By`. Take a look at `Locate elements By <http://selenium-python.readthedocs.io/api.html#locate-elements-by>`_ for more info.

    Example:
        ::

            from selenium import webdriver
            from selenium.webdriver.common.by import By
            from selenium_extensions.core import click_on_element


            driver = webdriver.Chrome()
            ...
            click_on_element(driver, (By.ID, 'form-submit-button'))
    '''
    element = driver.find_element(*element_locator)
    element.click()


def element_is_present(driver, element_locator, waiting_time=2):
    '''Shortcut to check if the element is present on the current page

    Args:
        driver (selenium.webdriver.): Selenium webdriver to use.
        element_locator ((selenium.webdriver.common.by.By., str)): element locator described using `By`. Take a look at `Locate elements By <http://selenium-python.readthedocs.io/api.html#locate-elements-by>`_ for more info.
        waiting_time (int): time in seconds - describes how much to wait.

    Returns:
        bool: True if the element is present on the current page, False otherwise.

    Example:
        ::

            from selenium import webdriver
            from selenium.webdriver.common.by import By
            from selenium_extensions.core import element_is_present


            driver = webdriver.Chrome()
            ...
            if not element_is_present(driver, (By.CLASS_NAME, 'search_photos_block')):
                pass # Do your things here
    '''
    try:
        WebDriverWait(driver, waiting_time).until(
            EC.presence_of_element_located(element_locator))
        return True
    except TimeoutException:
        return False


def wait_for_element_to_be_present(driver, element_locator, waiting_time=2):
    '''Shortcut to wait until the element is present on the current page

    Args:
        driver (selenium.webdriver.): Selenium webdriver to use.
        element_locator ((selenium.webdriver.common.by.By., str)): element locator described using `By`. Take a look at `Locate elements By <http://selenium-python.readthedocs.io/api.html#locate-elements-by>`_ for more info.
        waiting_time (int): time in seconds - describes how much to wait.

    Raises:
        selenium.common.exceptions.TimeoutException: timeout waiting for element described by ``element_locator``.

    Example:
        ::

            from selenium import webdriver
            from selenium.webdriver.common.by import By
            from selenium_extensions.core import wait_for_element_to_be_present


            driver = webdriver.Chrome()
            ...
            wait_for_element_to_be_present(driver, (By.CLASS_NAME, 'search_load_btn'))
    '''
    try:
        WebDriverWait(driver, waiting_time).until(
            EC.presence_of_element_located(element_locator))
    except TimeoutException:
        raise TimeoutException(
            'Timeout waiting for {} presense'.format(element_locator[1]))


def wait_for_element_to_be_clickable(driver, element_locator, waiting_time=2):
    '''Waits for element described by `element_locator` to be clickable

    Args:
        element_locator ((selenium.webdriver.common.by.By., str)): element locator described using `By`. Take a look at `Locate elements By <http://selenium-python.readthedocs.io/api.html#locate-elements-by>`_ for more info.
        waiting_time (int): time in seconds - describes how much to wait.

    Raises:
        selenium.common.exceptions.TimeoutException: timeout waiting for element described by ``element_locator``.

    Example:
        ::

            from selenium import webdriver
            from selenium.webdriver.common.by import By
            from selenium_extensions.core import wait_for_element_to_be_clickable


            driver = webdriver.Chrome()
            ...
            wait_for_element_to_be_clickable(driver, (By.CLASS_NAME, 'form-submit-button'))
    '''
    try:
        WebDriverWait(driver, waiting_time).until(
            EC.element_to_be_clickable(element_locator))
    except TimeoutException:
        raise TimeoutException(
            'Timeout waiting for {} element to be clickable'.format(element_locator[1]))


def populate_text_field(driver, element_locator, text):
    '''Populates text field with provided text

    Args:
        element_locator ((selenium.webdriver.common.by.By., str)): element locator described using `By`. Take a look at `Locate elements By <http://selenium-python.readthedocs.io/api.html#locate-elements-by>`_ for more info.
        text (str): text to populate text field with.

    Example:
        ::

            from selenium import webdriver
            from selenium.webdriver.common.by import By
            from selenium_extensions.core import populate_text_field


            driver = webdriver.Chrome()
            ...
            populate_text_field(driver, (By.CLASS_NAME, 'textbox'), 'some text')
    '''
    input_element = driver.find_element(*element_locator)
    input_element.send_keys(text)


class SeleniumDriver:
    '''Base class for selenium-based drivers

    User's classes should inherit from this class and initialize it using ``super()``. After this their class will have ``driver`` attribute and all the methods ready to go.

    Args:
        browser ('chrome' or 'firefox'): webdriver to use.
        executable_path (str): path to the browser's webdriver binary. If set to ``None`` selenium will serach for browser's webdriver in ``$PATH``.
        run_headless (bool): boolean flag that indicates if webdriver has to be headless (without GUI).
        load_images (bool): boolean flag that indicates if webdriver has to render images.

    Raises:
        selenium_extensions.exceptions.SeleniumExtensionsException: ``browser`` is not supported by ``selenium_extensions``.

    Example:
        ::

            from selenium_extensions.core import SeleniumDriver


            class MyBot(SeleniumDriver):

                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)

                def goto_google(self):
                    self.driver.get('https://google.com')


            bot = MyBot(browser='chrome', executable_path='/usr/bin/chromedriver', run_headless=True, load_images=False)
            bot.goto_google()
            bot.shut_down()

    Note:
        In order to create Chrome driver Selenium requires `Chrome <https://www.google.com/chrome/browser/desktop/index.html>`_ to be installed and `chromedriver <https://sites.google.com/a/chromium.org/chromedriver/>`_ to be downloaded.

    Note:
        In order to create Firefox driver Selenium requires `Firefox <https://www.mozilla.org/en-US/firefox/new/>`_ to be installed and `geckodriver <https://github.com/mozilla/geckodriver/releases>`_ to be downloaded.

    Note:
        Firefox doesn't support native headless mode. We use ``pyvirtualdisplay`` to simulate it. In order ``pyvirtualdisplay`` to work you need to install ``Xvfb`` package: ``sudo apt install xvfb``.
    '''

    def __init__(self, browser=None, executable_path=None, run_headless=False, load_images=True):
        self._initialize_driver(browser, executable_path,
                                run_headless, load_images)
        self._initialize_methods()

    def _initialize_driver(self, browser, executable_path, run_headless, load_images):
        if browser is None:
            self.driver = chrome_driver()
            browser = browser.lower()
        available_browsers = ['chrome', 'firefox']
        if browser not in available_browsers:
            raise SeleniumExtensionsException('Provided browser ({}) isn\'t \
                supported by selenium_extensions package. Available browsers \
                are {}'.format(browser, ', '.join(available_browsers)))

        if browser == 'chrome':
            self.driver = chrome_driver(executable_path=executable_path,
                                        run_headless=run_headless,
                                        load_images=load_images)
        if browser == 'firefox':
            self.driver = firefox_driver(executable_path=executable_path,
                                         run_headless=run_headless,
                                         load_images=load_images)

    def _initialize_methods(self):
        self.shut_down = partial(shut_down, self.driver)
        self.scroll = partial(scroll, self.driver)
        self.click_on_element = partial(click_on_element, self.driver)
        self.element_is_present = partial(element_is_present, self.driver)
        self.wait_for_element_to_be_present = partial(
            wait_for_element_to_be_present, self.driver)
        self.wait_for_element_to_be_clickable = partial(
            wait_for_element_to_be_clickable, self.driver)
        self.populate_text_field = partial(populate_text_field, self.driver)
