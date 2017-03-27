#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 11:19:27 2017

img get

@author: johnmanli
"""

#/Users/johnmanli/Documents/selenium_chromeDriver/imgUrl/imgUrl.txt 

import urllib2
def main():#{
    with open("/Users/johnmanli/Documents/selenium_chromeDriver/imgUrl/imgUrl.txt", "r") as imgSrc:#{
    #with open("/Users/johnmanli/Documents/selenium_chromeDriver/testFile.txt", "r") as imgSrc:#{
        for idx, line in enumerate(imgSrc):#{
                if idx < 5011:#{ #yep I am lazy, start in here as prevously got unknown exception
                    continue
                #}
                if line.rfind('\n')!= -1:#{
                    line = line[:line.rfind('\n')]
                #}
                print "downloading img: [", idx, "/46500]\n   url: ", line
                fileExtension = line[line.rfind('.'):]
                
                try:#{
                    imgResponse = urllib2.urlopen(line)
                #}
                except urllib2.HTTPError as e:#{
                    with open("/Users/johnmanli/Documents/selenium_chromeDriver/errorImgUrl/error.csv", "a") as errorLog:#{
                        errorLog.write(line)
                        errorLog.write(',')
                        errorLog.write(str(e.code))
                        errorLog.write('\n')
                    #}
                #}
                except urllib2.URLError as e:#{
                    with open("/Users/johnmanli/Documents/selenium_chromeDriver/errorImgUrl/error.csv", "a") as errorLog:#{
                        errorLog.write(line)
                        errorLog.write(',')
                        errorLog.write(str(e.reason))
                        errorLog.write('\n')
                    #}
                #}
                except:#{
                    with open("/Users/johnmanli/Documents/selenium_chromeDriver/errorImgUrl/error.csv", "a") as errorLog:#{
                        errorLog.write(line)
                        errorLog.write(',')
                        errorLog.write("unknown exception")
                        errorLog.write('\n')
                    #}
                    pass
                #}
                else:#{
                    print "saving Imgs"
                    img = imgResponse.read()
                    with open ("/Users/johnmanli/Documents/selenium_chromeDriver/img/img"+str(idx)+fileExtension,'w') as outputImg:#{
                        outputImg.write(img)
                        outputImg.close()
                    #}
                #}
        #}
    #}

#} 



if __name__ == "__main__":
    main()
    