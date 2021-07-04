import logging
import sys
import os
from app.model.schemas import Medicine
from app.scraper import scraper
sys.path.append(os.path.realpath(os.path.relpath("../..")))
logger = logging.getLogger(__name__)

def find_medicine(search_str:str):
    brand_name,generic_name,isExact = scraper.scraper_fine(search_str)
    medicine = Medicine(brand_name=brand_name,generic_name=generic_name,isExact=isExact,search_name=search_str)
    logger.info(f'{medicine}')
    return medicine
