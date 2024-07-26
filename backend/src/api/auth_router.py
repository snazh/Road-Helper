from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from backend.src.api.dependecies import auth_service
from backend.src.schemas.user import UserSchemaAdd, UserLoginSchema
from backend.src.services.auth import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
        user: UserSchemaAdd,
        service: Annotated[AuthService, Depends(auth_service)],
):
    try:
        user_id = await service.register_user(user)

        return {
            "status": "success",
            "data": user_id,
            "details": "Successful registrations"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": str(e)
        })


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
            "details": "Successful login"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": str(e)
        })


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
        response: Response,
        service: Annotated[AuthService, Depends(auth_service)]
):
    await service.logout(response)


@router.get("/users/me", status_code=status.HTTP_200_OK)
async def read_current_user(
        request: Request,
        service: Annotated[AuthService, Depends(auth_service)]
):
    try:

        current_user = await service.get_current_user(request)
        return {
            "status": "success",
            "data": current_user,
            "details": "Current user fetched successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": str(e)
        })
