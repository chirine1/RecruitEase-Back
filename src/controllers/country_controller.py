from typing import Annotated, Optional
from fastapi import  Depends
from src.models.country import Country as model
from src.schemas.country import CountryCreate as create_schema

from src.services.country import CountryService



class CountryController:

    def __init__(
        self,
        service: Annotated[CountryService, Depends()],
        
    ) -> None:
        self.service = service
        
    async def create(self, body: create_schema):
        return await self.service.create(body)

    async def get_by_id(self, id:int):
        return await self.service.get_one(id)
    
    async def get_all(self):
        return await self.service.get_all()
    
    async def update(self, id:int, body: create_schema):
        return await self.service.update(id, body)

    async def delete(self, id:int):
        return await self.service.delete(id)