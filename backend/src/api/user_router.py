from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Request

from backend.src.services.user import UsersService
from backend.src.api.dependecies import users_service, auth_service

from backend.src.services.auth import AuthService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/get-all-users", status_code=status.HTTP_200_OK)
async def get_all_users(
        request: Request,
        service: Annotated[UsersService, Depends(users_service)],
        auth: Annotated[AuthService, Depends(auth_service)]
):
    users = await service.get_all_users()
    return {"users": users}


@router.get("/get-user", status_code=status.HTTP_200_OK)
async def get_specific_user(
        user_id: int,
        service: Annotated[UsersService, Depends(users_service)]

):
    sign = await service.get_specific_user(user_id)

    return sign


@router.delete("/delete-user", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        user_id: int,
        service: Annotated[UsersService, Depends(users_service)],

):
    try:
        await service.delete_user(user_id)
        return {
            "status": "success",
            "data": None,
            "details": "The user has been successfully deleted"
        }

    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"An error occurred while deleting the user"
        })
