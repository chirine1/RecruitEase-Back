from typing import Annotated, Optional
from fastapi import  Depends
from src.models.skill import Skill as model
from src.schemas.skill import SkillIn as input_schema
from src.schemas.skill import SkillCreate as create_schema
from src.services.skill import SkillService as srv




class SkillController:

    def __init__(
        self,
        service: Annotated[srv, Depends()],
    ) -> None:
        self.service = service

  
    async def create(self, body:create_schema):
        return await self.service.create(body)

    async def get_by_id(self, id:int):
        return await self.service.get_one(id)
    
    async def get_all(self):
        return await self.service.get_all()
    
    async def update(self, id:int, body: create_schema):
        return await self.service.update(id, body)

    async def delete(self, id:int):
        return await self.service.delete(id)