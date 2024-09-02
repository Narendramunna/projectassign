from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from ...db import sessions
from ..repository.housing_type_repository import housingTypeRepository
from ..structs.housing_type import HousingType
from sqlalchemy.orm import Session


router = APIRouter()


@router.get("/", response_model=List[HousingType])
def get_all_housing_types(
        db: Session = Depends(sessions.get_db),
        skip: int = 0,
        limit: int = 100
) -> Any:
    """
    Retrieve Housing Types
    """
    housing_types = housingTypeRepository.get_multi(db, skip=skip, limit=limit)
    return [HousingType(housing_type_id=housing_type.id, code=housing_type.code, description=housing_type.description) for housing_type in housing_types]


@router.get("/{code}", response_model=HousingType)
def get_housing_type_code(
        db: Session = Depends(sessions.get_db),
        *,
        code: str
) -> Any:
    """
    Get HousingType By Type code.
    """

    db_object = housingTypeRepository.get_by_code(db, code=code)
    if not db_object:
        raise HTTPException(
            status_code=404, detail="No HousingType for this code")

    ret_val = HousingType(housing_type_id=db_object.id,
                          code=db_object.code, description=db_object.description)
    return ret_val
