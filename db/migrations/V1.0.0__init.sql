CREATE SCHEMA IF NOT EXISTS housing;
SET SEARCH_PATH TO housing;
CREATE SEQUENCE IF NOT EXISTS "housing_type_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE;
CREATE SEQUENCE IF NOT EXISTS "housing_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE;

CREATE TABLE "housing_types"
(
    id          INTEGER PRIMARY KEY DEFAULT nextval('housing_type_id_seq'),
    code        CHAR(3) NOT NULL UNIQUE,
    description VARCHAR(50) NOT NULL
);

CREATE TABLE "housing"
(
    id              INTEGER PRIMARY KEY DEFAULT nextval('housing_id_seq'),
    address         VARCHAR(50) NOT NULL,
    street          VARCHAR(50) NOT NULL,
    city            VARCHAR(50) NOT NULL,
    postal_code     CHAR(7) NOT NULL,
    housing_type_id INTEGER NOT NULL,
    CONSTRAINT fk_housing_type
      FOREIGN KEY(housing_type_id) 
        REFERENCES housing_types(id)
);
INSERT INTO housing.housing_types (code, description)
VALUES ('SFD', 'Single Family Housing'),
       ('ASL', 'Assisted Living'),
       ('MFD', 'Multi Family Housing'),
       ('COP', 'Co-Op Housing');
