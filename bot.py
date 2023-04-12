import datetime
import random
import wikiquotes

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

name = 'Joseph Stalin'
nick = 'Towarzysz'

print('Starting bot...')

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')  # Last I checked this was necessary.
driver = webdriver.Chrome(options=options)


def move_and_click(element):
    move = ActionChains(driver)
    move.move_to_element(element)
    move.perform()
    driver.execute_script('window.scrollBy(0,300)')
    element.click()


def type_text(text):
    actions = ActionChains(driver)
    actions.send_keys(text)
    actions.perform()


driver.get("https://www.wp.pl/")
no_comment_section = True

driver.find_element(By.XPATH, '//button[contains(text(), \'AKCEPTUJĘ I PRZECHODZĘ DO SERWISU\')]').click()
sleep(1)

while no_comment_section:
    no_comment_section = False
    move_and_click(random.choice(driver.find_elements(By.XPATH, '//a[@data-testid="link-box-item"]')[:12]))
    sleep(1)

    try:
        move_and_click(driver.find_element(By.XPATH,
                                '//*[contains(text(), \'Dzieci widzą i słyszą. #StopMowieNienawiści.\')]'))
        sleep(1)
    except:
        driver.get("https://www.wp.pl/")
        no_comment_section = True
        print('No comment section')


type_text(wikiquotes.random_quote(name, 'english'))  # polski nie supportowany :(
sleep(1)

move_and_click(driver.find_element(By.XPATH, '//input[@placeholder="Twój nick"]'))
sleep(1)
type_text(nick)
sleep(1)

driver.find_element(By.XPATH, '//button[contains(text(), \'Wyślij\')]').click()
sleep(1)

driver.save_screenshot('{}.png'.format(datetime.datetime.now().timestamp()))
