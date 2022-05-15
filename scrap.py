from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests
import pandas as pd
from selenium.webdriver.common.by import By

starturl = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"
browser = webdriver.Chrome("chromedriver.exe")
browser.get(starturl)
time.sleep(10)

headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date","hyperlink","planet_type", "planet_radius", "orbital_radius", "orbital_period", "eccentricity"]
planetdata = []
def scrap():
    
    for i in range(0,5):
        while True:
            time.sleep(2)
            soup = BeautifulSoup(browser.page_source,"html.parser")
            currentpage = int(soup.find_all("input",attrs = {"class","page_num"})[0].get("value"))
            if currentpage<i:
                browser.find_element(By.XPATH,value = '//*[@id="primary_column"]/div[1]/div[2]/div[1]/div/nav/span[2]/a').click()
            elif currentpage>i:
                browser.find_element(By.XPATH,value = '//*[@id="primary_column"]/div[1]/div[2]/div[1]/div/nav/span[1]/a').click()
            else :
                break

        for ultag in soup.find_all("ul",attrs = {"class","exoplanet"}):
            litags = ultag.find_all("li")
            templist = []
            for index,litag in enumerate(litags):
                if index==0:
                    templist.append(litag.find_all("a")[0].contents[0])
                else:
                    try:
                        templist.append(litag.contents[0])
                    except:
                        templist.append("")
            hyperlinktag = litags[0]
            templist.append("https://exoplanets.nasa.gov"+hyperlinktag.find_all("a",href = True)[0]["href"])
            planetdata.append(templist)
        browser.find_element_by_xpath('//*[@id="primary_column"]/div[1]/div[2]/div[1]/div/nav/span[2]/a').click()
    
scrap()
newplanetsdata = []
def scrapmoredata(hyperlink):
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content,"html.parser")
        templist = []
        for trtag in soup.find_all("tr",attrs = {"class":"fact_row"}):
            tdtags = trtag.find_all("td")
            for tdtag in tdtags:
                try:
                    templist.append(tdtag.find_all("div",attrs = {"class":"value"})[0].contents[0])
                except:
                    templist.append("")
        newplanetsdata.append(templist)

    except:
        time.sleep(1)
        scrapmoredata(hyperlink)

for index,data in enumerate(planetdata):
    scrapmoredata(data[5])

finalplanetdata=[]

for index,data in enumerate(planetdata):
    newelement = newplanetsdata[index]
    newelement = [element.replace("\n","") for element in newelement]
    newelement = newelement[:7]
    finalplanetdata.append(data+newelement)
with open("final.csv","w") as p:
        attach = csv.writer(p)
        attach.writerow(headers)
        attach.writerows(finalplanetdata)