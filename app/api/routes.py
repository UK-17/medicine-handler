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

@router.post('/find-medicine')
async def create_author(data:schemas.Medicine):
    result = queries.find_medicine(data)
    logger.info(result)
    return result