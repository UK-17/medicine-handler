import logging
import sys
import os
import requests
import json
sys.path.append(os.path.realpath(os.path.relpath("../..")))
from app.model.schemas import Medicine
from pathlib import Path
from app.scraper import scraper
logger = logging.getLogger(__name__)

DAILY_MED = 'https://dailymed.nlm.nih.gov/dailymed/services/v2/drugnames.json?drug_name='


def find_medicine(search_str:str):
    logger.info(f'Searching {search_str} on MIMS.')
    brand_name,generic_name,isExact = scraper.scraper_fine(search_str)
    medicine = Medicine(brand_name=brand_name,generic_name=generic_name,isExact=isExact,search_name=search_str)
    if medicine.generic_name: medicine.substitutes = get_list_of_substitutes(medicine.generic_name)
    return medicine

def get_list_of_substitutes(generic_name:str):
    logger.info(f'Finding substitutes for {generic_name}')
    url = DAILY_MED + generic_name
    response = json.loads(requests.request("GET", url,timeout=5).text)
    data = response['data']
    substitues = [each['drug_name'] for each in data if each['name_type']=='B']
    return substitues

if __name__=="__main__":
    query = input("enter medicine query: ")
    medicine_details = find_medicine(query)
    print(f'Result : {medicine_details}')

