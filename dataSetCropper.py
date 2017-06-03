# -*- coding: utf-8 -*-
"""
img cropper

"""

import lxml
import os
import numpy as np
from scipy.misc import imread, imsave


    
    

      
def getXmlPaths(sourceDir):#{
    
    xmls = []
    for xml in os.listdir(sourceDir): #{
        if xml.endswith(".xml"): #{
            xmls.append(xml)
            #print(xml[:-4])
        #}
    #}
    return xmls
        
#}
        
        
def getBndBoxInfo(xmlPath):#{
   tree = lxml.etree.parse(xmlPath)
   root = tree.getroot()
   
   bndboxInfo =[ [ "mjClass", "xmin", "ymin", "xmax", "ymax" ] ]
   
   for  obj in root.findall('object'):#{
       mjClass = obj.find('name').text
       #print mjClass, idx
       bndbox = obj.find('bndbox')
       xmin = int(bndbox.find('xmin').text)
       xmax = int(bndbox.find('xmax').text)
       ymin = int(bndbox.find('ymin').text)
       ymax = int(bndbox.find('ymax').text)
       
       bndboxInfo.append([ mjClass, xmin, ymin, xmax, ymax ])
   #}
   return bndboxInfo
   
#}

def main():#{
   sourceDir = "/Users/johnmanli/Documents/dataSetCropping/"
   desDir = "/Users/johnmanli/Documents/datasetResultDir/"
   
   xmls = getXmlPaths(sourceDir)
   for xml in xmls:#{
      print xml
      bndBoxInfo = getBndBoxInfo(os.path.join(sourceDir,xml))
   
      imgFile = xml[:-4]
      img = imread(os.path.join(sourceDir,xml[:-4]))
   
   
      for idx, info in enumerate(bndBoxInfo):#{
         if idx == 0 :#{
            continue 
         #}
         imgCroped = img[info[2]:info[4],info[1]:info[3],:]
         #file naming format: orgImgFileName_mahjongClass_idx.orgImgFileExtension
         #file naming format example : taobao_img962_cheracter1_1.jpg
         savePath = os.path.join(desDir,info[0], imgFile[:imgFile.rfind('.')]+"_"+info[0]+"_"+str(idx)+imgFile[imgFile.rfind('.'):])
         imsave(savePath, imgCroped)
       
         print idx, info
      #}
       
       
   #}
#}


if __name__ == "__main__": #{
    main()
#}
    