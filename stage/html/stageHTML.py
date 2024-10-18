from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import csv
import json
import pandas as pd
import os
 
# URL of the XML data
url = 'https://scsanctions.un.org/consolidated'
 
# Setup Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
StrongList= ['Title:','Designation: ','Listed on: ','Nationality: ','Good quality a.k.a.: ','Low quality a.k.a.: ','Address: ','Passport no: ','POB: ','DOB: ','National identification no: ','A.k.a.: ','F.k.a.: ']
def search(trs,records):
    for tr in trs:
        record={}
        strongs=tr.find_all('strong')  
        record['REFERENCE_NUMBER']=strongs[0].text
        strongs=strongs[1:]
        for strong in strongs:
           
            # elif strong.string=='Designation: ':#in ['designation','listed_on','nationality']etc
            if strong.string in StrongList:
               list=[]
               item=''
               for n in strong.next_siblings:
                 if n.get_text() not in list:
                    if n.name is None:
                        item+=n.string.strip()
                    elif n.name=='span':
                        list.append(n.get_text(strip=True))
                        item="".join(list)
    
    
                    elif n.name=='strong' and n.text not in StrongList: # sinon kén ma 3andouch esm exemple toul nel9aw afghanistan n7ottlou el key howa el strong.string exemple nationality,wel item howa n.text.strip()
                        if n.text.find(')')!=-1:
                        
                         list.append(n.text)
                         list.append(n.next_sibling.text)
                         item=' '.join(list)
                        
    
    
                    elif n.name=='strong' and n.text in StrongList: # kifkif in ['designation','listed_on','nationality']etc
                        
                        record[strong.string]=item
                        break
                        
               
               
               
            # elif strong.next_sibling.name=='span':
            #    record[strong.string.strip()]=strong.next_sibling.get_text(strip=True)
            else:
               record[strong.string.strip()]=strong.next_sibling.get_text(strip=True)
             
        # listed_on_tags= soup.find_all('strong', string='Listed on: ')
        # for listed_on_tag in listed_on_tags:
        #     spans=listed_on_tag.next_siblings
        #     listed_on=[]
        #     for span in spans:
        #         if span.name=="span":
        #          listed_on.append(span.get_text(strip=True))
 
        #     record['Listed on']=','.join(listed_on)
        #     if individual_records:
        #         existing_keys = set(record.keys())
        #         for ind in individual_records:
        #           for key in existing_keys:
        #             if key not in ind:
        #                 ind[key] = ''
                   
        if records:
                existing_keys = set(record.keys())
                for ind in records:
                  for key in existing_keys:
                    if key not in ind:
                        ind[key] = ''
       
        records.append(record)
try:
    # Open the webpage
    driver.get(url)
   
    # Wait for the page to load (adjust the wait time as needed)
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.TAG_NAME, 'html'))
    )
   
    # Get the page source
    page_source = driver.page_source
    individual_records=[]
    entity_records=[]
    # Parse the HTML content
    soup = BeautifulSoup(page_source, 'html.parser')
    tables=soup.find_all('table')
    trs1=tables[2].find_all('tr',{'class':'rowtext'})
    trs2=tables[3].find_all('tr',{'class':'rowtext'})
    # trs2=tables[3].find_all('tr',{'class':'rowtext'})
    search(trs1,individual_records)
    search(trs2,entity_records)
    # search(trs2[:5],entity_records)
    csv_filepath = os.path.join(os.getcwd(), 'individuals.csv')
    keys1= individual_records[0].keys()
    with open(csv_filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys1)
        writer.writeheader()
        writer.writerows(individual_records)

    csv_filepath = os.path.join(os.getcwd(), 'entities.csv')
    keys2= entity_records[0].keys()
    with open(csv_filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys2)
        writer.writeheader()
        writer.writerows(entity_records)
    # csv_filepath = os.path.join(os.getcwd(), 'entities1.csv')
    # keys = entity_records[0].keys()
    # with open(csv_filepath, 'w', newline='', encoding='utf-8') as csvfile:
    #     writer = csv.DictWriter(csvfile, fieldnames=keys)
    #     writer.writeheader()
    #     writer.writerows(entity_records)
 
    # print(strongs[2].string)
    # print(strongs[3].string)
    # print(strongs[4].string)
 
    if individual_records:
        json_filename = 'INDIVIDUALS.json'
        json_dir = 'json_files'
        json_filepath = os.path.join(os.getcwd(), json_dir, json_filename)
        if not os.path.exists(json_dir):
            os.makedirs(json_dir)
        with open(json_filepath, 'w', encoding='utf-8') as jsonfile:
            json.dump(individual_records, jsonfile, ensure_ascii=False, indent=4)
    if entity_records:
        json_filename = 'ENTITIES.json'
        json_dir = 'json_files'
        json_filepath = os.path.join(os.getcwd(), json_dir, json_filename)
        if not os.path.exists(json_dir):
            os.makedirs(json_dir)
        with open(json_filepath, 'w', encoding='utf-8') as jsonfile:
            json.dump(entity_records, jsonfile, ensure_ascii=False, indent=4)
    
 
    print(entity_records[0])
    print(individual_records[0])
    # sectionHeader=soup.find_all('tr',{'class':'display'})
    # a=sectionHeader[0].get_text()
   
    # print(sectionHeader[0].get_text())#.text.strip()
    print("Data processing complete")
 
except Exception as e:
    print(f"Failed to retrieve XML data: {e}")
 
finally:
    driver.quit()