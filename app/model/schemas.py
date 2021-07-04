from pydantic import BaseModel
from typing import List, Optional

class Medicine(BaseModel):
    search_name:str
    brand_name:Optional[str]
    generic_name:Optional[str]
    isExact:Optional[str]
    substitutes:Optional[List]
    
