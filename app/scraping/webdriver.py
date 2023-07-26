from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class WDriver:
    def getDriver(self):
        options = Options()
        options.add_argument("start-maximized")
        options.add_argument("enable-automation")
        options.add_argument("disable-infobars")
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-browser-side-navigation")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        prefs = {"profile.default_content_setting_values.notifications" : 2}
        options.add_experimental_option("prefs",prefs)
        driver = webdriver.Chrome(options=options)
        driver.set_window_size(1980, 1040)
        return driver
