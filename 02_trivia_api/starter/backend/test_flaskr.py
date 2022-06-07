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
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format('augustine','bahdman','localhost:5432', self.database_name)
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

    def test_get_all_categories(self):
        res  = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data["categories"])

    def test_405_for_categories(self):
        res = self.client().patch("/categories")

        self.assertEqual(res.status_code,405)

    def test_404_for_categories(self):
        res = self.client().get("/categories/1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)

    def test_get_all_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data) 

        self.assertEqual(res.status_code,200)
        self.assertTrue(data["questions"])
        self.assertTrue(data["totalQuestions"])
        self.assertTrue(data["categories"])

    def test_405_for_questions(self):
        res = self.client().delete("/questions") 

        self.assertEqual(res.status_code,405)

    def test_get_search_term_match_on_questions(self):
        res  = self.client().post("/questions", json={"searchTerm":"young"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data["questions"])
        self.assertTrue(data["totalQuestions"])
        self.assertTrue(data["currentCategory"])
    
    def test_search_term_no_result_on_questions(self):
        res = self.client().post("/questions", json={"searchTerm":"fulani"})
        
        self.assertEqual(res.status_code,404)

    def test_insert_new_questions(self):
        res = self.client().post("/questions", json={
            "question":"Who is the Oscar's named after",
            "answer":"Oscar Wilde",
            "category":2,
            "difficulty":3
            })
        self.assertEqual(res.status_code,200)
    
    def test_get_questions_by_categories(self):
        res  = self.client().get("/categories/1/questions")
        data = json.loads(res.data) 

        self.assertEqual(res.status_code,200)
        self.assertTrue(data["questions"])
        self.assertTrue(data["totalQuestions"])
        self.assertTrue(data["currentCategory"])
    
    def test_non_existing_category_for_questions(self):
        res  = self.client().get("/categories/100/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertTrue(data["message"],"Resource not found")

    def test_unsupported_method_for_questions_by_categories(self):
        res = self.client().delete("/categories/1/questions")

        self.assertEqual(res.status_code,405)





# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()