
from typing import Annotated, List, Optional
from fastapi import  Depends, HTTPException
from pydantic import ValidationError
from src.config.database import Base
from src.controllers.auth_controller import AuthController
from src.payload.responses.base import GenericResponse

from src.controllers.company_controller import CompanyController as ctrl
from src.schemas.company import CompanyOut as output_schema
from src.schemas.company import CompanyCreate as create_schema
from src.security.access_token_bearer2 import AccessTokenBearer2
from .routers import company_router as router





@router.get("", response_model=List[output_schema])
async def get_all(
    controller: Annotated[ctrl, Depends()],
):
    resp = await controller.get_all()
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

          
 

@router.put("", response_model=output_schema)
async def update(
    controller: Annotated[ctrl, Depends()],
    body: create_schema,
    auth_controller: Annotated[AuthController, Depends()],
    token: str = Depends(AccessTokenBearer2()),
):
    try:
        id = await auth_controller.get_current_user_id(token)

        resp = await controller.update(id,body)

        if not resp:
            raise HTTPException(
                status_code=404,
                detail=GenericResponse(
                    error="no companies found with given id or attributes not found "
                ).__dict__,
        )

        return resp
    except ValidationError as e:
        # Log the validation errors
        error_messages = e.errors()
        for error in error_messages:
            field = error["loc"][0]
            reason = error["msg"]
            print(f"Validation error for field '{field}': {reason}")