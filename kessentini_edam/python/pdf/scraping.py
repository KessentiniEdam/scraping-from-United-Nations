from pdfminer.high_level import extract_text
import re
import csv
import json
import pandas as pd
import os
 
# URL of the XM
s=extract_text('sanctions.pdf') 
s=s.replace('https://scsanctions.un.org/927wken-all.html','').replace('24/06/2024','').replace('15:24','').replace('\f', '')

s = re.sub(r'\d{1,3}/167', '', s)
s=re.sub(r'\w*https://scsanctions.un.org/927wken-all.html\w*','', s).replace('scsanctions.un.org/927wken-all.html','')
s=re.sub(r'\n{2,}','',s)
# Diviser sur 'A. Individuals'
parts = s.split('A. Individuals')

# Diviser la seconde partie sur 'B. Entities and other groups'
subparts = parts[2].split('B. Entities and other groups')

# La partie avant 'B. Entities and other groups' est subparts[0]
individuals_section = subparts[0]

entities_section=subparts[1]
id=re.compile(r'[a-zA-Z]{3}\.\d{3} ')
individuals=re.split(id,individuals_section)
matches = id.findall(individuals_section)
entities=re.split(id,entities_section)
ematches=id.findall(entities_section)
entity_records=[]
#QDe.138
if ematches:
     name_pattern=re.compile(r'Name: (?P<name>.+?)(?=Name \(original script\):|A.k.a.|\n|F.k.a.|Address|Other information|Listed.*on:)',re.DOTALL)
     name_original_script_pattern = re.compile(r'Name \(original script\): (?P<name_original_script>.+?)(?=A.k.a.|\n|F.k.a.|Address|Other information|Listed.*on:)',re.DOTALL)
     listed_on_pattern = re.compile(r'Listed.*on: (?P<listed_on>.+?)(?=Other.*information:)',re.DOTALL)
     aka_pattern= re.compile(r'A.k.a.: (?P<aka>.+?)(?=F.k.a.|Address|Other information|Listed.*on)',re.DOTALL)
     fka_pattern = re.compile(r'F.k.a.: (?P<fka>.+?)(?=Address|Other information|Listed.*on)',re.DOTALL)
     address_pattern = re.compile(r'Address: (?P<address>.+?)(?=Listed.*on:|Other information:)',re.DOTALL)
     other_info_pattern = re.compile(r'Other.*information: (?P<other_info>(.|\n)+)',re.DOTALL)
     
     for ind, match in zip(entities[1:], ematches):  # Ignorer le premier élément de individuals car il est avant le premier ID
        record={}
        #f.write('ID: ' + match + '\n')  
        record['id']=match

        name_match = re.search(name_pattern, ind)
        if name_match:
            record['name']=name_match.group('name').strip().replace('\n','')
            #f.write('Name: ' + name_match.group('name').strip().replace('\n','')+ '\n')

        else:
            record['name']=''
        
        name_original_script_match = re.search(name_original_script_pattern, ind)
        if name_original_script_match:
            record['Name (original script): ']=name_original_script_match.group('name_original_script').strip().replace('\n','').replace('\u0000','')[::-1]
            #f.write('Name (original script): ' + name_original_script_match.group('name_original_script').strip().replace('\n','') + '\n')
        else:
            record["Name (original script): "]=""
       
        aka_match = re.search(aka_pattern, ind)
        if aka_match:
            record['a.k.a.']=aka_match.group('aka').strip().replace('\n','')

            #f.write('Good quality a.k.a.: ' + good_quality_aka_match.group('good_quality_aka').strip().replace('\n','') + '\n')
        else:
            record['a.k.a.']=''
        fka_match = re.search(fka_pattern, ind)
        if fka_match:
            record['f.k.a']=fka_match.group('fka').strip().replace('\n','')
            #f.write('Low quality a.k.a. ' + low_quality_aka_match.group('low_quality_aka').strip().replace('\n','') + '\n')
        else:
            record["f.k.a"]=''
      
        address_match = re.search(address_pattern, ind)
        if address_match:
            #f.write('Address: ' + address_match.group('address').strip().replace('\n','') + '\n')
            record['Address ']=address_match.group('address').strip().replace('\n','') 
        else:
             record['Address ']=''
        listed_on_match = re.search(listed_on_pattern, ind)
        if listed_on_match:
            record['Listed on ']=listed_on_match.group('listed_on').strip().replace('\n','') 

            #f.write('Listed on: ' + listed_on_match.group('listed_on').strip().replace('\n','') + '\n')
        else:
             record['Listed on ']=''
        other_info_match = re.search(other_info_pattern, ind)
        if other_info_match:
            record['Other information ']=other_info_match.group('other_info').strip().replace('\n','') 

            #f.write('Other information: ' + other_info_match.group('other_info').strip().replace('\n','') + '\n')
        else:
             record['Other information ']=''
       
        entity_records.append(record)

        #f.write('\n')
