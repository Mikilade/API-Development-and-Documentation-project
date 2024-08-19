import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = "trivia_test"
        self.database_path = f'postgresql+psycopg2://postgres:Biosphere4212!@localhost:5432/{self.database_name}'
        
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path
        })

        self.client = self.app.test_client

    
    def tearDown(self):
        """Executed after reach test"""
        pass
    
    def test_get_categories(self):
        """Test the GET /categories endpoint"""
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(data['categories'], None)

    def test_get_questions(self):
        """Test the GET /questions endpoint"""
        res = self.client().get('/questions?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(data['questions'], None)
        self.assertNotEqual(data['categories'], None)
    
    def test_get_questions_bad_page_index(self):
        """Test the GET /questions endpoint for a bad page index"""
        res = self.client().get('/questions?page=10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_question_not_found(self):
        """Test the DELETE /questions endpoint for a bad page index"""
        res = self.client().delete('/questions/100000') # nonsense extremely high question query
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
    
    def test_add_question_wrong_format(self):
        """Test the POST /questions endpoint for a badly formatted request in the JSON"""
        res = self.client().post('/questions', json={
            "question": "What day is Taco Tuesday?",
            "answer": "Tuesday",
            "category": 3,
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_create_and_delete_new_question(self):
        """Test the POST and DELETE /questions endpoint"""
        # test post
        res = self.client().post('/questions', json={
            "question": "What day is Taco Tuesday?",
            "answer": "Tuesday",
            "category": 3,
            "difficulty": 2
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question'], "What day is Taco Tuesday?")
        self.assertEqual(data['answer'], "Tuesday")
        self.assertEqual(data['category'], 3)
        self.assertEqual(data['difficulty'], 2)

        # test delete
        res2 = self.client().delete(f'/questions/{data['created']}')
        data2 = json.loads(res2.data)
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(data2['success'], True)
        self.assertEqual(data2['deleted'], data['created'])
    
    def test_search_questions(self):
        """Test the POST /questions/search endpoint"""
        # test post
        res = self.client().post('/questions/search', json={
            "searchTerm": "title"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(data['total_questions'], 0)
    
    def test_search_questions_empty_query(self):
        """Test the POST /questions/search endpoint behavior for an empty query"""
        res = self.client().post('/questions/search', json={
            "seachTerm": ""
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_get_questions_by_category(self):
        """Test the GET /categories/<int>/questions endpoint"""
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(data['questions'], None)
        self.assertNotEqual(data['total_questions'], 0)
        self.assertEqual(data['current_category'], 'Science')
    
    def test_get_questions_by_category_outside_range(self):
        """Test the GET /categories/<int>/questions endpoint for an out of range category ID"""
        res = self.client().get('/categories/10000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
    
    def test_play_quiz(self):
        """Test the POST /quizzes endpoint"""
        res = self.client().post('/quizzes', json={
            "quiz_category": {"id": 1, "type": "Science"},
            "previous_questions": [5, 9, 13]
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question']['category'], 1)

    def test_play_quiz_no_prev_questions(self):
        """Test the POST /quizzes endpoint behavior for missing previous questions"""
        res = self.client().post('/quizzes', json={
            "quiz_category": {"id": 1, "type": "Science"},
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_play_quiz_no_category(self):
        """Test the POST /quizzes endpoint behavior for missing category"""
        res = self.client().post('/quizzes', json={
            "previous_questions": [5, 9, 13]
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()