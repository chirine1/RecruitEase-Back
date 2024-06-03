from typing import Annotated, Optional
from fastapi import  Depends
from src.models.candidate import Candidate as model
from src.schemas.candidate import CandidateIn as input_schema
from src.schemas.candidate import CandidateCreate as create_schema

from src.services.candidate import CandidateService
from src.services.user import AuthService



class CandidateController:

    def __init__(
        self,
        service: Annotated[CandidateService, Depends()],
        user_service: Annotated[AuthService, Depends()],
    ) -> None:
        self.service = service
        self.user_service = user_service

  

    async def get_candidate_by_id(self, id:int):
        return await self.service.get_one(id)
    
    async def get_all_candidates(self):
        return await self.service.get_all()
    
    async def update_candidate(self, id:int, body: create_schema
    ) -> Optional[model]:
        return await self.service.update(id, body)

    async def delete_candidate(self, id:int):
        return await self.service.delete(id)