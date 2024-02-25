import datetime
import random
import names

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

nick = names.get_first_name()
ua = UserAgent()
user_agent = ua.random

print('Starting bot...')
print(f'User Agent = {user_agent}')

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')  # Last I checked this was necessary.
options.add_argument(f'--user-agent={user_agent}')
driver = webdriver.Chrome(options=options)


def move_and_click(element):
    move = ActionChains(driver)
    move.move_to_element(element)
    move.perform()
    driver.execute_script('window.scrollBy(0,400)')
    element.click()


def type_text(text):
    actions = ActionChains(driver)
    actions.send_keys(text)
    actions.perform()


driver.get("https://www.wp.pl/")
fail = True

driver.find_element(By.XPATH, '//button[contains(text(), \'AKCEPTUJĘ I PRZECHODZĘ DO SERWISU\')]').click()
sleep(1)

while fail:
    fail = False

    # noinspection PyBroadException
    try:
        move_and_click(random.choice(driver.find_elements(By.XPATH, '//a[@data-testid="link-box-item"]')[:12]))
    except:
        print('Something covering article links')
        fail = True
        driver.get("https://www.wp.pl/")
        sleep(1)
        continue

    sleep(1)

    # noinspection PyBroadException
    try:
        driver.find_element(By.XPATH, '//button[contains(text(), \'AKCEPTUJĘ I PRZECHODZĘ DO SERWISU\')]').click()
        sleep(1)
    except:
        pass

    # noinspection PyBroadException
    try:
        move_and_click(driver.find_element(By.XPATH,
                                '//*[contains(text(), \'Dzieci widzą i słyszą. #StopMowieNienawiści.\')]'))
        sleep(1)
    except:
        driver.get("https://www.wp.pl/")
        fail = True
        print('No comment section')
        sleep(1)
        continue

    type_text('memeg. eu - Twórz własne memy ze swoich zdjęć i obrazków!')
    sleep(1)

    # noinspection PyBroadException
    try:
        move_and_click(driver.find_element(By.XPATH, '//input[@placeholder="Twój nick"]'))
        sleep(1)
        type_text(nick)
        sleep(1)
    except:
        driver.get("https://www.wp.pl/")
        fail = True
        print('No nick input')
        sleep(1)
        continue

    # noinspection PyBroadException
    try:
        driver.find_element(By.XPATH, '//button[contains(text(), \'Wyślij\')]').click()
        sleep(1)
    except:
        driver.get("https://www.wp.pl/")
        fail = True
        print('No send button')
        sleep(1)
        continue

driver.save_screenshot('{}.png'.format(datetime.datetime.now().timestamp()))
print('Screenshot saved')
