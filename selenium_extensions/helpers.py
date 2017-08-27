import time

from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException


def kill_virtual_display(self, display):
    '''Kills virtual display created by ``pyvirtualdisplay.Display()``

    Args:
        display (pyvirtualdisplay.Display): display to kill.

    Example:
        ::

            from selenium_extensions.helpers import kill_virtual_display


            display = Display(visible=0, size=(1024, 768))
            display.start()
            ...
            kill_virtual_display(display)
    '''
    display.sendstop()


def element_has_gone_stale(element):
    '''Checks if element has gone stale

    Args:
        element (selenium.webdriver.remote.webelement.WebElement): Selenium webelement to check for.

    Returns:
        bool: True if element has gone stale, False otherwise.

    Examples:
        ::

            from selenium_extensions.helpers import element_has_gone_stale


            if element_has_gone_stale(your_element):
                pass  # Do something

        ::

            from selenium_extensions.helpers import wait_for_function_truth
            from selenium_extensions.helpers import element_has_gone_stale


            login_btn = driver.find_element_by_class_name('login_btn')
            wait_for_function_truth(element_has_gone_stale, element)
    '''
    try:
        # Poll the object with an arbitrary call
        element.find_elements_by_id('non-existing-id')
        return False
    except StaleElementReferenceException:
        return True


def wait_for_function_truth(condition_function, *args, time_to_wait=10, time_step=0.1):
    '''Waits for function represented by ``condition_function`` to return any non-False value

    Args:
        condition_function (function): function to wait for.
        *args: arguments that should be applied to the function.
        time_to_wait (int): time in seconds to wait.
        time_step (float): step in seconds between checks.

    Returns:
        bool: True if ``wait_for_function_truth`` succeeded and didn't reach ``time_to_wait`` limit

    Raises:
        selenium.common.exceptions.TimeoutException: timeout waiting for function described by ``condition_function`` to return any non-False value.

    Example:
        ::

            from selenium_extensions.helpers import wait_for_function_truth
            from selenium_extensions.helpers import element_has_gone_stale


            login_btn = driver.find_element_by_class_name('login_btn')
            wait_for_function_truth(element_has_gone_stale, element)
    '''
    start_time = time.time()
    while time.time() < start_time + time_to_wait:
        if condition_function(*args):
            return True
        else:
            time.sleep(time_step)
    raise TimeoutException(
        'Timeout waiting for {}'.format(condition_function.__name__)
    )


def join_css_classes(*args):
    '''Joins css classes into a single string

    Args:
        *args: arguments that represent classes that should be joined.

    Returns:
        str: a single string representing all of the classes.

    Examples:
        ::

            from selenium_extensions.helpers import join_css_classes


            classes = join_css_classes('class1', 'class2')
            print(classes)  # '.class2 .class2'
    '''
    return ' '.join(['.{}'.format(c) for c in args])
