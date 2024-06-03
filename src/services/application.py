from datetime import datetime
from enum import Enum
from typing import Annotated, List, Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends
from src.config.database import  get_session
from src.config.database import engine 
from sqlalchemy import  text
from src.models.application import Application as model
from src.models.enums import Decision
from src.schemas.application import ApplicationIn as input_schema
from src.schemas.application import ApplicationCreate as create_schema
from src.services.candidate import CandidateService
from src.services.job import JobService
from src.services.user import AuthService



class ApplicationService:
    def __init__(
            self,
            session: Annotated[
                AsyncSession, Depends(get_session)
            ],
            candidate_service: Annotated[
                CandidateService, Depends()
            ],
             job_service: Annotated[
                JobService, Depends()
            ],
        ) -> None:
            self._sess = session
            self.services_many = {}
            self.services_one = {}
           

    async def create(self, body: create_schema , candidate_id:int):
        data_dict = { 
        "candidate_id":candidate_id,
        "job_id": body.job_id,
        "motivation_letter": body.motivation_letter,
        "decision": Decision.pending.value
        }

       
        async with engine.connect() as conn:
                await  conn.execute(
                text("INSERT INTO application (motivation_letter, candidate_id, job_id , decision)" +
                    "VALUES (:motivation_letter , :candidate_id, :job_id , :decision)"
                    ),
                [data_dict],
            )
                await conn.commit()
            
        return candidate_id
                
      

    async def get_all(self):
        q = select(model)
        return (await self._sess.exec(q)).all()
    
    async def get_current_user_applications(self,candidate_id:int):
        q = select(model).where(model.candidate_id == candidate_id)
        return (await self._sess.exec(q)).all()
    
    async def get_current_company_applications(self, job_id: int):
        q = select(model).where(model.job_id == job_id)
        all = (await self._sess.exec(q)).all()
        return all

    async def get_one(self, id:int):
        q = select(model).where(model.id == id)
        result = (await self._sess.exec(q)).one_or_none()
        return result

    async def delete(self, id:int):
        result = await self.get_one(id)
        if not result:
             return 
        await self._sess.delete(result)
        await self._sess.commit()
        return True
  
    async def update(self, id:int , body: create_schema):
        result  = await self.get_one(id)
        if result == None:
              return 
        await self.populate_object(result,body)    
        self._sess.add(result) 
        await self._sess.commit()
        await self._sess.refresh(result)
        return result
    

    async def reject_application(self,app_id:int):
        result : Optional[model]= await self.get_one(app_id)
        if not result :
              return
        result.decision = Decision.rejected
        self._sess.add(result) 
        await self._sess.commit()
        return result
    
    async def accept_application(self,app_id:int):
        result : Optional[model]= await self.get_one(app_id)
        if not result :
              return
        result.decision = Decision.accepted
        self._sess.add(result) 
        await self._sess.commit()
        return result

     
    
    async def populate_object(self, dbmodel:model, body: create_schema):
        for attr, value in body.__dict__.items():
            if hasattr(dbmodel, attr) and isinstance(value,(int,str,Enum,float,datetime)):
                setattr(dbmodel, attr, value)
        #relationships many
        for relationship_attr in self.services_many.keys():
            relationship_attr_list_of_objects: List = getattr(body,relationship_attr)  #list of objects contained in the list attribute in the body(e.g. industries)
            service = self.services_many.get(relationship_attr)  #get rthe coresponding service dependancy
            new_list = list()  #initialize the new list to replace the old one 
            for dict in relationship_attr_list_of_objects:  #iterate over each obj in the list from body
                id = getattr(dict,"id")
                obj_to_add_to_list_attr  = await service.get_one(id)   # type: ignore  # fetch the (e.g industry) from the db 
                if not obj_to_add_to_list_attr:
                    return #"attribute does not match db"
                new_list.append(obj_to_add_to_list_attr)
            setattr(dbmodel, relationship_attr, new_list)      
        #relationships one
        for relationship_attr in self.services_one.keys(): 
            service = self.services_one.get(relationship_attr)  #get the coresponding service dependancy
            relationship_attr_from_body = getattr(body,relationship_attr)
            id = getattr(relationship_attr_from_body,"id")
            obj_to_add = await service.get_one(id) # type: ignore      #find the obj in db
            if not obj_to_add:
                return
            setattr(dbmodel, relationship_attr, obj_to_add)      #assign the obj to model 
        
        return dbmodel 