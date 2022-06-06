import json
import os
from unicodedata import category
from flask import Flask, Response, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category,db 

QUESTIONS_PER_PAGE = 10

def paginate_questions(request,selection):
  page = request.args.get("page",1,type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE 
  end   = start + QUESTIONS_PER_PAGE 
  questions = [question.format() for question in selection]
  current_questions = questions[start:end]
  return current_questions 

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app,resources={r"/api/*":{"origins":"*"}})

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods','GET, POST, PATCH,DELETE,OPTIONS')
    return response
  

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def all_categories():
    categories = Category.query.all()

    return jsonify({
      "categories":categories
    })


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def retrieve_questions():
    question = Question.query.all()
    paginated = paginate_questions(request,question)
    questions = [quizz['question'] for quizz in paginated]
    categories = [quizz['category'] for quizz in paginated]
    filtered_categories = []
    for char in categories:
      category_name = Category.query.get_or_404(int(char)).type
      if filtered_categories.count(category_name) <= 1:
        filtered_categories.append(category_name)
     
    if len(paginated)==0:
      abort(404)
    
    else:
      return jsonify({
        'questions': questions,
        'total_questions':len(questions),
        'categories':filtered_categories ,
      })
  
  @app.route('/questions',methods=['POST'])
  def retrieve_questions_by_search_term():
    body = request.get_json()
    term = body.get("search_term",None)
    questions = Question.query.filter(Question.question.contains(f'{term}')).all()#to search for the term anywhere it is a substring in the column
    filtered_questions = [quizz.question for quizz in questions]

    return jsonify({
      'success':True,
      'questions': filtered_questions,
      'total_questions':len(filtered_questions),
      'current_category':questions[0].category
    })

  @app.route('/categories/<int:id>/questions')
  def get_questions_by_category(id):
    '''This would return the questions having the particular category id '''
    #category = Category.query.filter_by(id=id)
    Quizz = Question.query.filter_by(category=id)
    selected = [questions.question for questions in Quizz]

    return jsonify({
      'questions':selected,
      'total_questions':len(selected),
      'current_category':id
    })

  @app.route('/questions/<int:id>',methods = ['DELETE'])
  def delete_question(id):
    question = Question.query.filter_by(id=id).one_or_none()   
    try:
      question.delete()
    except:
      if question == None:
        abort(400)
    return jsonify({
      'success':True,
      'deleted_question':question.id,
      'question':question.question           
    })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    