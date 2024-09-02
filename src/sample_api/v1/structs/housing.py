from pydantic import BaseModel, ConfigDict, field_validator
from .housing_type import HousingType
import re


class HousingBase(BaseModel):
    address: str
    street: str
    city: str
    postal_code: str
    housing_type_id: int

    @field_validator('postal_code')
    @classmethod
    def valid_postal_code(cls, v: str) -> str:
        if not re.match(r'^[A-Za-z]\d[A-Za-z] \d[A-Za-z]\d$', v):
            raise ValueError('Invalid postal code format')
        return v.upper()


class Housing(HousingBase):
    housing_id: int


class HousingVerbose(Housing):
    housing_type: HousingType


class HousingInDBBase(HousingBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
