'''
Created on Jul. 24, 2021
Twitter bot that scrapes data from a website containing daily updates on the changing currency exchange rates. Then, logs into, and posts the data onto Twitter.
@author: Tao
'''

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support import expected_conditions as EC
import time

# Creates path to chromedriver.
PATH = "C:\Program Files (x86)\chromedriver.exe"

# Creates driver using the created path.
driver = webdriver.Chrome(PATH)

# Declares empty strings for variables 'a', 'b', 'c', and 'date', which will later be filled.
a = ""
b = ""
c= ""
date = ""

# Opens the given website URL.
driver.get("https://www.bankofcanada.ca/rates/exchange/daily-exchange-rates/")

# Maximizes the window.
driver.maximize_window()

try:
    
    # Waits until the driver is open, or for a maximum of 10 seconds.
    wait = WebDriverWait(driver, 10)
    
    # Waits until all_data is visible.
    all_data = wait.until(ec.visibility_of_element_located((By.ID, "table_daily_1")))
    
    # Finds data.
    data = all_data.find_element_by_class_name("bocss-table__tbody")
    
    # Finds current date.
    current_date = all_data.find_element_by_xpath('//*[@id="table_daily_1"]/div/table/thead/tr/th[6]')
    date = current_date.text
    
    # Finds rows with data values.
    rows = data.find_elements_by_tag_name("tr")
    
    # Initializes a counter.
    count = 1
    
    # Declares a string as the current date.
    string = ""
    string += (current_date.text)
    
    # Loops for each row/until all data has been scraped.
    for row in rows:
        
        # Finds the name of each type of currency.
        name = row.find_element_by_tag_name("th")
        
        # XPATH for the current date's value of the currency.
        valuetext = "//*[@id='table_daily_1']/table[1]/tbody/tr["
        valuetext += str(count)
        valuetext += "]/td[5]"
        
        # Finds the value of the current date's value of the currency.
        value = row.find_element_by_xpath(valuetext)
        
        # Appends each new name and value to the string.
        if count != 9 or count != 17:
            string += ("\n")
        string += (name.text)
        string += (": ")
        string += (value.text)
        
        # Adds hyphens at certain locations for even splitting of the text.
        if count == 8 or count == 16:
            string += ("-")
        count = count + 1
        
    # Splits the text into 3 parts to follow Twitter's 280 max character limit.
    a, b, c = string.split('-')
except:
    driver.close()
    
# Logs into twitter.
def login():
    
    # Opens the given website URL.
    driver.get("https://twitter.com/login")
    
    # Maximizes the window.
    driver.maximize_window()
    time.sleep(3)
    
    # Waits until the website is opened, or for a maximum of 10 seconds.
    wait = WebDriverWait(driver, 10)
    time.sleep(1)
    
    # Stores the current string url.
    stringurl = driver.current_url
    
    # If the URL is regular.
    if stringurl == "https://twitter.com/login":
        
        # Waits until the username box is located, then inputs the username.
        username_input = wait.until(ec.visibility_of_element_located((By.NAME, "session[username_or_email]")))
        username_input.send_keys('usernamehere')
    
        # Waits until the password box is located, then inputs the password.
        password_input = wait.until(ec.visibility_of_element_located((By.NAME, "session[password]")))
        password_input.send_keys('passwordhere')
    
        # Waits until the login button is located, then clicks the button.
        login_button = wait.until(ec.visibility_of_element_located((By.XPATH, "//div[@data-testid='LoginForm_Login_Button']")))
        login_button.click()
        
    # If the URL redirects you to 'flow' version of the login page (Twitter occasionally redirects you to a different avoid bots like this one, by checking the string URL we can bypass this restriction).
    elif stringurl == "https://twitter.com/i/flow/login":
        
        # Waits until the username box is located, then inputs the username.
        username_input = wait.until(ec.visibility_of_element_located((By.NAME, "username")))
        username_input.send_keys('usernamehere')
        
        # Waits until the username next button is located, then clicks the button.
        username_next_button = wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div')))
        username_next_button.click()
        
        # Waits until the password box is located, then inputs the username.
        password_input = wait.until(ec.visibility_of_element_located((By.NAME, "password")))
        password_input.send_keys('passwordhere')
        
        # Waits until the password next button is located, then clicks the button.
        password_next_button = wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div')))
        password_next_button.click()

# Tweets the data that was scraped. The data must be split into 3 separate tweets to meet the 280 character limit for any Twitter post.
def tweet():
    
    # Wait until the textbox is clickable.
    text_box = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/header/div/div/div/div[1]/div[3]/a')))
    
    # Loops 3 times, one loop for each part of the split-up text.
    for i in range(0, 3):
        time.sleep(2)
        
        # Clicks the textbox to be able to begin typing.
        text_box.click()
        
        # Checks if this is the first loop. If yes, inputs the data stored in 'a' into the textbox.
        if i == 0:
            ActionChains(driver).move_to_element(text_box).send_keys(a).perform()
            time.sleep(2)
            
        # Checks if this is the second loop. If yes, inputs the data stored in 'b' into the textbox.
        elif i == 1:
            ActionChains(driver).move_to_element(text_box).send_keys(date).send_keys(" cont.").send_keys(b).perform()
            time.sleep(2)
            
        # Checks if this is the third loop. If yes, inputs the data stored in 'c' into the textbox.
        elif i == 2:
            ActionChains(driver).move_to_element(text_box).send_keys(date).send_keys(" cont.").send_keys(c).perform()
            time.sleep(2)
            
        # Finds the tweet button to post the tweet.
        tweet = driver.find_element_by_xpath('//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[3]/div/div/div/div[1]/div/div/div/div/div[2]/div[3]/div/div/div[2]/div[4]/div/span/span')
        time.sleep(2)
        
        # Clicks the tweet button.
        tweet.click()

# Calls the login and tweet functions.
def autobot():
    login()
    tweet()

# Calls the autobot function.
autobot()

# Quits the driver.
driver.quit()