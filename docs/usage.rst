=====
Usage
=====

There are three submodules you will look into for different utils:

Drivers
-------

Provides shortcuts for drivers creation.

Available tools are:

- :func:`selenium_extensions.drivers.chrome_driver` - function to initialize ``selenium.webdriver.Chrome`` with extended options.
- :func:`selenium_extensions.drivers.firefox_driver` - function to initialize ``selenium.webdriver.Firefox`` with extended options.

Core
----

Provides core functionality of the package. All of the function from this module directy access the webdriver and its state.

Available tools are:

- :func:`selenium_extensions.core.shut_down` - shuts down the driver and its virtual display.
- :func:`selenium_extensions.core.scroll` - scrolls the current page or the Selenium WebElement if one is provided.
- :func:`selenium_extensions.core.click_on_element` - clicks on a Selenium element represented by ``element_locator``.
- :func:`selenium_extensions.core.element_is_present` - shortcut to check if the element is present on the current page.
- :func:`selenium_extensions.core.wait_for_element_to_be_present` - shortcut to wait until the element is present on the current page.
- :func:`selenium_extensions.core.wait_for_element_to_be_clickable` - waits for element described by `element_locator` to be clickable.
- :func:`selenium_extensions.core.populate_text_field` - populates text field with provided text.
- :class:`selenium_extensions.core.SeleniumDriver` - base class for selenium-based drivers. User's classes should inherit from this class and initialize it using ``super()``. After this their class will have ``driver`` attribute and all the methods ready to go.


Helpers
-------

Provides helpers for writing things using Selenium.

Available tools are:

- :func:`selenium_extensions.helpers.kill_virtual_display` - kills virtual display created by ``pyvirtualdisplay.Display()``.
- :func:`selenium_extensions.helpers.element_has_gone_stale` - checks if element has gone stale.
- :func:`selenium_extensions.helpers.wait_for_function_truth` - waits for function represented by ``condition_function`` to return any non-False value.
- :func:`selenium_extensions.helpers.join_css_classes` - joins css classes into a single string.

About ``core.SeleniumDriver``
-----------------------------

:class:`selenium_extensions.core.SeleniumDriver` provides all of the tools available in ``selenium_extensions.core`` in a single class. It also can create driver by calling ``super()`` from child class and then use it for all the ``selenium_extensions.core`` functionality, **so you don't need to provide driver as the first argument to SeleniumDriver's methods**. Let's look at some code:


.. code-block:: python

    from selenium.webdriver.common.by import By
    from selenium_extensions.core import SeleniumDriver


    class MyBot(SeleniumDriver):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def goto_google(self):
            self.driver.get('https://google.com')
            searchbox_locator = (By.ID, 'lst-ib')
            # core.wait_for_element_to_be_present is now available as self.wait_for_element_to_be_present
            self.wait_for_element_to_be_present(searchbox_locator)
            # core.populate_text_field is now available as self.populate_text_field
            self.populate_text_field(searchbox_locator, 'query')


    bot = MyBot(browser='chrome', executable_path='/usr/bin/chromedriver', run_headless=True, load_images=False)
    bot.goto_google()
    bot.shut_down()  # core.shut_down() is now available as self.shut_down()


Another option, if you don't enjoy OOP style, would be we just to initialize ``SeleniumDriver`` and use its ``driver`` attribute to do whatever you want. So the code above could look like this:

.. code-block:: python

    from selenium.webdriver.common.by import By
    from selenium_extensions.core import SeleniumDriver


    bot = SeleniumDriver(browser='chrome', executable_path='/usr/bin/chromedriver',
                         run_headless=False, load_images=False)
    bot.driver.get('https://google.com')
    searchbox_locator = (By.ID, 'lst-ib')
    bot.wait_for_element_to_be_present(searchbox_locator)
    bot.populate_text_field(searchbox_locator, 'query')
    bot.shut_down()