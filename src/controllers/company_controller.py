from typing import Annotated, Optional
from fastapi import  Depends
from src.models.company import Company as model
from src.schemas.company import CompanyIn as input_schema
from src.schemas.company import CompanyCreate as create_schema


from src.services.company import CompanyService
from src.services.user import AuthService



class CompanyController:

    def __init__(
        self,
        service: Annotated[CompanyService, Depends()],
        user_service: Annotated[AuthService, Depends()],
    ) -> None:
        self.service = service
        self.user_service = user_service

  

    async def get_by_id(self, id:int):
        return await self.service.get_one(id)
    
    async def get_all(self):
        return await self.service.get_all()
    
    async def update(self, id:int, body: create_schema):
        return await self.service.update(id, body)

    async def delete(self, id:int):
        return await self.service.delete(id)