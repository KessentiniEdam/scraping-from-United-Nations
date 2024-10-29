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
url = 'https://scsanctions.un.org/resources/xml/en/consolidated.xml'

# Setup Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

all_tags = []

def extract_tags(element):
    for child in element.children:
        if child.name:
            if child.name not in all_tags:
                all_tags.append(child.name)
            extract_tags(child)

try:
    # Open the webpage
    driver.get(url)
    
    # Wait for the XML data to load (adjust the wait time as needed)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'INDIVIDUAL'))
    )
    
    # Get the page source
    page_source = driver.page_source
    
    # Parse the XML content
    soup = BeautifulSoup(page_source, 'xml')
    individuals = soup.find_all('INDIVIDUAL')
    
    # Extract tags for INDIVIDUAL elements
    for individual in individuals:
        extract_tags(individual)
    indTAGS = all_tags.copy()
    all_tags = []
    
    entities = soup.find_all('ENTITY')
    
    # Extract tags for ENTITY elements
    for entity in entities:
        extract_tags(entity)
    entTAGS = all_tags.copy()
    
    set1 = set(indTAGS)
    set2 = set(entTAGS)
    
    # Debugging info
    print(len(set1.difference(set2)))
    print(len(set1.intersection(set2)))
    
    # List to hold entity records
    entity_records = []
    for entity in entities:
        record = {}
        for tag in set2:
            element = entity.find(tag)
            if element:
                if element.children:
                        if (len(list(element.children)))==1:
                  
                             record[tag] =element.text
                        elif(len(list(element.children)))>1:
                            l=[e.text.strip() for e in element.children if element.name]
                            if(len(l))>2:
                                record[tag]=' '.join(l)
                            else:
                                record[tag]=l[1]

            else:
                record[tag] = '?'
        entity_records.append(record)
    
    # List to hold individual records
    individual_records = []
    for individual in individuals:
        record = {}
        for tag in set1:
            element = individual.find(tag)
            if element:
                  if element.children:
                        if (len(list(element.children)))==1:
                  
                             record[tag] =element.text.strip()
                        elif(len(list(element.children)))>1:
                            l=[e.text.strip() for e in element.children if element.name]
                            if(len(l))>2:
                                record[tag]=' '.join(l)
                            else:
                                record[tag]=l[1].strip()

            else:
                record[tag] = '?'
        individual_records.append(record)
    
    # Write to CSV for entities
    if entity_records:
        csv_filename = 'UN_entities.csv'
        csv_filepath = os.path.join(os.getcwd(), csv_filename)
        keys = set2
        with open(csv_filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=keys)
            writer.writeheader()
            writer.writerows(entity_records)
    
    # Convert to JSON for entities
    if entity_records:
        json_filename = 'ENTITIES.json'
        json_dir = 'json_files'
        json_filepath = os.path.join(os.getcwd(), json_dir, json_filename)
        if not os.path.exists(json_dir):
            os.makedirs(json_dir)
        with open(json_filepath, 'w', encoding='utf-8') as jsonfile:
            json.dump(entity_records, jsonfile, ensure_ascii=False, indent=4)
    
    # Write to CSV for individuals
    if individual_records:
        csv_filename = 'UN_individuals.csv'
        csv_filepath = os.path.join(os.getcwd(), csv_filename)
        keys =set1
        with open(csv_filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=keys)
            writer.writeheader()
            writer.writerows(individual_records)
    
    # Convert to JSON for individuals
    if individual_records:
        json_filename = 'INDIVIDUALS.json'
        json_dir = 'json_files'
        json_filepath = os.path.join(os.getcwd(), json_dir, json_filename)
        if not os.path.exists(json_dir):
            os.makedirs(json_dir)
        with open(json_filepath, 'w', encoding='utf-8') as jsonfile:
            json.dump(individual_records, jsonfile, ensure_ascii=False, indent=4)
    
    # Load into Pandas DataFrame if needed for additional processing
    df_entities = pd.DataFrame(entity_records)
    df_individuals = pd.DataFrame(individual_records)
    
    print("Data processing complete")

except Exception as e:
    print(f"Failed to retrieve XML data: {e}")
finally:
    driver.quit()
