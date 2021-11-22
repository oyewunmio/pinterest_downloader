from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import urllib.request
import os


pathname = input('Enter the name of the folder to store the downloaded images to\t')

#web driver configuration
chrome_options = Options()
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.headless = False
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
ua = UserAgent(use_cache_server=False)

#file managing configuration
if not os.path.isdir(pathname):
    os.makedirs(pathname)
    prefs = {"profile.managed_default_content_settings.images": 2, 'download.default_directory' : os.path.join(os.getcwd(), pathname)}
    chrome_options.add_experimental_option("prefs", prefs)
else:
    prefs = {"profile.managed_default_content_settings.images": 2, 'download.default_directory' : os.path.join(os.getcwd(), pathname)}

userAgent = ua.random
chrome_options.add_argument(f'user-agent={userAgent}')
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)


def get_pin(pin_url):
    """
    get src of requested pin image
    """

    url = 'https://www.expertstrick.com/pinterest-image-downloader/'
    driver.get(url)
    timeout = 10

    try:
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="login-form"]/center/button')))

        search_bar = driver.find_element(By.XPATH, '//*[@id="login-form"]/input')
        search_bar.send_keys(pin_url)
        search_bar.send_keys(Keys.ENTER)

        
        element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="post-7"]/div[2]/a'))
        WebDriverWait(driver, timeout).until(element_present)

        download_pin_src = driver.find_element(By.XPATH, '//*[@id="post-7"]/div[2]/a').get_attribute('href')

        urllib.request.urlretrieve(download_pin_src, str(download_pin_src).split('/')[-1])


    except TimeoutException:
        print("Timed out waiting for page to load..check your network connectivty")

get_pin('https://www.pinterest.com/pin/821907000749857407/')