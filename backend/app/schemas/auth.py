from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    phone: str = Field(min_length=10, max_length=20)
    password: str = Field(min_length=6, max_length=128)
    language: str = Field(default="en", pattern="^(en|ta)$")


class LoginRequest(BaseModel):
    phone: str
    password: str


class UserResponse(BaseModel):
    id: str
    full_name: str
    phone: str
    language: str

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
