from app.scraper import queries
from fastapi import APIRouter
import sys
import os
sys.path.append(os.path.realpath(os.path.relpath("../..")))

import logging
logger = logging.getLogger(__name__)



router=APIRouter()

@router.get('/get-medicine-info/{search_str}')
async def get_medicine_info(search_str:str):
    result = queries.find_medicine(search_str)
    logger.info(result)
    return result

@router.get('/get-substitutes/{generic_name}')
async def get_substitutes(generic_name:str):
    result = queries.get_list_of_substitutes(generic_name)
    logger.info(result)
    return result