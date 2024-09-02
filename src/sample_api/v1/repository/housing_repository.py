from typing import Optional

from sqlalchemy import Row
from sqlalchemy.orm import Session
from ..structs.housing import HousingBase, Housing as HousingUpdate
from ..models.models import Housing
from .repository import BaseRepository


class HousingRepository(BaseRepository[Housing, HousingBase, HousingUpdate]):
    def get_by_postal_code(self, db: Session, *, postal_code: str, skip: int = 0, limit: int = 100) -> list[Row[Housing]]:
        return db.query(Housing).filter(Housing.postal_code == postal_code).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: HousingBase) -> Housing:
        db_obj = Housing(
            address=obj_in.address,
            street=obj_in.street,
            city=obj_in.city,
            postal_code=obj_in.postal_code,
            housing_type_id=obj_in.housing_type_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


housingRepository = HousingRepository(Housing)