csv_filepath = os.path.join(os.getcwd(),'csv_files', 'entities.csv')
keys1= entity_records[0].keys()
with open(csv_filepath, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=keys1)
    writer.writeheader()
    writer.writerows(entity_records)
    
if entity_records:
    json_filename = 'ENTITIES.json'
    json_dir = 'json_files'
    json_filepath = os.path.join(os.getcwd(), json_dir, json_filename)
    if not os.path.exists(json_dir):
        os.makedirs(json_dir)
    with open(json_filepath, 'w', encoding='utf-8') as jsonfile:
        json.dump(entity_records, jsonfile, ensure_ascii=False, indent=4)


individual_records=[]
if matches:
    name_pattern = re.compile(r'Name: (?P<name>.+?)(?=Name \(original script\):|Title:|Designation:|\n)',re.DOTALL)
    name_original_script_pattern = re.compile(r'Name \(original script\): (?P<name_original_script>.+?)(?=Title:|Designation:)',re.DOTALL)
    dob_pattern = re.compile(r'DOB: (?P<dob>.+?)(?=POB:|Good quality a.k.a.:|Low quality a.k.a.:)',re.DOTALL)
    pob_pattern = re.compile(r'POB: (?P<pob>.+?)(?=Good quality a.k.a.:|Low quality a.k.a.:|Nationality:)',re.DOTALL)
    good_quality_aka_pattern = re.compile(r'Good quality a.k.a.: (?P<good_quality_aka>.+?)(?=Low quality a.k.a.:|Nationality:)',re.DOTALL)
    low_quality_aka_pattern = re.compile(r'Low quality a.k.a.: (?P<low_quality_aka>.+?)(?=Nationality:|Passport no:)',re.DOTALL)
    nationality_pattern = re.compile(r'Nationality: (?P<nationality>.+?)(?=Passport no:|National identification no:)',re.DOTALL)
    passport_no_pattern = re.compile(r'Passport no: (?P<passport_no>.+?)(?=National.*identification.*no:|Address:)',re.DOTALL)
    national_id_no_pattern = re.compile(r'National.*identification.*no: (?P<national_id_no>.+?)(?=Address:|Listed.*on:)',re.DOTALL)
    address_pattern = re.compile(r'Address: (?P<address>.+?)(?=Listed.*on:|Other information:)',re.DOTALL)
    listed_on_pattern = re.compile(r'Listed.*on: (?P<listed_on>.+?)(?=Other.*information:)',re.DOTALL)
    other_info_pattern = re.compile(r'Other.*information: (?P<other_info>(.|\n)+)',re.DOTALL)
    title_pattern=re.compile(r'Title: (?P<title>.*) Designation:',re.DOTALL)
    designation_pattern=re.compile(r'Designation: (?P<designation>.*)DOB:',re.DOTALL)
    for ind, match in zip(individuals[1:], matches):  # Ignorer le premier élément de individuals car il est avant le premier ID
        record={}
        #f.write('ID: ' + match + '\n')  
        record['id']=match

        name_match = re.search(name_pattern, ind)
        if name_match:
            record['name']=name_match.group('name').strip().replace('\n','')
            #f.write('Name: ' + name_match.group('name').strip().replace('\n','')+ '\n')

        else:
            record['name']=''
        
        name_original_script_match = re.search(name_original_script_pattern, ind)
        if name_original_script_match:
            record['Name (original script): ']=name_original_script_match.group('name_original_script').strip().replace('\n','').replace('\u0000','')[::-1]
            #f.write('Name (original script): ' + name_original_script_match.group('name_original_script').strip().replace('\n','') + '\n')
        else:
            record["Name (original script): "]=""
        dob_match = re.search(dob_pattern, ind)
        if dob_match:
            record['date of birth']=dob_match.group('dob').strip().replace('\n','')
            #f.write('DOB: ' + dob_match.group('dob').strip().replace('\n','') + '\n')

        else:
            record['date of birth']=''
        
        pob_match = re.search(pob_pattern, ind)
        if pob_match:
            record['place of birth']=pob_match.group('pob').strip().replace('\n','') 
            #f.write('POB: ' + pob_match.group('pob').strip().replace('\n','') + '\n')
        else:
            record['place of birth']=''
        
        good_quality_aka_match = re.search(good_quality_aka_pattern, ind)
        if good_quality_aka_match:
            record['Good quality a.k.a.']=good_quality_aka_match.group('good_quality_aka').strip().replace('\n','')

            #f.write('Good quality a.k.a.: ' + good_quality_aka_match.group('good_quality_aka').strip().replace('\n','') + '\n')
        else:
            record['Good quality a.k.a.']=''
        low_quality_aka_match = re.search(low_quality_aka_pattern, ind)
        if low_quality_aka_match:
            record['Low quality a.k.a.']=low_quality_aka_match.group('low_quality_aka').strip().replace('\n','')
            #f.write('Low quality a.k.a. ' + low_quality_aka_match.group('low_quality_aka').strip().replace('\n','') + '\n')
        else:
            record["Low quality a.k.a."]=''
        nationality_match = re.search(nationality_pattern, ind)
        if nationality_match:
            record['Nationality']=nationality_match.group('nationality').strip().replace('\n','')
            #f.write('Nationality: ' + nationality_match.group('nationality').strip().replace('\n','') + '\n')
        else:
             record['Nationality']=''
        passport_no_match = re.search(passport_no_pattern, ind)
        if passport_no_match:
            record['passport no']=passport_no_match.group('passport_no').strip().replace('\n','')

            #f.write('Passport no' + passport_no_match.group('passport_no').strip().replace('\n','') + '\n')
        else:
            record['passport no']=""
        national_id_no_match = re.search(national_id_no_pattern, ind)
        if national_id_no_match:
            record['National identification no: ']=national_id_no_match.group('national_id_no').strip().replace('\n','') 
            #f.write('National identification no: ' + national_id_no_match.group('national_id_no').strip().replace('\n','') + '\n')
        else:
                        record['National identification no: ']='' 

        address_match = re.search(address_pattern, ind)
        if address_match:
            #f.write('Address: ' + address_match.group('address').strip().replace('\n','') + '\n')
            record['Address ']=address_match.group('address').strip().replace('\n','') 
        else:
             record['Address ']=''
        listed_on_match = re.search(listed_on_pattern, ind)
        if listed_on_match:
            record['Listed on ']=listed_on_match.group('listed_on').strip().replace('\n','') 

            #f.write('Listed on: ' + listed_on_match.group('listed_on').strip().replace('\n','') + '\n')
        else:
             record['Listed on ']=''
        other_info_match = re.search(other_info_pattern, ind)
        if other_info_match:
            record['Other information ']=other_info_match.group('other_info').strip().replace('\n','') 

            #f.write('Other information: ' + other_info_match.group('other_info').strip().replace('\n','') + '\n')
        else:
             record['Other information ']=''
        title_match=re.search(title_pattern,ind)
        if title_match:
             record['Title']=title_match.group('title').strip().replace('\n','') 
             #f.write('title ' + title_match.group('title').strip().replace('\n','') + '\n')

        else:
             record['Title']=""
        designation_match=re.search(designation_pattern,ind)
        if designation_match:
             record['designation']=designation_match.group('designation').strip().replace('\n','')
             #f.write('designation ' + designation_match.group('designation').strip().replace('\n','') + '\n')

        else:
                          record['designation']=''
        individual_records.append(record)

        #f.write('\n')
    csv_filepath = os.path.join(os.getcwd(),'csv_files', 'individuals.csv')
    keys1= individual_records[0].keys()
    with open(csv_filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys1)
        writer.writeheader()
        writer.writerows(individual_records)
       
    if individual_records:
        json_filename = 'INDIVIDUALS.json'
        json_dir = 'json_files'
        json_filepath = os.path.join(os.getcwd(), json_dir, json_filename)
        if not os.path.exists(json_dir):
            os.makedirs(json_dir)
        with open(json_filepath, 'w', encoding='utf-8') as jsonfile:
            json.dump(individual_records, jsonfile, ensure_ascii=False, indent=4)

"""
 "REFERENCE_NUMBER": "QDe.006 ",
        "Name:": "ARMED ISLAMIC GROUP",
        "Name (original script):": "الجماعة الاسلامية المسلحة",
        "A.k.a.: ": " a)  Al Jamm’ah Al-Islamiah Al- Musallah  b)  GIA  c)  Groupe Islamique Armé ",
        "F.k.a.: ": "na",
        "Address: ": "Algeria",
        "Other information:": "Review pursuant to Security Council resolution 1822 (2008) was concluded\n        
"""

# La partie après 'B. Entities and other groups' est subparts[1]
#entities_section = subparts[1] 
    #  matches=id.findall(individuals_section)
    #  for match in matches:
    #    x=match #d['id']=x
    #    f.write(x+'\n')
       
