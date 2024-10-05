from openai import OpenAI

sqlSetUp = """
CREATE TABLE Equipment (
    EquipID VARCHAR(15) PRIMARY KEY,
    Name VARCHAR(30) NOT NULL,
    Manufacturer VARCHAR(30),
    SerialNumber VARCHAR(30),
    ModelNumber VARCHAR(30),
    Manual VARCHAR(20)
);
CREATE TABLE User (
    UserID INT AUTO_INCREMENT,
    Name VARCHAR(30) NOT NULL,
    Email VARCHAR(30),
    Phone CHAR(12),
    PRIMARY KEY(UserID)
);
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
);
"""

double_shot_example = ("Who has the hammer rented?\n" 
                       + "SELECT Name from User WHERE UserID = (SELECT UserID FROM Rental WHERE EquipID = (SELECT EquipID from Equipment WHERE Name = 'Hammer'))")

sqlOnlyRequest = "Give me a proper MySQL response that answers the following question. Only respond with MySQL syntax"

def single_shot_sql(ai: OpenAI, question):
    input = sqlSetUp + "\n\n" + sqlOnlyRequest + "\n\n" + question
    completion = ai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role":"user",
                "content": input
            }
        ]
    )
    result = completion.choices[0].message.content
    return scrapeSQL(result)

def single_domain_double_shot_sql(ai, question):
    input = sqlSetUp + "\n\n" + double_shot_example + "\n\n" + sqlOnlyRequest + "\n\n" + question
    completion = ai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role":"user",
                "content": input
            }
        ]
    )
    result = completion.choices[0].message.content
    return scrapeSQL(result)

def scrapeSQL(resultString):
    #print(result)
    sqlStart = "```sql"
    sqlEnd = "```"
    result = ""
    if sqlStart in resultString:
        result = resultString.split(sqlStart)[1]
        #print(result)
    if sqlEnd in result:
        result = result.split(sqlEnd)[0]
        #print(result)
    return result

def friendlyResponse(ai, question, results):
    input = "I asked a question \"" + question + "\" and the results were \"" + results + "\". Can you give me a concise, friendly summary?"
    completion = ai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role":"user",
                "content": input
            }
        ]
    )
    result = completion.choices[0].message.content
    return result