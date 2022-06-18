import os
import unittest
import json
import random
from urllib import response
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

"""CHANGE below code to get info from enviroment """
database_name = os.getenv('TEST_DB_NAME')
database_password = os.getenv('DB_PASSWORD')
database_host = os.getenv('DB_HOST')
database_username = os.getenv('DB_USER')
database_path = 'postgres://{}:{}@{}/{}'.format(database_username, database_password, database_host, database_name)

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = database_path
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        """test /categories endpoint"""
        response = self.client().get('/categories')
        self.assertEqual(response.status_code, 200)

    def test_get_questions(self):
        """test /questions endpoint"""
        response = self.client().get('/questions?page=1')
        self.assertEqual(response.status_code, 200)

        response = self.client().get('/questions?page=5')
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 422)
        self.assertEqual(json_response["Additional info"], "page index out of range")

    def test_delete_question(self):
        """test DELETE /questions/<int:question_id>"""
        random_question = random.choice(Question.query.all()).id 
        print ("++++++++++++++++++++>>>>>>>>>>>>>>>>" + str(random_question))

        response = self.client().delete('/questions/' + str(random_question))
        question_deleted = Question.query.get(random_question)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(question_deleted == None)

        response = self.client().delete('/questions/' + str(random_question))
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 422)
        self.assertEqual(json_response['Additional info'], "question with id does not exist")

    def test_post_question(self):
        """test add question and search questions"""
        response = self.client().post('/questions', json={
            "question": "Heres a new question string",
            "answer": "Heres a new answer string",
            "difficulty": 1,
            "category": 3
        })
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)

        response = self.client().post('/questions', json={
            "searchTerm": "this is the term the user is looking for"
        })
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)

        response = self.client().post('/questions',  json={
            "question": "Heres a new question string",
            "difficulty": 1,
            "category": 3
        })
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 422)
        self.assertEqual(json_response['Additional info'], 'incomplete data')

        response = self.client().post('/questions',  json={
            "difficulty": 1,
            "category": 3
        })
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 422)
        self.assertEqual(json_response['Additional info'], 'post request to /questions should contain either searchTerm or Question')

    def test_get_category_questions(self):
        """test get questions in a category"""
        response = self.client().get('/categories/1/questions')
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response['currentCategory'], 'Science')
        
        response = self.client().get('/categories/10000/questions')
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 422)
        self.assertEqual(json_response['Additional info'], 'category with id not found')

    #def test_post_quizzes(self):
        """test post quizzes"""

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()