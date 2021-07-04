import logging
import sys
import os
import requests
import json
from app.model.schemas import Medicine
from app.scraper import scraper
sys.path.append(os.path.realpath(os.path.relpath("../..")))
logger = logging.getLogger(__name__)

def find_medicine(search_str:str):
    brand_name,generic_name,isExact = scraper.scraper_fine(search_str)
    medicine = Medicine(brand_name=brand_name,generic_name=generic_name,isExact=isExact,search_name=search_str)
    if medicine.generic_name: medicine.substitutes = get_list_of_substitutes(medicine.generic_name)
    return medicine

def get_list_of_substitutes(generic_name:str):
    url = os.getenv('DAILY_MED') + generic_name
    response = json.loads(requests.request("GET", url,timeout=5).text)
    data = response['data']
    substitues = [each['drug_name'] for each in data if each['name_type']=='B']
    return substitues
