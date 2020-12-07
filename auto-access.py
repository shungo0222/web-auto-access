import os
import time
import datetime
import configparser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

DIR_PATH = os.path.dirname(__file__)
CHROMEDRIVER_PATH = os.path.join(DIR_PATH, 'chromedriver.exe')
LOG_PATH = os.path.join(DIR_PATH, 'log')

config = configparser.ConfigParser()
config.read(os.path.join(DIR_PATH, 'config.ini'))

def access(chromedriver, url, username, password, headless):
    # options setting
    options = Options()
    if headless:
        # headless(background) mode
        options.add_argument('--headless')
    
    # set chrome driver
    driver = webdriver.Chrome(executable_path=chromedriver, options=options)

    # wait until loading is complete
    driver.implicitly_wait(5)

    # go to the login page
    driver.get(url)

    # login
    driver.find_element_by_xpath('//*[@id="username"]').send_keys(username)
    driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)
    driver.find_element_by_xpath('//*[@id="loginbtn"]').click()

    # get login time
    dt_now = datetime.datetime.now()

    # move to the specific page
    driver.find_element_by_xpath('//*[@id="frontpage-course-list"]/div/div[2]/div[1]/h3/a').click()
    
    ##############################
    # do anything you want to do #
    ##############################

    driver.close()
    driver.quit()
    
    return dt_now

def save_access_time(time, dir_path):
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)
    
    file_path = os.path.join(dir_path, f'{str(datetime.date.today())}.log')
    
    with open(file_path, mode='a') as f:
        print(time.strftime('%Y/%m/%d %H:%M:%S'), file=f)

def stop(time):
    dt = datetime.date.today()
    tm = datetime.time(int(config['DEFAULT']['hour']), \
                        int(config['DEFAULT']['minute']), \
                        int(config['DEFAULT']['second']))
    stop_time = datetime.datetime.combine(dt, tm)
    if time > stop_time:
        exit()

def main():
    while True:
        try:
            access_time = access(chromedriver=CHROMEDRIVER_PATH, \
                                url=config['DEFAULT']['url'], \
                                username=config['DEFAULT']['username'], \
                                password=config['DEFAULT']['password'], \
                                headless=int(config['DEFAULT']['headless']))
            print(access_time)
            save_access_time(time=access_time, dir_path=LOG_PATH)
            stop(access_time)
        except KeyboardInterrupt as e:
            print(e)
            exit()
        except:
            print('Error')
            stop(datetime.datetime.now())
        time.sleep(int(config['DEFAULT']['interval']))

if __name__ == '__main__':
    main()