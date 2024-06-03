
from typing import Annotated, List, Optional
from fastapi import  Depends, HTTPException
from fastapi.responses import JSONResponse
from src.config.database import Base
from src.payload.responses.base import GenericResponse

from src.controllers.application_controller import ApplicationController as ctrl
from src.models.application import Application as model
from src.schemas.application import ApplicationOut as output_schema
from src.schemas.application import ApplicationIn as input_schema
from src.schemas.application import ApplicationCreate as create_schema
from src.security.access_token_bearer2 import AccessTokenBearer2
from .routers import application_router as router



@router.post("", response_model=int)
async def create(
    controller: Annotated[ctrl, Depends()],
    body: create_schema,
    token: str = Depends(AccessTokenBearer2()),
):
    resp = await controller.create(body,token)

    if not resp:
        raise HTTPException(
            status_code=404,
            detail=GenericResponse(
                error="attributes not found"
            ).__dict__,
        )
    
    return resp

@router.get("", response_model=List[output_schema])
async def get_all(
    controller: Annotated[ctrl, Depends()],
):
    resp = await controller.get_all()
    if not resp:
        return list()
    return resp

@router.get("/my_jobs", response_model=List[output_schema])
async def get_current_user_applications(
    controller: Annotated[ctrl, Depends()],
    token: str = Depends(AccessTokenBearer2()),
):
    resp = await controller.get_current_user_applications(token)
    if not resp:
        return list()
    return resp

@router.get("/job_apps/{id}", response_model=List[output_schema])
async def get_job_applications(
    controller: Annotated[ctrl, Depends()],
    id: int
):
    resp = await controller.get_job_applications(id)
    if not resp:
        return list()
    return resp


@router.get("/{id}", response_model=output_schema)
async def get_by_id(
    id: int,
    controller: Annotated[ctrl, Depends()],
):
    resp = await controller.get_by_id(id)

    if not resp:
        raise HTTPException(
            status_code=404,
            detail=GenericResponse(
                error="no record found with given id"
            ).__dict__,
        )
    return resp



@router.delete("/{id}", response_model=GenericResponse)
async def delete(
    id: int,
    controller: Annotated[ctrl, Depends()],
):
    resp = await controller.delete(id)
    if not resp:
        raise HTTPException(
            status_code=404,
            detail=GenericResponse(
                error="no records found with given id"
            ).__dict__,
        )
    return GenericResponse(
            message="deleted succesfully",
            error= None
            )
          
@router.put("/accept/{id}", response_model=output_schema)
async def accept_job_application(
    id: int,
    controller: ctrl = Depends()
):
    resp =  await controller.accept_application(id)
    if not resp:
         raise HTTPException(
            status_code=404,
            detail=GenericResponse(
                error="no records found with given id"
            ).__dict__,
            )
    return resp
    

@router.put("/reject/{id}", response_model=output_schema)
async def reject_job_application(
    id: int,
    controller: ctrl = Depends()
):
    resp = await controller.reject_application(id)
    if not resp:
        raise HTTPException(
            status_code=404,
            detail=GenericResponse(
                error="no records found with given id"
            ).__dict__,
            )
    return resp
    

@router.put("/{id}", response_model=output_schema)
async def update(
    id: int,
    controller: Annotated[ctrl, Depends()],
    body: create_schema
):
    resp = await controller.update(id,body)

    if not resp:
        raise HTTPException(
            status_code=404,
            detail=GenericResponse(
                error="no record found with given id or relationship attributes not found in db"
            ).__dict__,
    )

    return resp

