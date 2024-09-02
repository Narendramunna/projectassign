from typing import Any, List
import logging

from fastapi import APIRouter, Depends, HTTPException
from ...db import sessions
from ..models.models import Housing as HousingModel
from ..repository.housing_repository import housingRepository
from ..structs.housing import Housing, HousingBase
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import ForeignKeyViolation

router = APIRouter()

logger = logging.getLogger('uvicorn.error')


@router.get("/{postal_code}", response_model=List[Housing])
def get_housing_in_postal_code(
        db: Session = Depends(sessions.get_db),
        *,
        postal_code,
        skip: int = 0,
        limit: int = 100

) -> Any:
    """
    Get Houses with postal code
    """

    housing = housingRepository.get_by_postal_code(
        db, postal_code=postal_code, skip=skip, limit=limit)

    if not housing:
        raise HTTPException(
            status_code=404, detail="No homes found with the given postal code")

    return [
        Housing(
            address=house.address,
            street=house.street,
            city=house.city,
            postal_code=house.postal_code,
            housing_id=house.id,
            housing_type_id=house.housing_type_id,
        )
        for house in housing
    ]


@router.post("/", response_model=Housing)
def create_house(
        *,
        db: Session = Depends(sessions.get_db),
        input: HousingBase
) -> Any:
    """
    Create new house.
    """
    db_obj = HousingModel(
        address=input.address,
        street=input.street,
        city=input.city,
        postal_code=input.postal_code,
        housing_type_id=input.housing_type_id
    )
    try:
        saved_object = housingRepository.create(db, obj_in=db_obj)
        new_house = Housing(
            address=saved_object.address,
            street=saved_object.street,
            city=saved_object.city,
            postal_code=saved_object.postal_code,
            housing_id=saved_object.id,
            housing_type_id=saved_object.housing_type_id,
        )

        return new_house
    except IntegrityError as ie:
        db.rollback()
        if isinstance(ie.orig, ForeignKeyViolation):
            logger.debug("Foreign key exception")
            raise HTTPException(
                status_code=422, detail="Invalid housing_type_id")
        else:
            raise ie
    except Exception as e:
        db.rollback()
        raise e
