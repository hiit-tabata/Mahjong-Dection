# -*- coding: utf-8 -*-
"""
This is a spider to scrape item urls from taubao
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import re
import time


from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException

class mySearchPageSpider:#{
    def __init__(self, chrome_path):#{
      self.chrome_path = chrome_path
      self.driver = webdriver.Chrome(chrome_path)
      
    #}
    def setDriver(self, driver):#{
        self.driver = driver
    #}
    def browsePage(self, url):#{
        self.driver.get(url)
    #}
    
    def closeBroser(self):#{
        self.driver.quit()
    #}
    
    def possionWait(self, i):#{
        #self.driver.implicitly_wait(1+np.random.poisson(1))
        time.sleep(i+np.random.poisson(1))
    #}
    
    def indicatePageLoaded(self, url):#{
        try:#{
            WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,"""  //*[@id="J_DivItemDesc"]""")))
            return True
        #}
        except TimeoutException:#{
            with open("/Users/johnmanli/Documents/selenium_chromeDriver/imgUrl/tiomeOutErrLog.csv", "a") as errLog: #{
                errLog.write("Load Page")
                errLog.write(',')
                errLog.write(url)
                errLog.write('\n')
                return False
        #}
        finally:#{
            print "page load finish"
        #}
    
    def scrollToEnd(self, url):#{
        
        self.driver.execute_script("setInterval(function(){ window.scrollBy(0, 50);}, 100);")
        while True:#{
            #print "going to bottom"
            if(self.driver.execute_script("if((window.innerHeight + window.scrollY) >= document.body.offsetHeight){return 1;}")):#{
                break
            #}
        #}
        try:#{
            ps = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH,"""//*[@id="J_DivItemDesc"]/p""")))
            print "p len: ", len(ps)
        #}
        except TimeoutException:#{
            with open("/Users/johnmanli/Documents/selenium_chromeDriver/imgUrl/tiomeOutErrLog.csv", "a") as errLog: #{
                errLog.write("p tag")
                errLog.write(',')
                errLog.write(url)
                errLog.write('\n')
                return False
        #}
        finally:#{
            pass
        #}
        try:#{
            for p in ps:#{
                imgs = p.find_elements(By.TAG_NAME,'img')
                print "img len: ", len(imgs)
                
                #write the img url
                for img in imgs:#{
                    #print img.get_attribute("src")
                    extractedURL = img.get_attribute("src")
                    if  isinstance(extractedURL, basestring):
                        with open("/Users/johnmanli/Documents/selenium_chromeDriver/imgUrl/imgUrl.txt", "a") as imgUrl: #{
                                imgUrl.write(extractedURL)
                                imgUrl.write('\n')
                    #}
                #}
            #}
        finally:#{
            print "img load finish"
        #}
    #}
    
      
    

def getImgUrl(pageSpider, url):#{
    

    #url = "https://world.taobao.com/item/542843153345.htm#detail"
    #item url
    pageSpider.browsePage(url)
    if pageSpider.indicatePageLoaded(url):
        pageSpider.scrollToEnd(url)
    # now it become scrollToEnd and save (no eyes see)
    
    
#}

def main():#{
    #initial selenium webdriver
    chrome_path = "/Users/johnmanli/Documents/selenium_chromeDriver/chromedriver"
    
    pageSpider = mySearchPageSpider(chrome_path)
    try:#{
        with open('/Users/johnmanli/Documents/selenium_chromeDriver/itemUrl/itemUrl.txt', 'r') as f:#{
            for line in f:#{
                print line
                getImgUrl(pageSpider, line)
            #}
        #}
    #}
    finally:#{
        print "bye"
        pageSpider.closeBroser()
    #}
#}
    #url = "https://world.taobao.com/item/542843153345.htm#detail"
    #getImgUrl(url)
    
#driver.get("http://tw.yahoo.com/")


#//*[@id="J_DivItemDesc"]/p[2]/img[1]
#//*[@id="J_DivItemDesc"]/p[2]/img[2]
#//*[@id="J_DivItemDesc"]/p[1]/img[1]


if __name__ == "__main__":
    main()
    
    