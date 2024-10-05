# C_S_452_AI_Project

This project models a database for an equipment rental store which tracks equipment, users, and rentals.

## Model Picture

![image](/sql_model.png)

## Sample Question Output 1
Strategy was single_domain_double_shot
Question was 'Which user has rented the hammer?'
Result was:

SELECT u.Name
FROM User AS u
JOIN Rental AS r ON u.UserID = r.UserID
JOIN Equipment AS e ON r.EquipID = e.EquipID
WHERE e.Name = 'Hammer';

Query results were:
('Mary Jane',)

Friendly response is:
Certainly! Mary Jane is the user who has rented the hammer.

## Sample Question Output 2
Strategy was zero_shot
Question was 'Who has rented an equipment named shovel?'
Result was:

SELECT u.Name
FROM User u
JOIN Rental r ON u.UserID = r.UserID
JOIN Equipment e ON r.EquipID = e.EquipID
WHERE e.Name = 'shovel';

Query results were: 
('John Doe',)

Friendly response is:
Sure! According to the information provided, John Doe is the person who has rented a shovel.

## Discussion
I tried the zero shot and the single domain strategies. I didn't see any notable differences in my queries but maybe with a more complex model and queries I would see some variance in capabilities. The main file contains 8 questions and their output from chatgpt
