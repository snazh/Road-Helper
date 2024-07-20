from backend.src.repositories.roadsign import RoadSignsRepository
from backend.src.repositories.user import UserRepository

from backend.src.services.roadsign import RoadSignsService
from backend.src.services.user import UsersService
from backend.src.services.auth import AuthService
from backend.src.utils.auth.auth import JWTAuthRepository


def roadsigns_service():
    return RoadSignsService(RoadSignsRepository)


def users_service():
    return UsersService(UserRepository)


def auth_service():
    return AuthService(JWTAuthRepository, UserRepository)
