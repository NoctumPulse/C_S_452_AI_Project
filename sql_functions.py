from sqlalchemy import create_engine,text, Table, MetaData

def get_connection():
    try:
        user = 'root'
        password = 'admin'
        host = 'localhost'
        port = 3306
        database = "equiprental"
        return create_engine(
            url="mysql://{0}:{1}@{2}:{3}/{4}".format(
                user, password, host, port, database
            )
        )
    except Exception as e:
        print(e)

def setupDatabase(engine):
    dropEquipment = "DROP TABLE IF EXISTS Equipment"
    createEquipmentTable = """
    CREATE TABLE Equipment (
        EquipID VARCHAR(15) PRIMARY KEY,
        Name VARCHAR(30) NOT NULL,
        Manufacturer VARCHAR(30),
        SerialNumber VARCHAR(30),
        ModelNumber VARCHAR(30),
        Manual VARCHAR(20)
    )
    """

    dropUser = "DROP TABLE IF EXISTS User"
    createUserTable = """
    CREATE TABLE User (
        UserID INT AUTO_INCREMENT,
        Name VARCHAR(30) NOT NULL,
        Email VARCHAR(30),
        Phone CHAR(12),
        PRIMARY KEY(UserID)
    )
    """

    dropRental = "DROP TABLE IF EXISTS Rental"
    createRentalTable="""
    CREATE TABLE Rental (
        EquipID VARCHAR(15),
        UserID INT,
        Checkout_Date DATE NOT NULL,
        Due_Date DATE NOT NULL,
        FOREIGN KEY (EquipID) REFERENCES Equipment(EquipID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
        FOREIGN KEY (UserID) REFERENCES User(UserID)
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
        PRIMARY KEY (EquipID, UserID)
    )
    """

    with engine.connect() as conn:
        conn.execute(text(dropRental))
        conn.execute(text(dropEquipment))
        conn.execute(text(dropUser))
        conn.execute(text(createEquipmentTable))
        conn.execute(text(createUserTable))
        conn.execute(text(createRentalTable))
        conn.commit()

def insertData(engine):
    equipments = [
        {'EquipID': 'item1', 'Name': 'Shovel', 'Manufacturer': 'Harbor Feight', 'SerialNumber': '123j45j', 'ModelNumber': 'as23das31w4',  'Manual': 'SH98'},
        {'EquipID': 'item2', 'Name': 'Wrench', 'Manufacturer': 'Dewalt', 'SerialNumber': '89yhanid', 'ModelNumber': 'iuhbg679opklj',  'Manual': 'W845'},
        {'EquipID': 'item3', 'Name': 'Hammer', 'Manufacturer': 'HammerCo', 'SerialNumber': 'jky87ughi90', 'ModelNumber': 'awe12398ijad',  'Manual': 'HM75'},
        {'EquipID': 'item4', 'Name': 'Dolly', 'Manufacturer': 'HeavyLifterLLC', 'SerialNumber': 'asd79yhijk8ui', 'ModelNumber': 'asd90oiqewedsf',  'Manual': 'DOLLY1'}       
    ]

    users = [
        {'Name': "John Doe", 'Email':'john_doe@gmail.com', 'Phone': '397-803-9845'},
        {'Name': "Mary Jane", 'Email':'mjay@aol.com', 'Phone': '635-190-8293'},
        {'Name': "Lucy Grey", 'Email':'snow_girl@yahoo.com', 'Phone': '978-142-0917'},
        {'Name': "Sofie Field", 'Email':'sofie675@outlook.com', 'Phone': '738-601-3928'},
    ]

    rentals = [
        {'EquipID': 'item1', 'UserID': 1, 'Checkout_Date': '2024-10-05', 'Due_Date': '2024-10-15'},
        {'EquipID': 'item3', 'UserID': 2, 'Checkout_Date': '2024-10-05', 'Due_Date': '2024-10-20'}
    ]

    metadata1 = MetaData()
    equipment_table = Table("Equipment", metadata1, autoload_with=engine)
    metadata2 = MetaData()
    user_table = Table("User", metadata2, autoload_with=engine)
    metadata3 = MetaData()
    rental_table = Table("Rental", metadata3, autoload_with=engine)
    with engine.connect() as conn:
        conn.execute(equipment_table.insert(), equipments)
        conn.execute(user_table.insert(), users)
        conn.execute(rental_table.insert(), rentals)
        conn.commit()

def executeSQLQuery(engine, query):
    with engine.connect() as conn:
        try:
            result = conn.execute(text(query))
            resultString = ""
            for row in result:
                resultString += (str(row) + "\n")
            return resultString
        except Exception as e:
            #print ("Query failed with exception\n" + str(e))
            return None