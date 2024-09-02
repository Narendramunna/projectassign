from pydantic import ConfigDict, BaseModel


class HousingTypeBase(BaseModel):
    code: str
    description: str


class HousingType(HousingTypeBase):
    housing_type_id: int


class HousingTypeInDBBase(HousingTypeBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
