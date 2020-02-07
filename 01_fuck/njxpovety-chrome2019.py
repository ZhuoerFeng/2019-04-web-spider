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

chromedriver = "/usr/local/bin/chromedriver"

#os.environ["webdriver.chrome.driver"] = chromedriver

driver = webdriver.Chrome(chromedriver)

driver.get('http://cpadis.cpad.gov.cn:7080/portal/')
# driver.get('http://cpadisc2.cpad.gov.cn/cpad/main')
driver.add_cookie({
    "name": "JSESSIONID",
    "value": "uOfsqCrnDbAhF5IGhEhCHxMWNLJJhKMnRvqhhvSCKmypa7jB57Hj!2055736785",
    "domain": "cpadis.cpad.gov.cn",
    "path": "/portal"
})
driver.add_cookie({
    "name": "JSESSIONID",
    "value": "P4js73OLfcV-GGtuG5SNTY6mdRvAwJOs0GM2mfZgSmGfQ31LX3Q2!1214480065",
    "domain": "cpadis.cpad.gov.cn",
    "path": "/"
})
driver.add_cookie({
    "name": "outpath",
    "value": "http%3A%2F%2Fcpadis.cpad.gov.cn%3A8090%2Fbi%2F%7Chttp%3A%2F%2Fcpadisc2.cpad.gov.cn%2Fcpad%2F%7C",
    "domain": "cpadis.cpad.gov.cn",
    "path": "/portal"
})
driver.add_cookie({
    "name": "outpath",
    "value": "http%3A%2F%2Fcpadisc2.cpad.gov.cn%2Fcpad%2F%7C",
    "domain": "cpadis.cpad.gov.cn",
    "path": "/portal/techcomp/idm"
})
driver.add_cookie({
    "name": "vs",
    "value": "76519347",
    "domain": "cpadis.cpad.gov.cn",
    "path": "/"
})

driver.get('http://cpadis.cpad.gov.cn:7080/portal/')

time.sleep(1)
driver.find_element_by_class_name('menuIcon1').click()

time.sleep(2)
driver.find_element_by_link_text('域名访问：http://cpadisc2.cpad.gov.cn/cpad/loginUP').click()

time.sleep(3)
driver.find_element_by_css_selector('a[title=查询]').click()
time.sleep(1)
driver.find_element_by_css_selector('a[title=查询].ui-menuitem-link').click()
time.sleep(1)
driver.find_element_by_css_selector('a[title=基础信息查询]').click()
time.sleep(1)
driver.find_element_by_css_selector('a[title=贫困户信息查询]').click()
time.sleep(1)
driver.find_element_by_css_selector('.fa.fa-fw.fa-caret-down.ui-clickable').click()

time.sleep(2)
from selenium.webdriver.support.select import Select
import re
import os
import math
import json

os.system('rm -rf poor_data')
os.mkdir('poor_data')
os.chdir('poor_data')

