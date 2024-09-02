from pydantic import ValidationError
from src.sample_api.v1.structs.housing import HousingBase
import pytest


def test_postal_code_correct_format():
    pc = "V6Y 1J2"
    house = HousingBase(postal_code=pc, city="MyCity",
                        street="something", housing_type_id=1, address="134")
    assert house.postal_code == pc


def test_postal_code_lower_case():
    house = HousingBase(postal_code="v6y 1j2", city="MyCity",
                        street="something", housing_type_id=1, address="456")

    assert house.postal_code == "V6Y 1J2"


def test_postal_code_bad_format_zip_code():
    with pytest.raises(ValidationError) as e_info:
        house = HousingBase(postal_code="90210", city="MyCity",
                            street="something", housing_type_id=1, address="34")


def test_postal_code_bad_format_backwards():
    with pytest.raises(ValidationError) as e_info:
        house = HousingBase(postal_code="5T7 V8J", city="MyCity",
                            street="something", housing_type_id=1, address="134")


def test_postal_code_field_set():
    house = HousingBase(postal_code="v6y 1j2", city="MyCity",
                        street="something", housing_type_id=1, address="31A")

    new_pc = "J8J 1T7"
    house.postal_code = new_pc
    assert house.postal_code == new_pc


def test_empty_string_city():
    with pytest.raises(ValidationError) as e_info:
        house = HousingBase(postal_code="5T7 V8J", city=" ",
                            street="something", housing_type_id=1)


def test_empty_string_street():
    with pytest.raises(ValidationError) as e_info:
        house = HousingBase(postal_code="5T7 V8J", city="Something",
                            street=" ", housing_type_id=1)


def test_missing_housing_type_id():
    with pytest.raises(ValidationError) as e_info:
        house = HousingBase(postal_code="5T7 V8J", city="Something",
                            street=" ")
