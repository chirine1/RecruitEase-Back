
from typing import Annotated, List, Optional, Union
from fastapi import  Depends, HTTPException
from pydantic import ValidationError
from src.config.database import Base
from src.controllers.auth_controller import AuthController
from src.payload.responses.base import GenericResponse

from src.controllers.candidate_controller import CandidateController
from src.models.candidate import Candidate as model
from src.schemas.candidate import CandidateOut as output_schema
from src.schemas.candidate import CandidateIn as input_schema
from src.schemas.candidate import CandidateCreate as create_schema
from src.security.access_token_bearer2 import AccessTokenBearer2

from .routers import candidate_router





@candidate_router.get("/all", response_model=List[output_schema])
async def get_all_candidates(
    controller: Annotated[CandidateController, Depends()],
):
    resp = await controller.get_all_candidates()
    if not resp:
        return list()
    return resp


@candidate_router.delete("/{id}", response_model=GenericResponse)
async def delete_candidate(
    id: int,
    controller: Annotated[CandidateController, Depends()],
):
    resp = await controller.delete_candidate(id)
    if not resp:
        raise HTTPException(
            status_code=404,
            detail=GenericResponse(
                error="no candidate found with given id"
            ).__dict__,
        )
    return GenericResponse(
            message="deleted succesfully",
            error= None
            )
          
 

@candidate_router.get("/{id}", response_model=output_schema)
async def get_candidate_by_id(
    id: int,
    controller: Annotated[CandidateController, Depends()],
):
    resp = await controller.get_candidate_by_id(id)

    if not resp:
        raise HTTPException(
            status_code=404,
            detail=GenericResponse(
                error=f"no candidate found with given id"
            ).__dict__,
        )

    return resp

@candidate_router.put("", response_model=output_schema)
async def update_candidate(
    controller: Annotated[CandidateController, Depends()],
    auth_controller: Annotated[AuthController, Depends()],
    body: create_schema,
    token: str = Depends(AccessTokenBearer2())
):
    try:
        id = await auth_controller.get_current_user_id(token)

        resp = await controller.update_candidate(id,body)

        if not resp:
            raise HTTPException(
                status_code=404,
                detail=GenericResponse(
                    error="no candidate found with given id or attributes not found "
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