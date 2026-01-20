"""
JWT Authentication Middleware for TallyInsight
Validates JWT tokens from TallyBridge

This middleware:
1. Extracts JWT token from Authorization header
2. Validates token using shared SECRET_KEY
3. Extracts user_id and company_id from token
4. Makes user info available to route handlers
"""

import os
from typing import Optional
from datetime import datetime

from fastapi import HTTPException, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from pydantic import BaseModel


# Load from environment or use default (must match TallyBridge)
SECRET_KEY = os.getenv("SECRET_KEY", "tallybots-super-secret-key-change-in-production-2026")
ALGORITHM = os.getenv("ALGORITHM", "HS256")


class TokenData(BaseModel):
    """Token payload data"""
    user_id: Optional[int] = None
    email: Optional[str] = None
    role: Optional[str] = None
    company_id: Optional[int] = None
    exp: Optional[datetime] = None


class CurrentUser(BaseModel):
    """Current authenticated user"""
    id: int
    email: str
    role: str
    company_id: Optional[int] = None


class JWTBearer(HTTPBearer):
    """
    JWT Bearer token authentication
    Use as dependency: Depends(JWTBearer())
    """
    
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
    
    async def __call__(self, request: Request) -> Optional[str]:
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=401,
                    detail="Invalid authentication scheme. Use Bearer token."
                )
            
            token = credentials.credentials
            payload = verify_token(token)
            
            if not payload:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid or expired token"
                )
            
            # Store user info in request state for later use
            request.state.user = CurrentUser(
                id=payload.get("sub") or payload.get("user_id"),
                email=payload.get("email", ""),
                role=payload.get("role", "user"),
                company_id=payload.get("company_id")
            )
            
            return token
        
        raise HTTPException(
            status_code=401,
            detail="Authorization header missing"
        )


def verify_token(token: str) -> Optional[dict]:
    """
    Verify JWT token and return payload
    
    Args:
        token: JWT token string
        
    Returns:
        Token payload dict if valid, None otherwise
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Check expiration
        exp = payload.get("exp")
        if exp:
            exp_datetime = datetime.fromtimestamp(exp)
            if datetime.now() > exp_datetime:
                return None
        
        return payload
        
    except JWTError as e:
        print(f"JWT Error: {e}")
        return None
    except Exception as e:
        print(f"Token verification error: {e}")
        return None


async def get_current_user(request: Request) -> CurrentUser:
    """
    Get current authenticated user from request state
    Use after JWTBearer dependency
    
    Usage:
        @router.get("/endpoint")
        async def endpoint(
            token: str = Depends(JWTBearer()),
            current_user: CurrentUser = Depends(get_current_user)
        ):
            # current_user.id, current_user.email, etc.
    """
    if not hasattr(request.state, "user"):
        raise HTTPException(
            status_code=401,
            detail="User not authenticated"
        )
    
    return request.state.user


def get_optional_user(request: Request) -> Optional[CurrentUser]:
    """
    Get current user if authenticated, None otherwise
    Use for endpoints that work with or without auth
    """
    if hasattr(request.state, "user"):
        return request.state.user
    return None


# Dependency for protected routes
jwt_bearer = JWTBearer()


def require_auth():
    """
    Dependency that requires authentication
    
    Usage:
        @router.get("/protected", dependencies=[Depends(require_auth())])
        async def protected_endpoint():
            pass
    """
    return Depends(jwt_bearer)


def require_role(allowed_roles: list):
    """
    Dependency that requires specific role(s)
    
    Usage:
        @router.get("/admin-only", dependencies=[Depends(require_role(["admin", "super_admin"]))])
        async def admin_endpoint():
            pass
    """
    async def role_checker(request: Request, token: str = Depends(jwt_bearer)):
        user = request.state.user
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail=f"Access denied. Required roles: {allowed_roles}"
            )
        return user
    
    return Depends(role_checker)


def get_company_filter(current_user: CurrentUser, company_param: Optional[str] = None) -> Optional[str]:
    """
    Get company name filter based on user's company_id or explicit parameter
    
    For multi-tenant data isolation:
    - If company_param provided, use it (for admin users)
    - Otherwise, filter by user's company_id
    
    Usage in controller:
        company_filter = get_company_filter(current_user, company_param)
        if company_filter:
            query += " WHERE company_name = ?"
            params.append(company_filter)
    """
    if company_param:
        return company_param
    
    # In future, map company_id to company_name via TallyBridge API
    # For now, return None (no filter) - will be implemented in Phase 3
    return None
