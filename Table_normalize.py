import sqlite3
con = sqlite3.connect("adata_sqlite_erd.db")

cursor = con.cursor()

cursor.execute("""CREATE TABLE Organizations (
    ID INT PRIMARY KEY,
    Organization_Name VARCHAR(255),
    Full_Name VARCHAR(255),
    Territory VARCHAR(255),
    IIN VARCHAR(255)
)
            """)

cursor.execute("""CREATE TABLE Court_Decisions (
    Decision_ID INT PRIMARY KEY,
    Organization_ID INT,
    Decision_Date DATE,
    Decision_Number VARCHAR(255),
    FOREIGN KEY (Organization_ID) REFERENCES Organizations(ID)
)
            """)

cursor.execute("""CREATE TABLE Registration_History (
    Event_ID INT PRIMARY KEY,
    Organization_ID INT,
    Registration_Date DATE,
    Deregistration_Date DATE,
    FOREIGN KEY (Organization_ID) REFERENCES Organizations(ID)
)
            """)