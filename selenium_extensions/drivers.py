import os

from pyvirtualdisplay import Display
from selenium import webdriver


def chrome_driver(executable_path=None, run_headless=False,
                  load_images=True):
    '''Function to initialize ``selenium.webdriver.Chrome`` with extended options

    Args:
        executable_path (str): path to the chromedriver binary. If set to ``None`` selenium will serach for ``chromedriver`` in ``$PATH``.
        run_headless (bool): boolean flag that indicates if chromedriver has to be headless (without GUI).
        load_images (bool): boolean flag that indicates if Chrome has to render images.

    Returns:
        selenium.webdriver.Chrome: created driver.

    Note:
        In order to create Chrome driver Selenium requires `Chrome <https://www.google.com/chrome/browser/desktop/index.html>`_ to be installed and `chromedriver <https://sites.google.com/a/chromium.org/chromedriver/>`_ to be downloaded.

    Warning:
        Headless Chrome is shipping in Chrome 59 and in Chrome 60 for Windows. Update your Chrome browser if you want to use ``headless`` option.
    '''
    chrome_options = webdriver.ChromeOptions()
    if run_headless:
        chrome_options.add_argument('headless')
    if not load_images:
        prefs = {'profile.managed_default_content_settings.images': 2}
        chrome_options.add_experimental_option('prefs', prefs)
    if executable_path:
        driver = webdriver.Chrome(chrome_options=chrome_options,
                                  executable_path=executable_path)
    else:
        driver = webdriver.Chrome(chrome_options=chrome_options)
    return driver


def firefox_driver(executable_path=None, run_headless=False,
                   load_images=True):
    '''Function to initialize ``selenium.webdriver.Firefox`` with extended options

    Args:
        executable_path (str): path to the ``geckdriver`` binary. If set to ``None`` selenium will search for ``geckdriver`` in ``$PATH``.
        run_headless (bool): boolean flag that indicates if ``geckodriver`` has to be headless (without GUI). ``geckodriver`` doesn't support native headless mode, that's why ``pyvirtualdisplay`` is used.
        load_images (bool): boolean flag that indicates if Firefox has to render images.

    Returns:
        selenium.webdriver.Firefox: created driver.

    Note:
        In order to create Firefox driver Selenium requires `Firefox <https://www.mozilla.org/en-US/firefox/new/>`_ to be installed and `geckodriver <https://github.com/mozilla/geckodriver/releases>`_ to be downloaded.

    Note:
        Firefox doesn't support native headless mode. We use ``pyvirtualdisplay`` to simulate it. In order ``pyvirtualdisplay`` to work you need to install ``Xvfb`` package: ``sudo apt install xvfb``.
    '''
    firefox_profile = webdriver.FirefoxProfile()
    if run_headless:
        display = Display(visible=0, size=(1024, 768))
        display.start()
    else:
        display = None
    if not load_images:
        firefox_profile.add_extension(os.path.dirname(
            os.path.realpath(__file__)) +
            '/browser_extensions/firefox/quickjava-2.1.2-fx.xpi')
        # Prevents loading the 'thank you for installing screen'
        firefox_profile.set_preference(
            'thatoneguydotnet.QuickJava.curVersion', '2.1.2.1')
        # Turns images off
        firefox_profile.set_preference(
            'thatoneguydotnet.QuickJava.startupStatus.Images', 2)
        # Turns animated images off
        firefox_profile.set_preference(
            'thatoneguydotnet.QuickJava.startupStatus.AnimatedImage', 2)
    if executable_path:
        driver = webdriver.Firefox(
            firefox_profile, executable_path=executable_path)
    else:
        driver = webdriver.Firefox(firefox_profile)
    driver.display = display
    return driver