driver.find_element_by_css_selector('#on_query').click()
time.sleep(3)
Select(driver.find_element_by_css_selector('select.ui-paginator-rpp-options.ui-widget.ui-state-default')).select_by_visible_text('100')
time.sleep(3)
driver.find_element_by_css_selector('.fa.fa-forward').click()
time.sleep(3)
driver.find_element_by_css_selector('.fa.fa-backward').click()
time.sleep(3)
for y in range(2014, 2018 + 1):
    year_text = '%s年底' % y
    if y == 2018:
        year_text = '2018年度'

    # TODO select the year

    total = int(re.search('\d+', driver.find_element_by_css_selector('span.fl.ft125').text).group())
    print('year = %s total = %s' % (y, total))

    per_page = 100
    page_count = int(math.ceil(total / per_page))

    dir_name = str(y)
    os.mkdir(dir_name)
    os.chdir(dir_name)

    os.mkdir('table')
    os.mkdir('records')
    family_data = []
    for i in range(0, page_count):
        s_id = i * 100 + 1
        e_id = i * 100 + 100
        table_html = driver.find_element_by_css_selector('p-datatable[datakey=aac001]').get_attribute('innerHTML')
        with open('table/p%s.html' % (i + 1), 'w') as f:
            f.write(table_html)
    
        print('page = %s (from %s to %s)' % (i + 1, s_id, e_id))

        names = re.findall('<span class="ui-cell-data">\s*<p-columnbodytemplateloader></p-columnbodytemplateloader>\s*<span><a>(\S+)</a></span>\s*</span>', table_html)

        for j in range(s_id, e_id + 1):
            driver.find_element_by_link_text(names[(j - s_id) * 2]).click()
            time.sleep(1)
            #for fk in ['一、基本情况', '二、生产生活条件', '三、上年度收入、患病信息', '四、易地搬迁信息', '五、帮扶责任人结对信息', '六、帮扶措施', '七、两不愁、三保障', '八、脱贫措施']:
            #    driver.find_element_by_link_text(fk).click()
            #    time.sleep(0.1)
            record_html = driver.find_element_by_css_selector('p-dialog.ng-tns-c2-4').get_attribute('innerHTML')
            keys = re.findall('<input.*id="(\w+)".*>', record_html)
            data = {}
            for key in keys:
                fk = driver.find_element_by_id(key)
                v = fk.get_attribute('value')
                if not v:
                    v = fk.get_attribute('outerText')
                data[key] = v
            with open('records/%s.json' % j, 'w') as f:
                f.write(json.dumps(data))
            with open('records/%s.html' % j, 'w') as f:
                f.write(record_html)
            
            #with open('records/%s.txt' % j, 'w') as f:
            #    f.write(driver.find_element_by_css_selector('p-dialog.ng-tns-c2-4').get_attribute('outerText'))
            driver.find_element_by_css_selector('.ng-tns-c2-4.ui-dialog-titlebar-icon.ui-dialog-titlebar-close.ui-corner-all').click()
            time.sleep(0.5)
        driver.find_element_by_css_selector('.fa.fa-forward').click()
        time.sleep(3)
    os.chdir('..')

time.sleep(10)
driver.close()

