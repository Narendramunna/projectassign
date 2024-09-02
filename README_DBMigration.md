## API Environment Setup
Setting up a test environment for the API involves several steps, from replicating the production database schema and data to ensuring the environment is properly configured. Here’s a detailed approach to achieve this:

1. Set Up the Database Schema
    - Create a Schema and Sequences: Ensure that the schema and sequences in the test environment match those in the production environment. The below script have to be executed in the test DB

```sql
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
Create Tables: Create tables in the test environment as per the provided schema:
```
```sql
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
```
2. Populate Initial Data
We need to populate the housing_types table with the initial data:

```sql
INSERT INTO housing.housing_types (code, description)
VALUES ('SFD', 'Single Family Housing'),
       ('ASL', 'Assisted Living'),
       ('MFD', 'Multi Family Housing'),
       ('COP', 'Co-Op Housing');
```
3. Data Migration
    - For large datasets like housing, ownership, and owners, follow these steps:

    - Export Data from Production: Use PostgreSQL tools like pg_dump to export data from the production database. For example:

```bash
pg_dump -U user -h production_host -d database -t housing -F c -f housing_dump.backup
pg_dump -U user -h production_host -d database -t ownership -F c -f ownership_dump.backup
pg_dump -U user -h production_host -d database -t owners -F c -f owners_dump.backup
```
    - Transfer Dumps to Test Environment: Transfer the dump files to the OpenShift environment where the test database is set up. We can use scp, rsync, or any other secure transfer method.

    - Import Data to Test Database: Restore the data into the test environment using pg_restore:

```bash
pg_restore -U user -h test_host -d test_database -F c -v housing_dump.backup
pg_restore -U user -h test_host -d test_database -F c -v ownership_dump.backup
pg_restore -U user -h test_host -d test_database -F c -v owners_dump.backup
```

4. Adjust Configuration
    -  Update Connection Details: Ensure that the API and any other applications point to the new test database. Update connection strings and credentials as needed.

    - Review Performance Settings: With large datasets, performance settings such as indexing, query optimization, and resource allocation might need adjustments. Verify that the test environment is configured to handle the expected load.

5. Testing and Validation
    - Verify Data Integrity: Check that the data in the test environment matches the production data. Run queries and compare counts, data samples, and referential integrity.

    -  Functional Testing: Run API tests to ensure that the application behaves as expected with the data in the test environment. This includes CRUD operations, querying, and any business logic related to housing data.

    - Performance Testing: Simulate load and performance tests to ensure the system behaves under stress, similar to the production environment.

6. Documentation and Cleanup
    - Document the Process: Maintain clear documentation of the setup process, including any deviations from the production schema or data, for future reference.