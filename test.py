from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime

class Hosttest(TestCase):
    
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.live_server_url = 'http://127.0.0.1:8000/'

    def tearDown(self):
        self.driver.quit()

    

    def test_01_login_page(self):
        driver = self.driver
        driver.get(self.live_server_url)
        driver.maximize_window()
        login=driver.find_element(By.CSS_SELECTOR,"a[href='/login_view/'].nav-item.nav-link")
        login.click()
        time.sleep(2)
        login=driver.find_element(By.CSS_SELECTOR,"input#username")
        login.send_keys('teenamaryalex21@gmail.com')
        time.sleep(2)
        login=driver.find_element(By.CSS_SELECTOR,"input#pass")
        login.send_keys('MT23rt@a')
        time.sleep(2)
        login=driver.find_element(By.CSS_SELECTOR,"input#logsub")
        login.click()
        time.sleep(2)
        design = driver.find_element(By.CSS_SELECTOR, 'a.banner-button[href="/design/"] ')
        design.click()
        time.sleep(2)
        design = driver.find_element(By.CSS_SELECTOR, 'button.dress-type-btn[data-dress-type="Gowns"]')
        design.click()
        time.sleep(2)
        options = driver.find_element(By.CSS_SELECTOR, 'div.options[data-toggle="collapse"][href="#fabricPatternOptions"]')
        options.click()
        design = driver.find_element(By.CSS_SELECTOR, 'img[src="/media/media/fabrics/Theory_Dusted_Perfect_Plum_Stretch_Silk_Chiffon_iDogsAn.jpeg"][alt="Perfect Plum Stretch Silk Chiffon"]')
        design.click()
        time.sleep(2)
        options = driver.find_element(By.CSS_SELECTOR, 'div.options[data-toggle="collapse"][href="#neckPatternOptions"]')
        options.click()
        design = driver.find_element(By.CSS_SELECTOR, 'img[src="/media/neck_patterns/Sweet_heart_neckline_f2EsL1D.jpeg"][alt="sweet heart -gown"]')
        design.click()
        time.sleep(2)
        options = driver.find_element(By.CSS_SELECTOR, 'div.options[data-toggle="collapse"][href="#topPatternOptions"]')
        options.click()
        design = driver.find_element(By.CSS_SELECTOR, 'img[src="/media/top_patterns/Sheath_Dress_63SRNOm.jpeg"][alt="top sheath"]')
        design.click()
        time.sleep(2)
        options = driver.find_element(By.CSS_SELECTOR, 'div.options[data-toggle="collapse"][href="#sleevesPatternOptions"]')
        options.click()
        design = driver.find_element(By.CSS_SELECTOR, 'img[src="/media/sleeves_patterns/Quarter_Sleeve_QU3r0Ar.jpeg"][alt="Quarter Sleeve"]')
        design.click()
        time.sleep(2)
        options = driver.find_element(By.CSS_SELECTOR, 'div.options[data-toggle="collapse"][href="#bottomPatternOptions"]')
        options.click()
        design = driver.find_element(By.CSS_SELECTOR, 'img[src="/media/bottom_patterns/mermaid_gown_OUb3lYb.jpeg"][alt="Mermaid- gown"]')
        design.click()
        time.sleep(2)
        design = driver.find_element(By.CSS_SELECTOR, 'button#next-button.btn.btn-primary.mb-5')
        design.click()
        time.sleep(2)
        design = driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-primary.mt-4')
        design.click()
        time.sleep(2)
        login=driver.find_element(By.CSS_SELECTOR,'input#shoulder.form-control[type="number"][step="0.1"][required]')
        login.send_keys('16')
        time.sleep(2)
        login=driver.find_element(By.CSS_SELECTOR,'input#waist.form-control[type="number"][step="0.1"][required]')
        login.send_keys('16')
        time.sleep(2)
        login=driver.find_element(By.CSS_SELECTOR,'input#chest.form-control[type="number"][step="0.1"][required]')
        login.send_keys('16')
        time.sleep(2)
        login=driver.find_element(By.CSS_SELECTOR,'input#hip.form-control[type="number"][step="0.1"][required]')
        login.send_keys('16')
        time.sleep(2)
        login=driver.find_element(By.CSS_SELECTOR,'input#Inseam.form-control[type="number"][step="0.1"][required]')
        login.send_keys('16')
        time.sleep(2)
        design = driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-primary[type="submit"]')
        design.click()
        time.sleep(2)
        
        

        

        
        
        
        
       
       