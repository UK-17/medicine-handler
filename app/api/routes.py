from app.scraper import queries
from fastapi import APIRouter, File, UploadFile, Request, Body, Form
from fastapi.param_functions import Depends
from app.model import schemas
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

@router.get('/get-medicine-description/{generic_name}')
async def get_medicine_description(generic_name:str):
    result = queries.get_info_on_generic_name(generic_name)
    logger.info(result)
    return result