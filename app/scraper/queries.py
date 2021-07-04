import logging
import sys
import os
from app.model.schemas import Medicine
from app.scraper import scraper
sys.path.append(os.path.realpath(os.path.relpath("../..")))
logger = logging.getLogger(__name__)

def find_medicine(medicine:Medicine):
    medicine.brand_name,medicine.generic_name,medicine.isExact = scraper.scraper_fine(medicine.search_name)
    logger.info(f'{medicine}')
    return medicine
