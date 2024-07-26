from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from backend.src.api.dependecies import roadsigns_service
from backend.src.schemas.roadsign import RoadSignSchemaAdd
from backend.src.services.roadsign import RoadSignsService
from backend.src.services.auth import AuthService

router = APIRouter(
    prefix="/roadsigns",
    tags=["Road Signs"],
)


@router.post("/add-roadsigns", status_code=status.HTTP_201_CREATED)
async def add_sign(
        task: RoadSignSchemaAdd,
        signs_service: Annotated[RoadSignsService, Depends(roadsigns_service)],

):
    try:
        user = current_user
        sign_id = await signs_service.add_sign(task)

        return {
            "status": "success",
            "data": {"sign_id": sign_id, "user": user},
            "details": "Successful registrations"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"{e}"
        })


@router.get("/get-all-roadsigns", status_code=status.HTTP_200_OK)
async def get_all_roadsigns(
        signs_service: Annotated[RoadSignsService, Depends(roadsigns_service)],
):
    signs = await signs_service.get_all_signs()
    return signs


@router.get("/get-specific-sign", status_code=status.HTTP_200_OK)
async def get_specific_roadsign(
        signs_service: Annotated[RoadSignsService, Depends(roadsigns_service)],
        sign_id: int

):
    sign = await signs_service.get_specific_sign(sign_id)

    return sign


@router.delete("/delete-sign", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sign(
        sign_service: Annotated[RoadSignsService, Depends(roadsigns_service)],
        sign_id: int
):
    try:
        await sign_service.delete_sign(sign_id)
        return {
            "status": "success",
            "data": None,
            "details": "The sign has been successfully deleted"
        }

    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"An error occurred while deleting the sign"
        })
