from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
    NoSuchElementException,
    ElementNotInteractableException,
    WebDriverException
)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import functools
from time import sleep

import logging
logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(levelname)s - %(message)s")

# decoradores

def retry(retries=3, type="None | Bool"):
    """fun = safe_click"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            
            for attempt in range(retries):
                result = func(*args, **kwargs)

                if type == "Bool":
                    if result is True:
                        return True
                    
                if type == "None":
                    if result is not None:
                        return result
                    
                logging.warning(f"retry, tentativa = {attempt+1}, xpath = {args[1]}")
                sleep(1+attempt)
                
            return False
        return wrapper
    return decorator

# helpers universais

def options():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--incognito")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-notifications")
    return options

def find(driver, xpath, wait=10, all=False):
    """Localiza e retorna elemento com wait padrão."""
    try:
        if all:
            return WebDriverWait(driver, wait).until(EC.visibility_of_all_elements_located((By.XPATH, xpath)))
        else:
            return WebDriverWait(driver, wait).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    except (TimeoutException,
            StaleElementReferenceException,
            ElementClickInterceptedException,
            NoSuchElementException, 
            ElementNotInteractableException,
            WebDriverException
            ):
        return None 


def safe_click(driver, xpath, wait=10):
    """Clica em um elemento com espera explícita."""
    try:
        elem = WebDriverWait(driver, wait).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        elem.click()
        return True
    except (TimeoutException,
            StaleElementReferenceException,
            ElementClickInterceptedException,
            NoSuchElementException):
        return False

@retry(retries=3, type="None")
def web_driver():
    try:
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options())
    except:
        sleep(30)
        return None