from selenium import webdriver
from pyvirtualdisplay import Display
import xvfbwrapper
#from webdriver_manager.chrome import ChromeDriverManager

# Initialize virtual display, needed in order to start chromium-browser
display = Display(visible=0, size=(800, 600))
display.start()

# Set arguments to use for browser 
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--test-type')
options.add_argument("--headless")
#options.binary_location = "/usr/lib/chromium-browser/chromedriver"
options.binary_location = "/usr/bin/chromium-browser"
# Create driver
driver = webdriver.Chrome(options=options)

# Open a website
driver.get('http://example.com/')
print(driver.page_source.encode("utf-8"))
driver.quit()

testvar2 = 0