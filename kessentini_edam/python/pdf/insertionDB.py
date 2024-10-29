import psycopg2

try:
    # Connect to your postgres DB
    print("Connecting to the database...")
    conn = psycopg2.connect(
        host="localhost",
        dbname="stage",
        user="postgres",
        password="5altikalba",
        port=3000
    )
    print("Connection successful!")

    # Open a cursor to perform database operations
    cur = conn.cursor()
    
    # Drop the tables if they exist
    cur.execute("DROP TABLE IF EXISTS individuals;")
    cur.execute("DROP TABLE IF EXISTS entities;")
    
    # Create the individuals table
    cur.execute("""
CREATE TABLE individuals(
    id varchar(9) PRIMARY KEY,
    name varchar,
    name_original_script varchar,
    date_of_birth varchar,
    place_of_birth varchar,
    good_quality_aka varchar,
    low_quality_aka varchar,
    nationality varchar,
    passport_no varchar,
    national_identification_no varchar,
    address varchar,
    listed_on varchar,
    other_information varchar,
    title varchar,
    designation varchar
);
""")
    print("Individuals table created successfully!")

    conn.commit()

    # Copy data into the individuals table
    cur.execute(r"""COPY individuals(id, name, name_original_script, date_of_birth, place_of_birth, good_quality_aka, low_quality_aka, nationality, passport_no, national_identification_no, address, listed_on, other_information, title, designation)
                    FROM 'C:\\Users\\Pc\\Desktop\\python\\pdf\\csv_files\\individuals.csv' 
                    DELIMITER ',' 
                    CSV HEADER
                    ENCODING 'UTF8';""")
    print("Data copied into individuals table successfully!")

    conn.commit()

    # Create the entities table
    cur.execute("""
CREATE TABLE entities(
    id varchar(9) PRIMARY KEY,
    name varchar,
    name_original_script varchar,
    aka varchar,
    fka varchar,
    address varchar,
    listed_on varchar,
    other_information varchar
);
""")
    print("Entities table created successfully!")

    conn.commit()

    # Copy data into the entities table
    cur.execute(r"""COPY entities(id, name, name_original_script, aka, fka, address, listed_on, other_information)
                    FROM 'C:\\Users\\Pc\\Desktop\\python\\pdf\\csv_files\\entities.csv' 
                    DELIMITER ',' 
                    CSV HEADER
                    ENCODING 'UTF8';""")
    print("Data copied into entities table successfully!")

    conn.commit()

except (Exception, psycopg2.DatabaseError) as error:
    print(f"Error: {error}")

finally:
    # Close communication with the database
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()
    print("Connection closed.")
