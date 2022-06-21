## API Reference

### Getting Started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling

Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable


### Endpoints

#### GET /categories
- General:
    - This endpoint returns question categories (category id and type)
- Sample: curl http://localhost:5000/categories

- Response:
    ```
    {
        "categories": {
            "1": "Science",
            "2": "Art",
            "3": "Geography",
            "4": "History",
            "5": "Entertainment",
            "6": "Sports"
        }
    }
    ```

#### GET /questions
- General:
    - This endpoint returns list of questions, number of total questions, current category, categories
    - Results are paginated in groups of 8. Include a request argument (page) to choose page number, starting from and defaults to 1
- Sample: curl http://localhost:5000/questions?page=2

- Response:
    ```
    {
        "categories": {
            "1": "Science",
            "2": "Art",
            "3": "Geography",
            "4": "History",
            "5": "Entertainment",
            "6": "Sports"
        },
        "currentCategory": null,
        "questions": [
            {
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
            },
            {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
            },
            {
            "answer": "Mona Lisa",
            "category": 2,
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
            },
            {
            "answer": "Jackson Pollock",
            "category": 2,
            "difficulty": 2,
            "id": 19,
            "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
            },
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
            },
            {
            "answer": "Scarab",
            "category": 4,
            "difficulty": 4,
            "id": 23,
            "question": "Which dung beetle was worshipped by the ancient Egyptians?"
            },
            {
            "answer": "Jubril Abdulsalam",
            "category": 4,
            "difficulty": 1,
            "id": 24,
            "question": "What is your Name"
            },
            {
            "answer": "20",
            "category": 4,
            "difficulty": 2,
            "id": 25,
            "question": "How old are you"
            }
        ],
        "totalQuestions": 29
    }
    ```

#### DELETE /questions/question_id
- General:
    - This endpoint deletes question using question id
- Sample: curl -X DELETE http://localhost:5000/questions/32
- Response:
    ```
    {
        "id": 32,
        "deleted": True
    }
    ```

#### POST /questions/search
- General:
    - This endpoint gets questions based on a search term
    - It return any questions for whom the search term is a substring of the question.
- Sample: curl -X POST -H "Content-type: application/json" --data "{\"searchTerm\": \"title\"}" http://localhost:5000/questions/search
- Response:
    ```
    {
        "currentCategory": null,
        "questions": [
            {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
            },
            {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
            }
        ],
        "totalQuestions": 2
    }
    ```

#### POST /questions
- General:
    - This endpoint adds a new question, It requires the question and answer text, category, and difficulty score.
- Sample: curl -X POST -H "Content-type: application/json" --data "{\"question\":\"Heres a new question\",\"answer\":\"Heres a new answer\",\"difficulty\":4,\"category\":2}" http://localhost:5000/questions
- Response:
    ```
    {
        "success": true
    }
    ```

#### GET /categories/<category_id>/questions
- General:
    - This endpoint gets questions based on category, it returns name of category with id specified,
        question in the category, total number of questions in the category
- Sample: curl http://localhost:5000/categories/1/questions
- Response:
    ```
    {
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

#### POST /quizzes
- General:
    - This endpoint gets questions to play the quiz.
    - It takes category and previous question parameters and return a random questions within the given category which is not one of the previous questions.
- Sample: curl -X POST -H "Content-Type: application/json" --data "{\"quiz_category\": {\"type\": \"science\", \"id\": 1}, \"previous_questions\":[20]}" http://localhost:5000/quizzes
- Response:
    ```
    {
        "question": {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
        }
    }
    ```