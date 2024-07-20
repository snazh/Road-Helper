from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from backend.src.api.dependecies import users_service
from backend.src.schemas.user import UserSchemaAdd
from backend.src.services.user import UsersService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
        user: UserSchemaAdd,
        service: Annotated[UsersService, Depends(users_service)],
):
    try:
        user_id = await service.add_user(user)
        return {
            "status": "success",
            "data": user_id,
            "details": "Successful registrations"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"{e}"
        })


@router.get("/get-all-users", status_code=status.HTTP_200_OK)
async def get_all_users(
        service: Annotated[UsersService, Depends(users_service)],
):
    signs = await service.get_all_users()
    return signs


@router.get("/get-user", status_code=status.HTTP_200_OK)
async def get_specific_user(
        user_id: int,
        service: Annotated[UsersService, Depends(users_service)]

):
    sign = await service.get_specific_user(user_id)

    return sign


@router.delete("/delete-user", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        sign_id: int,
        service: Annotated[UsersService, Depends(users_service)],

):
    try:
        await service.delete_user(sign_id)
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