"""
###year 2016 所有
poor = []
year = 2016
infom=[]

npg=814

for i in range(1, npg+1):
    nj=13
    driver.switch_to.default_content()
    driver.switch_to.frame("jzfp_jdlk_ifm")
    for j in range(1, nj):
        fname = driver.find_element_by_xpath(
            "/html/body/div/div[4]/div[2]/div[2]/div/table/tbody[2]/tr["+str(j)+"]/td[2]").text
        poorprop = driver.find_element_by_xpath(
            "/html/body/div/div[4]/div[2]/div[2]/div/table/tbody[2]/tr["+str(j)+"]/td[3]").text
        reason = driver.find_element_by_xpath(
            "/html/body/div/div[4]/div[2]/div[2]/div/table/tbody[2]/tr[" + str(j) + "]/td[4]").text

        location = driver.find_element_by_xpath(
            "/html/body/div/div[4]/div[2]/div[2]/div/table/tbody[2]/tr[" + str(j) + "]/td[6]").text
        havehelp = driver.find_element_by_xpath(
            "/html/body/div/div[4]/div[2]/div[2]/div/table/tbody[2]/tr[" + str(j) + "]/td[7]").text
        yearesc = year

        xpath="/html/body/div/div[4]/div[2]/div[2]/div/table/tbody[2]/tr["+str(j)+"]/td[2]"
        alldata1 = driver.find_element_by_xpath(xpath)
        alldata1.click()
        #time.sleep(random.randint(8, 9))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "chengYXX")))
        time.sleep(2)

        famid = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[1]/div[3]/table/tbody/tr[2]/td[2]').text
        poorcond = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[1]/div[3]/table/tbody/tr[5]/td[2]').text
        pooragn = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[1]/div[3]/table/tbody/tr[6]/td[2]').text
        issingechild = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[1]/div[3]/table/tbody/tr[9]/td[4]').text
        istwogirl = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[1]/div[3]/table/tbody/tr[10]/td[2]').text
        planedyear = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[1]/div[3]/table/tbody/tr[14]/td[2]').text
        #reason1 = driver.find_element_by_xpath('//*[@id="aae960"]/div').text
        reason2 = driver.find_element_by_xpath('//*[@id="aad108"]/div[1]').text
        famnum = len(driver.find_element_by_id('chengYXX').find_elements_by_tag_name('tr'))-1

        infomember0 = []
        for k in range(0,famnum):
            fid=driver.find_element_by_xpath('//*[@id="chengYXX"]/tbody[2]/tr['+str(1+k)+']').get_attribute('id')
            iname=driver.find_element_by_xpath('//*[@id="chengYXX"]/tbody[2]/tr['+str(1+k)+']/td[2]').text
            igend = driver.find_element_by_xpath('//*[@id="chengYXX"]/tbody[2]/tr[' + str(1 + k) + ']/td[3]').text
            iage = driver.find_element_by_xpath('//*[@id="chengYXX"]/tbody[2]/tr[' + str(1 + k) + ']/td[6]').text
            irelt = driver.find_element_by_xpath('//*[@id="chengYXX"]/tbody[2]/tr[' + str(1 + k) + ']/td[7]').text
            ination = driver.find_element_by_xpath('//*[@id="chengYXX"]/tbody[2]/tr[' + str(1 + k) + ']/td[8]').text
            iedu = driver.find_element_by_xpath('//*[@id="chengYXX"]/tbody[2]/tr[' + str(1 + k) + ']/td[9]').text
            ischool = driver.find_element_by_xpath('//*[@id="chengYXX"]/tbody[2]/tr[' + str(1 + k) + ']/td[10]').text
            ihealth = driver.find_element_by_xpath('//*[@id="chengYXX"]/tbody[2]/tr[' + str(1 + k) + ']/td[11]').text
            ilab = driver.find_element_by_xpath('//*[@id="chengYXX"]/tbody[2]/tr[' + str(1 + k) + ']/td[12]').text
            iwork = driver.find_element_by_xpath('//*[@id="chengYXX"]/tbody[2]/tr[' + str(1 + k) + ']/td[13]').text
            iworkm = driver.find_element_by_xpath('//*[@id="chengYXX"]/tbody[2]/tr[' + str(1 + k) + ']/td[14]').text
            icorpins = driver.find_element_by_xpath('//*[@id="chengYXX"]/tbody[2]/tr[' + str(1 + k) + ']/td[15]').text
            ipens = driver.find_element_by_xpath('//*[@id="chengYXX"]/tbody[2]/tr[' + str(1 + k) + ']/td[16]').text
            ipolt = driver.find_element_by_xpath('//*[@id="chengYXX"]/tbody[2]/tr[' + str(1 + k) + ']/td[17]').text
            imedins = driver.find_element_by_xpath('//*[@id="chengYXX"]/tbody[2]/tr[' + str(1 + k) + ']/td[20]').text
            ihelp = driver.find_element_by_xpath('//*[@id="chengYXX"]/tbody[2]/tr[' + str(1 + k) + ']/td[22]').text
            infomember0.append([fid,iname,igend,iage,irelt,ination,iedu,ischool,ihealth,ilab,iwork,iworkm,
                                icorpins,ipens,ipolt,imedins,ihelp])

        driver.find_element_by_xpath('//*[@id="poorFamilyForm"]/div/div[3]/ul[1]/li[2]').click()
        time.sleep(1)

        land = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[5]/div/table/tbody/tr[1]/td[2]').text
        landwater = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[5]/div/table/tbody/tr[2]/td[2]').text
        forest = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[5]/div/table/tbody/tr[3]/td[2]').text
        forestgrain = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[5]/div/table/tbody/tr[4]/td[2]').text
        forestecon = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[5]/div/table/tbody/tr[5]/td[2]').text
        grass = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[5]/div/table/tbody/tr[6]/td[2]').text
        water = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[5]/div/table/tbody/tr[7]/td[2]').text
        drinking = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[5]/div/table/tbody/tr[8]/td[2]').text
        safedrink = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[5]/div/table/tbody/tr[9]/td[2]').text
        electric = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[5]/div/table/tbody/tr[10]/td[2]').text
        TVradio = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[5]/div/table/tbody/tr[11]/td[2]').text
        distance = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[5]/div/table/tbody/tr[12]/td[2]').text
        road = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[5]/div/table/tbody/tr[13]/td[2]').text
        roomspace = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[5]/div/table/tbody/tr[14]/td[2]').text
        dangroom = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[5]/div/table/tbody/tr[15]/td[2]').text
        WC = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[5]/div/table/tbody/tr[16]/td[2]').text
        energy = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[5]/div/table/tbody/tr[17]/td[2]').text
        coop = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[5]/div/table/tbody/tr[18]/td[2]').text
        loaneduill = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[5]/div/table/tbody/tr[19]/td[2]').text
        electricprod = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[5]/div/table/tbody/tr[20]/td[2]').text
        pension = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[5]/div/table/tbody/tr[21]/td[2]').text
        loannotpay = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[5]/div/table/tbody/tr[1]/td[4]').text
        netinc = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[5]/div/table/tbody/tr[2]/td[4]').text
        avgnetinc = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[5]/div/table/tbody/tr[3]/td[4]').text
        inc = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[5]/div/table/tbody/tr[4]/td[4]').text
        wages = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[5]/div/table/tbody/tr[5]/td[4]').text
        incprod = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[5]/div/table/tbody/tr[6]/td[4]').text
        subsidy = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[5]/div/table/tbody/tr[7]/td[4]').text
        subbirth = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[5]/div/table/tbody/tr[8]/td[4]').text
        subpoor = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[5]/div/table/tbody/tr[9]/td[4]').text
        subfive = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[5]/div/table/tbody/tr[10]/td[4]').text
        subagri = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[5]/div/table/tbody/tr[11]/td[4]').text
        subgrain = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[5]/div/table/tbody/tr[12]/td[4]').text
        insuaged = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[5]/div/table/tbody/tr[13]/td[4]').text
        insumed = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[5]/div/table/tbody/tr[14]/td[4]').text
        medsalv = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[5]/div/table/tbody/tr[15]/td[4]').text
        subenvi = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[5]/div/table/tbody/tr[16]/td[4]').text
        incasset = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[5]/div/table/tbody/tr[17]/td[4]').text
        expend = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[5]/div/table/tbody/tr[18]/td[4]').text
        consumpc = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[5]/div/table/tbody/tr[19]/td[4]').text
        otherinc = driver.find_element_by_xpath(
            '//*[@id="poorFamilyForm"]/div/div[5]/div/table/tbody/tr[20]/td[4]').text

        poor.append(
            [fname, poorprop, reason, reason2, famnum , location , havehelp ,
             yearesc,famid,poorcond,pooragn,issingechild ,
        istwogirl , planedyear ,land, landwater, forest , forestgrain , forestecon , grass ,
        water , drinking , safedrink , electric ,TVradio , distance ,road , roomspace ,
        dangroom , WC , energy , coop , loaneduill , electricprod , pension ,
        loannotpay , netinc , avgnetinc , inc , wages , incprod , subsidy , subbirth ,
        subpoor,subfive ,  subagri , subgrain , insuaged , insumed , medsalv ,
        subenvi , incasset , expend , consumpc, otherinc, year])

        infom.append(infomember0)

        driver.find_element_by_xpath('//*[@id="return"]').click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "content")))
        time.sleep(2)

    if i < npg + 1:
        if i == int(i/10) *10:
            driver.find_element_by_link_text("下一页").click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "content")))
            time.sleep(12)
        else:
            driver.find_element_by_link_text("下一页").click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "content")))
            time.sleep(2)
        #driver.switch_to.default_content()


with open("D:\\temp\\poor\\allpoor-" + str(year) + "p.txt", "wb") as fp:
    pickle.dump(poor, fp)

"""