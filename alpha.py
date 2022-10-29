import csv
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium.webdriver.chrome.service import Service

def create_webdriver_instance():
    options = Options()
    options.headless = False
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    return driver

def chrome_profile():
    """
        Use this for specific chrome profile
    """
    #options = webdriver.ChromeOptions() 
    s = Service("C:\Program Files\Google\Chrome\Application\chrome.exe")
    driver = webdriver.Chrome(service=s)
    #options = Options()
    #options.headless = True
    #options.add_argument("user-data-dir=C:\\Users\\Sensei\\AppData\\Local\\Google\\Chrome\\User") #Path to your chrome profile
    #w = webdriver.Chrome(executable_path="C:\Program Files\Google\Chrome\Application\chrome.exe", options=options)
    #w.maximize_window()
    return driver

def scroll_down_page(driver, last_position, num_seconds_to_load=5, scroll_attempt=0, max_attempts=5):
    end_of_scroll_region = False
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    sleep(num_seconds_to_load)
    curr_position = driver.execute_script("return window.pageYOffset;")
    if curr_position == last_position:
        if scroll_attempt < max_attempts:
            end_of_scroll_region = True
        else:
            scroll_down_page(last_position, curr_position, scroll_attempt + 1)
    last_position = curr_position
    return last_position, end_of_scroll_region

def extract_video_card_from_current_view(driver):
    last_position = None
    end_of_scroll_region = False
    while not end_of_scroll_region:
        try:
            video_cards = driver.find_elements(By.XPATH, "//div[@class='tiktok-x6y88p-DivItemContainerV2 e19c29qe7']")
        except exceptions.NoSuchElementException:
            video_cards = None
        last_position, end_of_scroll_region = scroll_down_page(driver, last_position)
        sleep(5)
    return video_cards

def extract_links(video_cards):
    video_links = []
    for video_card in video_cards:
        try:
            video_link = video_card.find_element(By.TAG_NAME, 'a').get_attribute('href')
        except exceptions.NoSuchElementException:
            video_link = ""
        except exceptions.StaleElementReferenceException:
            return
        else:
            video_links.append(video_link)
    return video_links

def download_video(driver,video_links):
    for video_link in video_links:
        driver.get("https://snaptik.app")
        sleep(10)
        try:
            driver.find_element(By.XPATH, "//input[@id='url']").send_keys(video_link)
            driver.find_element(By.XPATH, "//button[@class='btn btn-go flex-center']").send_keys(Keys.RETURN)
        except exceptions.NoSuchElementException:
            return None
        else:
            sleep(10)
            link = driver.find_element(By.XPATH, "//a[@class='btn btn-main active mb-2']").get_attribute('href')
            #driver.get(link)
            print(link)
            sleep(10)
            driver.get("https://snaptik.app")



def main(filepath):
    search_url = input("Enter the User Profile Url : ")
    driver = create_webdriver_instance()
    driver.get(search_url)
    sleep(10)
    video_cards = extract_video_card_from_current_view(driver)
    if len(video_cards) > 0 :
        video_links = extract_links(video_cards)
    print(len(video_links))
    print(video_links)
    download_video(driver,video_links)
    sleep(100)
    driver.close()

if __name__ == '__main__':
    path = 'Twitter.csv'
    
    main(path)