from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


class DriverConfig:
    def __init__(self) -> None:
        self.delay_time = 5
        self.implicitly_wait = 4


class ChromeDriver:
    def __init__(self, config: DriverConfig) -> None:
        self.config = config

    def load(self):
        caps = {}
        caps["pageLoadStrategy"] = "none"
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.set_capability("cloud:options", caps)
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(self.config.implicitly_wait)

        wait = WebDriverWait(driver, self.config.delay_time)
        return driver, wait


chrome_driver, wait = ChromeDriver(DriverConfig()).load()
