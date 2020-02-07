# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 20:05:48 2017

@author: Feng
"""

# -*- coding: UTF-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time, os
import json, pickle, random


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 1}
chrome_options.add_experimental_option("prefs", prefs)

#driver = webdriver.Chrome(chrome_options=chrome_options)

chromedriver = '/usr/local/bin/chromedriver'

#os.environ["webdriver.chrome.driver"] = chromedriver

driver = webdriver.Chrome(chromedriver)
driver.get('http://*****/login.jsp')


###year 2016 id
poorid = []
year = 2016
npg = 814

for i in range(718, npg+1):
    nj=13
    driver.switch_to.default_content()
    driver.switch_to.frame("jzfp_jdlk_ifm")
    for j in range(1, nj):
        famid = driver.find_element_by_xpath(
            '//*[@id="tdd"]/tr['+str(j)+"]").get_attribute('tid')
        poorid.append(famid)

    if i < npg + 1:
            driver.find_element_by_link_text("下一页").click()
            #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "rightDiv")))
            time.sleep(4)
        #driver.switch_to.default_content()

driver.find_element_by_xpath('//*[@id="ul-state"]/li[6]').click()
time.sleep(10)

npg = 415
for i in range(406, npg+1):
    nj=13
    driver.switch_to.default_content()
    driver.switch_to.frame("jzfp_jdlk_ifm")
    for j in range(1, nj):
        famid = driver.find_element_by_xpath(
            '//*[@id="tdd"]/tr['+str(j)+"]").get_attribute('tid')
        poorid.append(famid)

    if i < npg + 1:
            driver.find_element_by_link_text("下一页").click()
            #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "rightDiv")))
            time.sleep(4)
        #driver.switch_to.default_content()

with open("D:\\temp\\poor\\poorid-" + str(year) + "p.txt", "wb") as fp:
    pickle.dump(poorid, fp)
poorid2016=poorid

poorid2014 = poorid
poorid2015=poorid


def saveHtml(file_name,file_content):
#    注意windows文件命名的禁用符，比如 /
    with open(file_name,"wb") as f:
#   写文件用bytes而不是str，所以要转码
        f.write( file_content )

#js='window.open("http://www.baidu.com")'
#driver.execute_script(js)
import pandas as pd


with open("C:\\Research\\developEcon\\data\\update201712\\poorid-" + str(2014) + "p.txt", "rb") as fp:
    poorid2014=pickle.load(fp)
with open("C:\\Research\\developEcon\\data\\update201712\\poorid-" + str(2015) + "p.txt", "rb") as fp:
    poorid2015 = pickle.load(fp)
with open("C:\\Research\\developEcon\\data\\update201712\\poorid-" + str(2016) + "p.txt", "rb") as fp:
    poorid2016 = pickle.load(fp)
with open("C:\\Research\\developEcon\\data\\update201712\\poorid-" + str(2017) + "p.txt", "rb") as fp:
    poorid2017=pickle.load(fp)
poorid=poorid2014+poorid2015+poorid2016+poorid2017
poorid=pd.Series(poorid).drop_duplicates().tolist()

nlp=len(poorid)#11080,11106,11123, 11162-11169

for i in range(11165, 11167):#
    for year in range(2016, 2018):
        url = 'http://*********/base/poor-family!input.do?familyId=' + poorid[
            i] + '&op=view&areaCode=532926000000&itemNo=1&dataYear=' + str(year)
        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "poorFamilyForm")))
            time.sleep(1.5)
            pg1=driver.page_source
            saveHtml('D:\\poorhtml3\\'+poorid[i]+'-'+str(year), pg1.encode())
            time.sleep(0.1)
        except:
            print('error:'+str(i)+'--'+str(year))
    if i == int(i/50)*50:
        try:
            driver.find_element_by_xpath('//*[@id="return"]').click()
            time.sleep(1)
            driver.refresh()
            time.sleep(4)
        except:
            driver.refresh()
            time.sleep(3)


# check existence
for i in range(10000,nlp):#
    for year in range(2014,2018):
        file = 'D:\\poorhtml3\\'+ poorid[i] +'-'+str(year)
        if os.path.exists(file):
            j=0
        else:
            print(str(i)+'--'+str(year))



for i in range(14462, nlp):#
    for year in range(2015, 2016):
        url = 'http://*******/base/poor-family!input.do?familyId=' + poorid[
            i] + '&op=view&areaCode=532926000000&itemNo=1&dataYear=' + str(year)
        driver.get(url)
        time.sleep(4)
        pg1=driver.page_source
        saveHtml('D:\\poorhtml4\\'+poorid[i]+'-'+str(year), pg1.encode())
        time.sleep(0.1)


