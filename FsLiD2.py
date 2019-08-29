from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from time import sleep
import random


youtube_url = input('URL YT VIDEO =>')
while True:
    mode = int(input('setmode like=0, dislike=1 =>'))
    if mode == 0:
        break
    elif mode == 1:
        break
    else:
        pass



def signinGoogle(login, password):
    """Авторизация в google аккаунте """
    browser = webdriver.Chrome()
    browser.implicitly_wait(8)
    url_signin = 'https://accounts.google.com/signin/v2/identifier?service=youtube&uilel=3&passive=true&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Dru%26next%3D%252F&hl=ru&flowName=GlifWebSignIn&flowEntry=ServiceLogin'

    browser.get(url_signin)
    email_area = browser.find_element_by_xpath('//*[@id="identifierId"]')
    email_area.send_keys(login)

    sumbit_button = browser.find_element_by_xpath('//*[@id="identifierNext"]')
    sumbit_button.click()

    pass_area = browser.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')
    pass_area.send_keys(password)

    sleep(1)
    sumbit_button = browser.find_element_by_xpath('//*[@id="passwordNext"]')
    sumbit_button.click()

    return browser


def setFrstAcc(browser):
    """залогинивание в первый канал ютуба """
    account_set = browser.find_element_by_xpath('//*[@id="identity-prompt-account-list"]/ul/label[1]/li/span/span[1]/input')
    account_set.click()

    ok_button = browser.find_element_by_xpath('//*[@id="identity-prompt-confirm-button"]/span')
    ok_button.click()


def checkCount(browser):
    """Подсчёт количества привязаных каналов на аккаунт"""
    avatar_button = browser.find_element_by_xpath('//*[@id="avatar-btn"]')
    avatar_button.click()
    change_acc_button = browser.find_element_by_xpath('//*[@id="items"]/ytd-compact-link-renderer[4]')
    change_acc_button.click()
    accs = browser.find_elements_by_xpath('//*[@id="contents"]/ytd-account-item-renderer')
    # acc = browser.find_element_by_xpath('//*[@id="contents"]/ytd-account-item-renderer[1]')
    # acc.click()
    print('Каналов на данном аккаунте:{}'.format(str(len(accs))))
    return accs


def dislikes(browser):
    """Выгрузка дизлайков на видео"""
    try:
        sleep(random.uniform(3, 10))
        dis = browser.find_element_by_xpath('//*[@id="top-level-buttons"]/ytd-toggle-button-renderer[2]')
        dis.click()
    except:
        pass


def likes(browser):
    """Выгрузка лайков на видео"""
    try:
        sleep(random.uniform(3, 10))
        like = browser.find_element_by_xpath('//*[@id="top-level-buttons"]/ytd-toggle-button-renderer[1]')
        like.click()
    except:
        pass


file = open('email_pass.txt')
logins = [line.strip() for line in file]
file.close()
for login in logins:
    login = login.split(':')
    email = login[0]
    password = login[1]
    browser = signinGoogle(email, password)
    try:
        setFrstAcc(browser)
    except:
        pass
    accs = checkCount(browser)
    browser.get(youtube_url)

    i = 1
    for acc in accs:
        sleep(random.uniform(0, 2))
        avatar_button = browser.find_element_by_xpath('//*[@id="avatar-btn"]')
        avatar_button.click()

        change_acc_button = browser.find_element_by_xpath('//*[@id="items"]/ytd-compact-link-renderer[4]')
        change_acc_button.click() # ошибка в поиске кнопки
        try:
            acc = browser.find_element_by_xpath('//*[@id="contents"]/ytd-account-item-renderer[{}]'.format(str(i)))
            acc.click()
        except:
            break
        if mode == 0:
            likes(browser)
        elif mode == 1:
            dislikes(browser)
        i += 1

    if mode == 0:
        likes(browser)
    elif mode == 1:
        dislikes(browser)
    browser.close()
print('Done!')
