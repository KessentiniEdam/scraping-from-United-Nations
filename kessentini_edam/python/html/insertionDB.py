import psycopg2

# Connect to your PostgreSQL DB
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

try:
    # Drop the tables if they exist
    cur.execute("DROP TABLE IF EXISTS individualsHTML;")
    cur.execute("DROP TABLE IF EXISTS entitiesHTML;")

    # Create the individuals table
    cur.execute("""
    CREATE TABLE individualsHTML (
        REFERENCE_NUMBER VARCHAR(9) PRIMARY KEY,
        name VARCHAR,
        "NAME_ORIGINAL_SCRIPT" VARCHAR,
        "TITLE" VARCHAR,
        "DESIGNATION" VARCHAR,
        "DOB" VARCHAR,
        "POB" VARCHAR,
        "Good quality a.k.a." VARCHAR,
        "Low quality a.k.a." VARCHAR,
        "NATIONALITY" VARCHAR,
        "Passport no" VARCHAR,
        "National identification no" VARCHAR,
        "Listed on" VARCHAR,
        "Other information" VARCHAR
    );
    """)
    print("Individuals table created successfully!")

    conn.commit()

    # Copy data into the individuals table
    cur.execute("""
    COPY individualsHTML(REFERENCE_NUMBER, name, "NAME_ORIGINAL_SCRIPT", "TITLE", "DESIGNATION", "DOB", "POB", "Good quality a.k.a.", "Low quality a.k.a.", "NATIONALITY", "Passport no", "National identification no", "Listed on", "Other information")
    FROM 'C:\\Users\\Pc\\Desktop\\python\\html\\output\\csv_files\\individuals.csv' 
    DELIMITER ',' 
    CSV HEADER
    ENCODING 'UTF8';
    """)
    print("Data copied into individuals table successfully!")

    conn.commit()

    # Create the entities table
    cur.execute("""
    CREATE TABLE entitiesHTML (
        REFERENCE_NUMBER VARCHAR(9) PRIMARY KEY,
        name VARCHAR,
        "A.k.a." VARCHAR,
        "F.k.a." VARCHAR,
        "Listed on" VARCHAR,
        "Other information" VARCHAR,
        "NAME_ORIGINAL_SCRIPT" VARCHAR
    );
    """)
    print("Entities table created successfully!")

    conn.commit()

    # Copy data into the entities table
    cur.execute("""
    COPY entitiesHTML(REFERENCE_NUMBER, name, "A.k.a.", "F.k.a.", "Listed on", "Other information", "NAME_ORIGINAL_SCRIPT")
    FROM 'C:\\Users\\Pc\\Desktop\\python\\html\\output\\csv_files\\entities.csv' 
    DELIMITER ',' 
    CSV HEADER
    ENCODING 'UTF8';
    """)
    print("Data copied into entities table successfully!")

    conn.commit()

except Exception as e:
    conn.rollback()
    print(f"Error: {e}")

finally:
    # Close communication with the database
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()
    print("Connection closed.")
