from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Response

from backend.src.api.dependecies import users_service, auth_service
from backend.src.schemas.user import UserSchemaAdd, UserLoginSchema
from backend.src.services.auth import AuthService
from backend.src.services.user import UsersService

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
        user: UserSchemaAdd,
        service: Annotated[AuthService, Depends(auth_service)],
):
    return await service.register_user(user)
    # try:
    #     user_id = await service.register_user(user)
    #     return {
    #         "status": "success",
    #         "data": user_id,
    #         "details": "Successful registrations"
    #     }
    #
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail={
    #         "status": "error",
    #         "data": None,
    #         "details": f"{e}"
    #     })


@router.post("/login", status_code=status.HTTP_201_CREATED)
async def login(
        response: Response,
        user: UserLoginSchema,
        service: Annotated[AuthService, Depends(auth_service)],
):
    try:

        token = await service.authorize_user(user, response)

        return {
            "status": "success",
            "data": token,
            "details": "Successful registrations"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"{e}"
        })
