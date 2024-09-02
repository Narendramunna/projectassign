from typing import Optional

from sqlalchemy.orm import Session
from ..structs.housing_type import HousingTypeBase, HousingType as HousingTypeUpdate
from ..models.models import HousingType
from .repository import BaseRepository


class HousingTypeRepository(BaseRepository[HousingType, HousingTypeBase, HousingTypeUpdate]):
    def get_by_code(self, db: Session, *, code: str) -> Optional[HousingType]:
        return db.query(HousingType).filter(HousingType.code == code).first()


housingTypeRepository = HousingTypeRepository(HousingType)
