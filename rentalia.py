from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import csv


options = webdriver.ChromeOptions()
#options.add_argument('--headless')
#options.add_argument('--no-sandbox')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
# options.add_argument("user-data-dir=selenium")
options.add_argument("--remote-debugging-port=9222")
options.add_argument('--disable-dev-shm-usage')

url = "https://es.rentalia.com/" 
driver = webdriver.Chrome(executable_path = r"C:\Users\marcl\chromedriver_106\chromedriver.exe", options = options)  

driver.implicitly_wait(30)
driver.get(url) 

cookies = driver.find_element('xpath', '//*[@id="didomi-host"]/div/div/div/div//div[2]/button[2]')
cookies.click()

locations = ["Costa Brava", "Alicante", "Barcelona", "Madrid", "Castelldefels", "Gavà"]  

for loc in locations:

    
    try:
        input_field = driver.find_element('class', 'locationInput ng-pristine ng-valid ng-scope ng-isolate-scope ng-empty ng-touched')   
    except:    
        input_field = driver.find_element('xpath', '//*[@id="masterContainer"]/div/div[1]/div/form/div/div[1]/span/input')
 
    input_field.send_keys(loc)

    srchbutton = driver.find_element('xpath','//*[@id="masterContainer"]/div/div[1]/div/form/div/div[5]/button')
    srchbutton.click()
    
    print(f"reached page {url}")   

    with open('rentalia.csv','w', encoding = 'utf-8') as f:
        wr = csv.writer(f, dialect = 'excel')
        wr.writerow(['Sr.No.','Title','Location', 'Price', 'Phone Number', 'Link'])
        n = 0
        i = 1
        while(True):
            # now extract the data from the page we reached on that website 
            n = i
            props = driver.find_elements('class name', 'itemList itemRow col ng-scope s12 m6 l4')
            
            for prop in props:  
                
                
                try:    
                    title = prop.find_element('xpath', f'//*[@id="masterContainer"]/div/div[2]/div[1]/div[{i}]/div/div[2]/a/h3').text
                except:  
                    title = "" 
                try:
                    location = prop.find_element('xpath', f'//*[@id="masterContainer"]/div/div[2]/div[1]/div[{i}]/div/div[2]/a/h4').text
                except:
                    location = ""
                try:
                    price = prop.find_element('xpath', f'//*[@id="masterContainer"]/div/div[2]/div[1]/div[{i}]/div/div[1]/div[1]/span/span').text
                except:
                    price = ""
                try:
                    link = prop.find_element('xpath', f'//*[@id="masterContainer"]/div/div[2]/div[1]/div[{i}]/div/div[2]/a').get_attribute('href')
                except:
                    i+=1
                    break
                    
                driver.get(link)
                for i in range(0,6):
                    ActionChains(driver).send_keys(Keys.SPACE).perform()
                try:
                    phone = driver.find_element('xpath', '//*[@id="masterContainer"]/div/div[4]/div[1]/div[6]/div[4]/a').get_attribute('href')
                except:
                    phone = ""
            
            
                wr.writerow([n, title, location, price, phone, link ])  
                
                #backbutton to itemContainerPage
                bckbtn = driver.find_element('xpath', '//*[@id="masterContainer"]/div/div[1]/div[1]/div/a').get_attribute('href')
                driver.get(bckbtn)
                i+=1
                
          
          #  nxtpg_lnk = driver.find_element('css selector', 'button.')
            #nxtpg_lnk.click()
            
    