from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UserProfile(BaseModel):
    # username: str
    username: str = Field(pattern=r"^[a-zA-Z0-9_]{3,20}$", description="Буквы, цифры и '_'")
    password: str = Field(min_length=8, description="Password must be at least 8 characters long")
    email: EmailStr

    model_config = ConfigDict(
        json_schema_extra= {
            "example": {
                "username": "john_doe",
                "password": "securePassword123",
                "email": "john_doe@example.com",
                        }
                            }
                              )

# Пример создания пользователя
user_profile = UserProfile(username="john_doe", password="securePassword123", email="john_doe@example.com")
print(user_profile)