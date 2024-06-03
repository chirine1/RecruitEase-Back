from datetime import datetime
from enum import Enum
from typing import Annotated, List, Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends
from src.config.database import  get_session


from src.models.job import Job as model
from src.schemas.job import JobCreate as create_schema

from src.services.company import CompanyService
from src.services.industry import IndustryService
from src.services.skill import SkillService



class JobService:
    def __init__(
            self,
            session: Annotated[
                AsyncSession, Depends(get_session)
            ],
            industry_service: Annotated[
                IndustryService, Depends()
            ],
            skill_service: Annotated[
                SkillService, Depends()
            ],
            company_service: Annotated[
                CompanyService, Depends()
            ],
        ) -> None:
            self._sess = session
            self.services_many = {"skills": skill_service}
            self.services_one = {"industry": industry_service}
            self.company_service = company_service


    async def create(self, body: create_schema , company_id):
        db_model = model()
        company = await self.company_service.get_one(company_id)
        db_model.company = company
        populated_db_model = await self.populate_object(db_model,body)
        if not populated_db_model:
            return
        self._sess.add(populated_db_model)
        await self._sess.commit()
        return db_model
    

    async def get_all(self):
        q = select(model)
        all = (await self._sess.exec(q)).all()
        for job in all:
            deadline_is_expired = await self.is_expired_job_with_id(job.id)
            if deadline_is_expired:
                await self.expire_job(job.id)
        return  (await self._sess.exec(q)).all()

    async def get_one(self, id:int):
        q = select(model).where(model.id == id)
        result = (await self._sess.exec(q)).one_or_none()
        return result
    
    async def get_all_by_company(self, company_id:int):
        company = await self.company_service.get_one(company_id)
        if not company:
            return 
        q = select(model).where(model.company == company)
        all = (await self._sess.exec(q)).all()
        for job in all:
            deadline_is_expired = await self.is_expired_job_with_id(job.id)
            if deadline_is_expired:
                await self.expire_job(job.id)
        return  (await self._sess.exec(q)).all()

    async def delete(self, id:int):
        result = await self.get_one(id)
        if not result:
             return 
        await self._sess.delete(result)
        await self._sess.commit()
        return True
  
    async def update(self, id:int , body: create_schema):
        result : model = await self.get_one(id)
        if result == None:
              return 
        
        if not await self.populate_object(result,body):     #sometimes its none due to db obj not found for relationships
            return

        self._sess.add(result) 
        await self._sess.commit()
        await self._sess.refresh(result)
        return result
    
    async def extend_deadline(self,id:int,deadline: datetime):
        result: Optional[model] = await  self.get_one(id)
        if not result :
            return
        result.deadline = deadline
        self._sess.add(result) 
        await self._sess.commit()
        await self._sess.refresh(result)
        return result
    
    async def is_expired_job_with_id(self,id:int):
        result: Optional[model] = await  self.get_one(id)
        if not result :
            return
        now = datetime.now().replace(tzinfo=None)
        if result.deadline < now:
            return True  # Deadline is past
        else:
            return False  # Deadline is still in the future
        
    async def expire_job(self, id: int):
        result: Optional[model] = await  self.get_one(id)
        if not result :
            return
        result.status = "expired"
        self._sess.add(result) 
        await self._sess.commit()
        return result 

    async def cancel_job(self, id:int):
        result: Optional[model] = await  self.get_one(id)
        if not result :
            return
        result.status = "cancelled"
        self._sess.add(result) 
        await self._sess.commit()
        return result 

    async def populate_object(self,dbmodel:model, body: create_schema ):
        for attr, value in body.__dict__.items():
            if hasattr(dbmodel, attr) and isinstance(value,(int,str,Enum,float,datetime)):
                setattr(dbmodel, attr, value)
        #relationships many
        for relationship_attr in self.services_many.keys():
            relationship_attr_list_of_objects: List = getattr(body,relationship_attr)  #list of objects contained in the list attribute in the body(e.g. industries)
            service = self.services_many.get(relationship_attr)  #get rthe coresponding service dependancy
            new_list = list()  #initialize the new list to replace the old one 
            for dict in relationship_attr_list_of_objects:  #iterate over each obj in the list from body
                label = getattr(dict,"label")
                obj_to_add_to_list_attr  = await service.get_one_by_unique_label(label)   # type: ignore  # fetch the (e.g industry) from the db 
                if not obj_to_add_to_list_attr:
                    return #"attribute does not match db"
                new_list.append(obj_to_add_to_list_attr)
            setattr(dbmodel, relationship_attr, new_list)      
        #relationships one
        for relationship_attr in self.services_one.keys(): 
            service = self.services_one.get(relationship_attr)  #get the coresponding service dependancy
            relationship_attr_from_body = getattr(body,relationship_attr)
            label = getattr(relationship_attr_from_body,"label")
            obj_to_add = await service.get_one_by_unique_label(label) # type: ignore      #find the obj in db
            if not obj_to_add:
                return
            setattr(dbmodel, relationship_attr, obj_to_add)      #assign the obj to model 
        
        return dbmodel 
