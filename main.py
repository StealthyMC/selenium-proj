from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pyvirtualdisplay import Display

def _exit(driver, display):
    """Exit wrapper function.
    Ensures that the web driver exits cleanly, and cleans up the chrome driver and Xvfb display
    to prevent rogue processes. 
    """
    driver.quit()
    display.stop()

# Initialize virtual display, needed in order to start chromium-browser
display = Display(visible=0, size=(800, 600))
display.start()

# Set arguments to use for browser 
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
#options.add_argument('--test-type')
#options.add_argument("--headless")
#options.binary_location = "/usr/lib/chromium-browser/chromedriver"
options.binary_location = "/usr/bin/chromium-browser"
# Create driver
driver = webdriver.Chrome(options=options)

# Setup complete

# Open a website
#driver.get('https://www.instagram.com/')
driver.get('https://store.gamersnexus.net/')
#WebDriverWait(driver, 5).until(EC.frame_to_be_available_and_switch_to_it((By.CLASS_NAME, "KPnG0")))
try:
    search_box = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div/div/div/div/div[2]/div/div/div/input')
    search_box.send_keys("mouse")
    search_box.send_keys(Keys.RETURN)
    print(driver.page_source.encode("utf-8"))
    #print(driver)
except Exception as e:
    print(e)
    _exit(driver, display)
#driver.find_element_by_id('loginForm')
#print(driver.page_source.encode("utf-8"))

_exit(driver, display)
