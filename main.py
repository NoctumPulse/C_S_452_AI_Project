from sql_functions import get_connection, setupDatabase, insertData, executeSQLQuery
from openai import OpenAI
from ai_functions import single_shot_sql, single_domain_double_shot_sql, friendlyResponse
import os

def main():
    engine = get_connection()
    print("CONNECTION SUCCESSFUL")
    setupDatabase(engine)
    insertData(engine)
    openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    questions = [('zero_shot', 'Who has rented an equipment named shovel?'),
     ('single_domain_double_shot', 'What is the phone number of Mary Jane?'),
     ('zero_shot', 'How would I insert a new user who is named John Smith whose phone and email are 563-545-8712 and john@gmail.com?'),
     ('single_domain_double_shot', 'What would inserting a new equipment look like?'),
     ('zero_shot', 'How would I get a list of all rentals with their corresponding user emails?'),
     ('single_domain_double_shot', 'Which users do not have any rentals?'),
     ('zero_shot', 'How many equipment items are in the database?'),
     ('single_domain_double_shot', 'Which user has rented the hammer?')]
    for question in questions:
        if question[0] == 'zero_shot':
            result = single_shot_sql(openai, question[1])
            print("Strategy was zero_shot")
            print("Question was '" + question[1] + "'")
            print("Result was:")
            print(result)
            queryResult = executeSQLQuery(engine, result)
            if queryResult != None:
                print("Query results were: ")
                print(queryResult)
                print("Friendly response is: ")
                print(friendlyResponse(openai, question[1], queryResult))
            else:
                print("Friendly response is: ")
                print(friendlyResponse(openai, question[1], result))

        elif question[0] == 'single_domain_double_shot':
            result = single_domain_double_shot_sql(openai, question[1])
            print("Strategy was single_domain_double_shot")
            print("Question was '" + question[1] + "'")
            print("Result was:")
            print(result)
            queryResult = executeSQLQuery(engine, result)
            if queryResult != None:
                print("Query results were: ")
                print(queryResult)
                print("Friendly response is: ")
                print(friendlyResponse(openai, question[1], queryResult))
            else:
                print("Friendly response is: ")
                print(friendlyResponse(openai, question[1], result))

        else:
            print("ERROR")
            break

        print("\n\n")
    return 0

if __name__ == '__main__':
    main()