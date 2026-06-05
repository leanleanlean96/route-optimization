from fastapi import APIRouter, Depends, Request
from fastapi.exceptions import HTTPException
from fastapi import Response

from app.api.schemas.auth.login import LoginRequest, LoginResponse
from app.api.schemas.auth.refresh import RefreshTokenRequest
from app.application.use_cases.auth.login import LoginUseCase
from app.application.use_cases.auth.refresh import RefreshTokenUseCase
from app.core.dependencies import get_login_usecase, get_refresh_token_usecase

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", status_code=200)
async def login(request: LoginRequest, response: Response, usecase=Depends(get_login_usecase)):
    pair = await usecase.execute(request.email, request.password)
    response.set_cookie("access_token", pair.access_token,
        httponly=True, secure=False, samesite="lax", max_age=900)
    response.set_cookie("refresh_token", pair.refresh_token,
        httponly=True, secure=False, samesite="lax", max_age=172800)
    return {"ok": True}

@router.post("/refresh", status_code=200)
async def refresh_token(request: Request, response: Response, usecase=Depends(get_refresh_token_usecase)):
    refresh = request.cookies.get("refresh_token")
    if not refresh:
        raise HTTPException(401)
    pair = await usecase.execute(refresh)
    response.set_cookie("access_token", pair.access_token,
        httponly=True, secure=False, samesite="lax", max_age=900)
    response.set_cookie("refresh_token", pair.refresh_token,
        httponly=True, secure=False, samesite="lax", max_age=172800)
    return {"ok": True}

@router.post("/logout", status_code=200)
async def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"ok": True}