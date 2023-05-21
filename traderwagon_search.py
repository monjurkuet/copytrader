import seleniumwire.undetected_chromedriver as uc
import time,random
# xpath
POSTFOLIO_LIST='//div[text()="Portfolio List"]'
NEXTBUTTON='//button[@aria-label="Next page"]'




def jsclick(xpth):
    try: 
        element=driver.find_element('xpath',xpth)
        driver.execute_script("arguments[0].click();", element)
    except:
        pass  

def newBrowser():
    driver=uc.Chrome(user_data_dir="G:\\copytraderscrapingprofile2",
                     browser_executable_path='C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe',
                     headless=False,seleniumwire_options={
        'proxy': {
            'http': "http://45.85.147.136:24003",
            'https': "http://45.85.147.136:24003"
                }
            })
    return driver

driver=newBrowser()

driver.get('https://www.traderwagon.com/en')
jsclick(POSTFOLIO_LIST)

jsclick(NEXTBUTTON)