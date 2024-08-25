# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

### Endpoint Documentation

`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: A JSON object that returns a success boolean of value True and a dictionary of `categories` with keys corresponding to ID.

```json
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "success": true
}
```

`GET '/questions'`

- Fetches a dictionary of categories, list of questions paginated in blocks of 10 results, a success boolean of value True and the total # of questions in the bank.
- Request Arguments: 
    - `page` - Desired page for query. Default: `1`.
- Expected Errors:
    - `404` if page not found.
- The `categories` dictionary has keys corresponding to ID.
- The `questions` list contains `question` objects with fields `answer`, `category`, `difficulty`, `id`, and `question`.

```json
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": null,
    "questions": [
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
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
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
        },
        {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        },
        {
            "answer": "Mona Lisa",
            "category": 2,
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
        },
        {
            "answer": "One",
            "category": 2,
            "difficulty": 4,
            "id": 18,
            "question": "How many paintings did Van Gogh sell in his lifetime?"
        }
    ],
    "success": true,
    "total_questions": 16
}
```

`DELETE '/questions/<int:question_id>'`

- Deletes a question provided applicable question id.
- Request Arguments:
    - `question_id` - `int`, value corresponding to the desired question ID to delete.
- Expected Errors:
    - `404` if question not found.
- Returns: A JSON object that returns a success boolean of value True and a `deleted` value corresponding to the deleted ID.

```json
{
    "deleted": 9,
    "success": true
}
```

`POST '/questions'`

- Creates a question given an input JSON.
- Request Arguments: (all in an input JSON)
    - `question` - String containing the question.
    - `category` - `1` - `6`. Category the question belongs to.
    - `difficulty` - Numerical value denoting question difficulty from `1` - `5`.
    - `answer` - String denoting question answer.
- Expected Errors:
    - `404` if question not found.
    - `400` if badly formatted input JSON.
    - `500` if an error occurs server-side, i.e. you input a garbage value like @ or a string for the category.
- Returns: A JSON object with fields corresponding to the question parameters along with a success boolean of value True.

```json
{
    "answer": "a broken pencil has no point",
    "category": 3,
    "created": 26,
    "difficulty": 1,
    "question": "what time is your name",
    "success": true
}
```

`POST '/questions/search'`

- Queries questions based on a search term provided in an input JSON.
- Request Arguments: (all in an input JSON)
    - `searchTerm` - The string (can be partial string) to search question text for query.
- Expected Errors:
    - `404` if question not found.
    - `400` if no search term provided
    - `500` for server-side error
- Returns: A JSON object with fields corresponding to the current category along with a list of questions objects that fit a partial string match for query as well as a success boolean of value True and the total questions fetched by the query.

```json
{
    "current_category": null,
    "questions": [
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
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
        }
    ],
    "success": true,
    "total_questions": 7
}
```

`GET '/categories/<int:category_id>/questions'`

- Queries all questions corresponding to a given category.
- Request Arguments: (all in an input JSON)
    - `category_id` - `int`, category ID to query questions from. `1` - `6`.
- Expected Errors:
    - `404` if category not found.
    - `500` if an error occurs server-side.
- Returns: A JSON object with fields corresponding to the current category along with a list of questions objects under that category.

```json
{
    "current_category": "Science",
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
        },
        {
            "answer": "Mitochondria",
            "category": 1,
            "difficulty": 5,
            "id": 24,
            "question": "What is the powerhouse of the cell"
        },
        {
            "answer": "a",
            "category": 1,
            "difficulty": 5,
            "id": 25,
            "question": "a"
        }
    ],
    "success": true,
    "total_questions": 5
}
```

`POST '/quizzes'`

- Play the quiz.
- Request Arguments: (all in an input JSON)
    - `quiz_category` - {"id": <int>, "type": <str>}, note that type must match the id per normal categories query. ID `0` means all categories.
    - `previous_questions` - [<int>, <int>, ...], comma-separated list of question IDs.
- Expected Errors:
    - `400` if category or previous questions were not provided.
- Returns: A JSON object with a success boolean of value True and a randomly selected question object from the relevant bank.

```json
{
    "question": {
        "answer": "Blood",
        "category": 1,
        "difficulty": 4,
        "id": 22,
        "question": "Hematology is a branch of medicine involving the study of what?"
    },
    "success": true
}
```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
