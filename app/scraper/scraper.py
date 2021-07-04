import sys
import os
import requests
import json
import re
from pathlib import Path
from dotenv import load_dotenv
from bs4 import BeautifulSoup
sys.path.append(os.path.realpath(os.path.relpath("../..")))
import logging
logger = logging.getLogger(__name__)
load_dotenv(Path(os.path.realpath(os.path.relpath("..")))/"dev.env")

def string_cleanup(string:str):
    if string[-1]==')':string = string[:-1] #to remove ) bracket
    if string[-1]=='.': string = string[:-1] # to remove . at the end
    return string

def raw_search(name:str):
    logger.info('\t\tPerforming a RAW SEARCH for '+name+'\n')
    brand_name = None
    generic_name = None
    url = os.getenv('MEDICINE_SITE') + name
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html5lib')
    text = str(soup)
    path = '/india/drug/info/'
    cursor = text.find(path)
    offset = len(path) + len(name)+len('?mtype=generic')
    text = text[cursor:cursor+offset].strip()
    if text.find('?mtype=generic') >0: #given name is generic
        generic_name = name
    else: #given name is brand
            text = soup.get_text()
            cursor = text.find('Generic Name')
            extract = text[cursor:cursor+300]
            extract = extract.split()
            extract = ' '.join(extract)
            try:
                generic_name = extract.split(':')[1].strip()
            except:
                generic_name = ''
            if name ==generic_name.upper():
                generic_name = name
            else:
                brand_name=name
    isExact = False
    return brand_name,generic_name,isExact

def scraper_fine(name:str): #scraping for validation of medicine type
    logger.info(f'Scraping for "{name}"')
    url = os.getenv('MEDICINE_SITE') + name
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html5lib')
    extract = soup.find("meta",attrs={'name':'DESCRIPTION'})
    brand_name=generic_name= None
    if extract:
        extract = extract['content']
        extract = extract.split(':')[0]
        if extract.find('(')<0: #search_name is a generic name
            generic_name = extract.lower()
        else: #search_name is a brand name
            extract = extract.split('(')
            brand_name = extract[0].upper()
            generic_name = (extract[1].lower())
            generic_name = string_cleanup(generic_name)
        isExact = True                  
        return brand_name,generic_name,isExact
    else:
        logger.info(f'{name} not found while scraping')
        isExact = False
        return raw_search(name)

def generic_info(name:str):
    logger.info(f'Trying to find drug description for {name}')
    url = os.getenv('GENERIC_INFO') + name +'.html'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html5lib')
    text = str(soup)
    logger.info(text)
    return True