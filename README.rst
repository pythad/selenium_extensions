===================
Selenium extensions
===================

.. image:: https://img.shields.io/pypi/pyversions/selenium_extensions.svg
        :target: https://pypi.python.org/pypi/selenium_extensions
        :alt: Supported python versions

.. image:: https://img.shields.io/pypi/v/selenium_extensions.svg
        :target: https://pypi.python.org/pypi/selenium_extensions
        :alt: PyPI version

.. image:: https://readthedocs.org/projects/selenium_extensions/badge/?version=latest
        :target: https://selenium_extensions.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/pythad/selenium_extensions/shield.svg
        :target: https://pyup.io/repos/github/pythad/selenium_extensions/
        :alt: Updates

.. image:: https://img.shields.io/github/license/pythad/selenium_extensions.svg
        :target: https://pypi.python.org/pypi/selenium_extensions
        :alt: License



Tools that will make writing tests, bots and scrapers using Selenium much easier


* Free software: MIT license
* Documentation: https://selenium-extensions.readthedocs.io.

************
Installation
************

.. code-block:: console

    $ pip install selenium_extensions

*******
Example
*******

Creating a headless Selenium bot and filling in a form is as easy as

.. code-block:: python

    from selenium.webdriver.common.by import By
    from selenium_extensions.core import SeleniumDriver


    class MyBot(SeleniumDriver):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def goto_google(self):
            self.driver.get('https://google.com')
            searchbox_locator = (By.ID, 'lst-ib')
            self.wait_for_element_to_be_present(searchbox_locator)
            self.populate_text_field(searchbox_locator, 'query')


    bot = MyBot(browser='chrome', executable_path='/usr/bin/chromedriver', headless=True)
    bot.goto_google()
    bot.shut_down()

Or do you want to wait until you will be redirected from login page? ``selenium_extensions`` makes it easy

.. code-block:: python

    from selenium_extensions.helpers import wait_for_function_truth
    from selenium_extensions.helpers import element_has_gone_stale


    ...
    login_btn = self.driver.find_element_by_css_selector(
        "button.submit.EdgeButton.EdgeButton--primary")
    login_btn.click()

    # Wait to be redirected
    wait_for_function_truth(element_has_gone_stale, login_btn)

********
Features
********

* ``selenium_extensions.drivers.chrome_driver`` - extended Chrome webdriver class with built-in support for headless mode and rendering webpages without media.
* ``selenium_extensions.drivers.firefox_driver`` - extended Firefox webdriver class with built-in support for headless mode and rendering webpages without media.
* ``selenium_extensions.core.scroll`` - scrolls the current page or the Selenium WebElement if one is provided.
* ``selenium_extensions.core.element_is_present`` - shortcut to check if the element is present on the current page.
* ``selenium_extensions.core.wait_for_element_to_be_clickable`` - waits for element described by `element_locator` to be clickable.
* ``selenium_extensions.helpers.element_has_gone_stale`` - checks if element has gone stale.
* ``selenium_extensions.core.SeleniumDriver`` - class with all necessary tools in one place. User's classes should inherit from this class and initialize it using ``super()``. After this their class will have ``driver`` attribute and all the methods ready to go.

and more.