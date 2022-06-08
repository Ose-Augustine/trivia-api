 # A Trivia App  

 This project is a trivia web application. Users are able to seek questions by category, And also hane the opportunity to reveal the answers to the questions they are unsure of. Players can decide rather than seeing the entire list of questions which already have been paginated 10 per page, they can play in a quiz format where one question would be shown at a time . This is my seconde project for the udacity nanodegree programme. By completing this project, I have created and mastered my api structuring skills as well as Test Driven Development(TDD) using flask and Unittest


 ## Guidlines 

 The UI should be pretty easy to interact with once the app is run. It is designed that every feature defines itself. 

 ## Getting Started  

 ### Pre-requisites and Local Development 
 Developers using this project should already have Python3, pip and node installed on thier local machines. This project is divided into to main parts .
 1. Frontend 
 2. Backend  

 #### Frontend 
  
  The frontend is built using the reactjs framework. To run the app. cd into the frontend folder and run _npm install_ then _npm start_. It automatically runs on localhost:3000.

  #### Backend
  Enter into the backend folder. To populate your local database with the data the app works on, run psql _'your db'_ < trivia.psql.

  To run the applcation, run the following commands:
  ``` 
  export FLASK_APP=flaskr
  export FLASK_ENV=development
  flask run 
  ``` 
  These commands will set the application to developement environment and poits to the `__init__.py`file in teh flaskr folder . The application is run on localhost:5000 by default and is proxy for the frontend. Make sure to run the backend before the frontend to avoid errors .

  ## API Reference 

  ### Getting Started 
  * Base URL : At present, this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default localhost:5000.
  * Authentication: This version of the application does not require atuthentication or API keys.

  ### Error Handling 
  Errors are returned as JSON objects in the following format:
  ```
  {
      "success":False,
      "error": 404,
      "messsage": "Resource not found"
  }
  ``` 
  The API will return four error types when requests fail:
  * 404: Resource Not Found
  * 405: Method Not Allowed 
  * 422: Unprocessed
  * 500: Server could not resolve.

  ### Endpoints 
  #### GET /categories 
- General:
    - Returns a list of all the categories and id's pairs covered in the app.
- Sample: `curl https://127.0.0.1:5000/categories`

```{
    "categories":[
        "1":"Science",
        "2":"Art",
        "3":"Geography",
        "4":"History",
        "5":"Entertainment",
        "6":"Sports"
    ]
}
```

#### GET /questions 
- General
    - Returns a list of questions objects, total questions and categories in the page
    - Results are paginated in groups of 10. You can inclued a page number to start from, the default is 1.
- Sample : `curl https://127.0.0:5000/questions` . Defaults to page one
- Sample : `curl https://127.0.0:5000/questions?page=2`. Starts from page 2 

```{
      "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ], 
  "totalQuestions": 10

}
```
#### POST /questions 
- General:
    - The post method on this route behaves differently depending on the json body sent to it . It looks for either a `searchTerm` key in which case it returns all the questions where the term exists, or if the `searchTerm` key is absent, it knows to create new questions to persist in the database .
    - Reurns a list of questions, the categoryies and the total number of questions that match.
- Sample : `curl https://127.0.0.1:5000/questions -X POST -H "Content-Type:application/json" -d '{"searchTerm":"young"}'`
```{
    "currentCategory": 5, 
  "questions": [
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ], 
  "totalQuestions": 1

}
```
- Sample : `curl https://127.0.0.1:5000/questions -X POST -H "Content-Type:application/json" -d'{"question":"Who is the secretary general of the UN","answer":"Antonio Guterres","difficulty":3,"category":"Arts"`. **This sample does not return any new data but rather creates the question**

#### GET /categories/{int:id}/questions
- General:
    - Returns a list of question objects, currentCategory and total number of questions in the category having the specified id.
- Sample : `curl https://127.0.0.1:5000/categories/1/questions`

```{

  "currentCategory": "Science", 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ], 
  "totalQuestions": 3

}
```

#### DELETE /questions/{int:id}
- General:
   -Deletes the question of the given id if it exists. Does not return any data.
- Sample : `curl https://127.0.0.1:5000/questions/1 -X DELETE`

#### POST /quizzes 
- General:
    - Expects a json having keys of **previous_questions** _a list of the previous questions id_ and **quiz_category** _a string of the current category_ Returns a single questions object whose id is not in the list of previous_questions.
- Sample : `curl https://127.0.0.1:5000/quizzes -X POST -H 'Content-Type:application/json' -d'{"previous_questions":[9,5,12]"current category":"Arts"}`

```{
    "question": {
    "answer": "Apollo 13", 
    "category": 5, 
    "difficulty": 4, 
    "id": 2, 
    "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
  }

}
```

### Note 

While making use of the api, take not of case sensitivity as a search term of _young_ is not the same as _Young_ and so would return unexpected results.

## Authors 
Yours truly, Oserebameh Beckley.

## Acknoledgements 
The entire frontend of this project was provided to me by the Udacity team . This project is a requirement for my completion of the full stack nanodegree program. While I am conversant with the basis of html, css and javascript, this project frontend was built by udaciy using the react.js framework and is currently beyond my knowledge scope. The rest of the backend, apis and tests were written by me .