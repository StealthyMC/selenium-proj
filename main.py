from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pyvirtualdisplay import Display

# standard python imports
import re
import logging
import signal   # for catching SIGINT signal
import time

RECOMMENDED_MIN_WAIT_TIME = 10

driver = None
display = None

def test(url, xpath=None):
    # Open a website
    try:
        driver.get(url)
        if xpath is not None:
            search_box = driver.find_element_by_xpath(xpath)
            search_box.send_keys("mouse") # 
            search_box.send_keys(Keys.RETURN)
        print(driver.page_source.encode("utf-8"))
    except Exception as e:
        print(e)
        _exit(driver, display)

def wait_for_stock(url, wait_time):
    """Wait for product to enter a state where it's in stock.
    Sends a request to the [url] provided using [driver], checks to see if the product is in stock
    using a regular expression. 
    If there's a match, the [driver] will perform another check every [wait_time] (in seconds)
    """
    logging.info(f'Connecting to [{url}]\nWaiting {wait_time} seconds between each check.')
    
    # oos = out of stock
    oos_regex = re.compile(r'sold out|out of stock')
    get_webpage(url)
    page_contents = driver.page_source
    
    # get the web page every [wait_time] seconds until there's no match for regex
    try:
        while oos_regex.search(page_contents) is not None:
            logging.info(f'Product seems to be out of stock. Will check again in {wait_time} seconds.')
            if wait_time < RECOMMENDED_MIN_WAIT_TIME:
                logging.warning(f'{wait_time} seconds is a low wait time. Connecting to a website too often may result in your IP being blacklisted.')
            time.sleep(wait_time)   # sleep for [wait_time] seconds
    except Exception as e:
        logging.error(e)
        _exit()
    logging.info('Product seems to be in stock.')

def get_webpage(url):
    try:
        driver.get(url)
    except Exception as e:
        logging.error(e)
    
def _keyboard_interrupt_handler(signal, frame):
    logging.warning(f'KeyboardInterrupt (ID: {signal}) caught.')
    _exit()
    pass

def _exit():
    """Exit wrapper function.
    Ensures that the bot exits cleanly, and cleans up the chrome driver and Xvfb display
    to prevent rogue processes. 
    """
    logging.info('Cleaning up before shutting down bot...')
    if driver is not None:
        logging.info('Stopping driver...')
        driver.quit()
        logging.info('Driver stopped.')
    if display is not None:
        logging.info('Stopping virtual display...')
        display.stop()
        logging.info('Virtual display closed.')
    logging.info('Cleanup complete. Exiting.')
    exit(0)

# --------- Program execution begins here --------- #

# Start logger
logging.basicConfig(level=logging.DEBUG)
logging.info("Initializing bot...")

# Start OS signal handler
# This will allow the process to catch SIGINT signals, which occurs when the user
# presses CTRL-C anytime the program is in execution
signal.signal(signal.SIGINT, _keyboard_interrupt_handler)

# Initialize virtual display, needed in order to start chromium-browser
logging.info("Starting virtual display...")
try:
    display = Display(visible=0, size=(800, 600))
    display.start()
except Exception as e:
    logging.error(e)
    _exit()
logging.info("Virtual display initialized successfully.")

# Set arguments to use for browser 
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.binary_location = "/usr/bin/chromium-browser"

# Create and start web driver, setup is complete with this step
logging.info("Starting web driver...")
try:
    driver = webdriver.Chrome(options=options)
except Exception as e:
    logging.error(e)
    _exit()
logging.info("Web driver started successfully.")

# Testing
# test(driver, 'https://store.gamersnexus.net/', '/html/body/div[1]/div[4]/div/div/div/div/div[2]/div/div/div/input')

wait_for_stock('https://www.supremenewyork.com/shop/skate/i4sk7m86j', 15)

_exit()