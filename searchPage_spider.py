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
    
    def possionWait(self):#{
        #self.driver.implicitly_wait(np.random.poisson(5.2))
        time.sleep(np.random.poisson(1+1))
    #}
    
    def indicatePageLoaded(self):#{
        try:#{
            WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID,'list-itemList')))
        #}
        finally:#{
            print "page load finish"
        #}
    
    def scrollToEnd(self):#{
        self.possionWait()
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #}
    
    def getHref(self):#{
        #itemList = self.driver.find_element_by_id( 'list-itemList')
        
        itemList = self.driver.find_element_by_xpath("""//*[@id="list-itemList"]""")
        J_AtpLogs = itemList.find_elements_by_class_name('J_AtpLog')
        i=0
        for J_AtpLog in J_AtpLogs:#{
            if (i%2 is 0):#{
                with open("/Users/johnmanli/Documents/selenium_chromeDriver/itemUrl/itemUrl.txt", "a") as itemUrl: #{
                    itemUrl.write(J_AtpLog.get_attribute("href"))
                    itemUrl.write('\n')
                    #}
            #}
            i+=1
        #}
        with open("/Users/johnmanli/Documents/selenium_chromeDriver/itemUrl/scrapLog.csv", "a") as scrapLog: #{
            scrapLog.write(str(self.getCurrPage()[0]))
            scrapLog.write(',')
            scrapLog.write(str(i/2))
            scrapLog.write('\n')
        #}
        print "number of item links: ", i/2
    #}    
    
    def goToNextPage(self):#{
        time.sleep(1)
        nextPage = self.driver.find_element_by_xpath("""//*[@id="list-filterForm"]/div[2]/div/div[5]/div[1]/div/span[3]""")
        itemList = self.driver.find_element_by_xpath("""//*[@id="list-itemList"]""")
        J_AtpLog = itemList.find_element_by_class_name('J_AtpLog')
        actions = ActionChains(self.driver)
        actions.move_to_element(nextPage)
        actions.click(nextPage)
        actions.perform()
        try:
            WebDriverWait(self.driver, 10).until(EC.staleness_of(J_AtpLog))
        except TimeoutException:
            print "Timeout, exit in 1"
            exit(1)
        #self.possionWait()
    #}
    
    def isAtLastPage(self):#{
        currPageNo = self.driver.find_element_by_xpath("""//*[@id="list-filterForm"]/div[2]/div/div[5]/div[1]/div/span[2]/strong""").text
        finalPageNo = self.driver.find_element_by_xpath("""//*[@id="list-filterForm"]/div[2]/div/div[5]/div[1]/div/span[2]""").text
        finalPageNo_list = [int(s) for s in re.findall('\\d+', finalPageNo)]
        currPageNo_list = [int(s) for s in re.findall('\\d+', currPageNo)]
        #print "Last Page? ", finalPageNo_list[-1], "Vs" , currPageNo_list[0], (finalPageNo_list[-1] == currPageNo_list[0])
        return finalPageNo_list[-1] == currPageNo_list[0]
    
    def getCurrPage(self):#{
        currPageNo = self.driver.find_element_by_xpath("""//*[@id="list-filterForm"]/div[2]/div/div[5]/div[1]/div/span[2]/strong""").text
        currPageNo_list = [int(s) for s in re.findall('\\d+', currPageNo)]
        return currPageNo_list
    #}
    def getFinalPage(self):#{
        finalPageNo = self.driver.find_element_by_xpath("""//*[@id="list-filterForm"]/div[2]/div/div[5]/div[1]/div/span[2]""").text
        finalPageNo_list = [int(s) for s in re.findall('\\d+', finalPageNo)]
        return finalPageNo_list
    #}

def main():#{
    #initial selenium webdriver
    chrome_path = "/Users/johnmanli/Documents/selenium_chromeDriver/chromedriver"

    profile = webdriver.FirefoxProfile()
    profile.accept_untrusted_certs = True
    
    
    pageSpider = mySearchPageSpider(chrome_path)
    
    url = "https://world.taobao.com/search/search.htm?cat=56156324&_ksTS=1487421488377_28&json=on&suggest_query=%E9%BA%BB%E5%B0%87&cna=mxYvEQfnxksCAdq94T4nD10c&wq=%E9%BA%BB%E5%B0%87&suggest=0_2&_input_charset=utf-8&source=suggest&s=0&navigator=all&q=%E9%BA%BB%E5%B0%86%E7%89%8C&callback=__jsonp_cb&abtest=_AB-LR517-LR854-LR895-PR517-PR854-PR895"
    #page 1/100
    #url = "https://world.taobao.com/search/search.htm?cat=56156324&_ksTS=1487496354756_367&json=on&suggest_query=%E9%BA%BB%E5%B0%87&cna=vwwwEY6wfhMCAdq94RQ3c38v&module=page&wq=%E9%BA%BB%E5%B0%87&suggest=0_2&_input_charset=utf-8&navigator=all&s=5820&source=suggest&q=%E9%BA%BB%E5%B0%86%E7%89%8C&callback=__jsonp_cb&abtest=_AB-LR517-LR854-LR895-PR517-PR854-PR895"
    #page 98/100
    pageSpider.browsePage(url)
    pageSpider.indicatePageLoaded()
    print "[first Page, last Page]: ", pageSpider.getFinalPage();
    try:#{
        #while True:#{
        for i in xrange(pageSpider.getFinalPage()[1]):
        #for i in xrange(5):
        #if True:
            print "scraping page ", pageSpider.getCurrPage()
            pageSpider.indicatePageLoaded()
            pageSpider.scrollToEnd()
            pageSpider.getHref()
            pageSpider.goToNextPage()
            if pageSpider.isAtLastPage():#{
                #break
                print "this is last page"
            #}
            
        #}
    #}
    finally:#{
        print "bye"
        pageSpider.closeBroser()
    #}
#}



#driver.get("http://tw.yahoo.com/")





if __name__ == "__main__":
    main()
    
    