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

def return_all_categories():
  categories          = Category.query.all()
  ids                 = [group.id for group in categories]
  filtered_categories = [group.type for group in categories]
  result              = zip(ids,filtered_categories)#jointly iterate over the two lists 
  package             = {}
  for id,type in result:
    package[f'{id}'] = f'{type}'
  
  return package 

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app,resources={r"/api/*":{"origins":"*"}})

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods','GET, POST,DELETE,OPTIONS')
    return response
  

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def all_categories():
    filtered_categories = return_all_categories()

    if len(filtered_categories)==0:
      abort(500)

    return jsonify({
      "categories":filtered_categories
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
    filtered_categories = return_all_categories()
    
     
    if len(paginated)==0:
      abort(404)
    
    else:
      return jsonify({
        'questions': paginated,
        'totalQuestions':len(paginated),
        'categories':filtered_categories ,
      })
  
  @app.route('/questions',methods=['POST'])
  def retrieve_questions_by_search_term():
    body = request.get_json()
    term = body.get("searchTerm",None)
    if term == None:
      question   = body.get('question',None) 
      answer     = body.get('answer',None)
      difficulty = body.get('difficulty',None)
      category   = body.get('category',None)

      new_question = Question(question=question,answer=answer,difficulty=int(difficulty),category=int(category))
      
      try:
        new_question.insert()

      except:
        new_question.turn_back()

      return "Success"
    else:
      questions = Question.query.filter(Question.question.contains(f'{term}')).all()#to search for the term anywhere it is a substring in the column
      filtered_questions = [quizz.format() for quizz in questions]

      if len(filtered_questions)==0:
        abort(404)

      return jsonify({
        'questions': filtered_questions,
        'totalQuestions':len(filtered_questions),
        'currentCategory':questions[0].category
      })

  @app.route('/categories/<int:id>/questions')
  def get_questions_by_category(id):
    '''This would return the questions having the particular category id '''
    Quizz = Question.query.filter_by(category=id)
    all_questions = Question.query.all()
    selected = [info.format() for info in Quizz]
    category = Category.query.get(id)

    if len(selected)==0:
      abort(404)

    return jsonify({
      'questions':selected,
      'totalQuestions':len(selected),
      'currentCategory':category.type
    })

  @app.route('/questions/<int:id>',methods = ['DELETE'])
  def delete_question(id):
    question = Question.query.filter_by(id=id).one_or_none()   
    try:
      question.delete()
    except:
      if question == None:
        abort(404)

  @app.route('/quizzes',methods=['POST']) 
  def return_quizzes():
    
    pass



  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success':False,
      'error':404,
      'message':"Resource not found"
    }),404

  @app.errorhandler(422)
  def uprocessed(error):
    return jsonify({
      'success':False,
      'error':422,
      'message':"Could not be processed"
    }),422

  @app.errorhandler(500)
  def server_error(error):
    return jsonify({
      'success':False,
      'error': 500,
      'message':"Server did not load this request"
    }),500

  @app.errorhandler(405)
  def unsupported_method(error):
    return jsonify({
      'success':False,
      'error':405,
      'message':"Method not allowed for this route"
    }),405
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

    