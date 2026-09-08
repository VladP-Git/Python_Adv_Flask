from pydantic import BaseModel, EmailStr, ValidationError


class Address(BaseModel):
    house_number: str
    street: str
    city: str


class User(BaseModel):
    id: int
    name: str
    age: int
    email: EmailStr
    is_active: bool = True
    address: Address


# addr_1 = Address(city='NY', street='San Francisco', house_number='10')
# user_1 = User(id=1, name='John', age=20, is_active=True, address=addr_1, email='example@gmail.com')
# print(user_1)


json_string = """{
    "id": 1,
    "name": "John Doe",
    "age": 22,
    "email": "john.doe@example.com",
    "is_active": 0,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": "123"
    }
}"""


try:
    user = User.model_validate_json(json_string, strict=False)
    print(user)
    user.age += 10
    res = user.model_dump_json()
    print(res)
except ValidationError as e:
    print(f'Validation Error {e}')












