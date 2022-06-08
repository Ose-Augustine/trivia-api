import json
import os
from unicodedata import category
from flask import Flask, Response, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions


def return_all_categories():
    categories = Category.query.all()
    ids = [group.id for group in categories]
    filtered_categories = [group.type for group in categories]
    # jointly iterate over the two lists
    result = zip(ids, filtered_categories)
    package = {}
    for id, type in result:
        package[f'{id}'] = f'{type}'

    return package


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, POST,DELETE,OPTIONS')
        return response

    @app.route('/categories')
    def all_categories():
        filtered_categories = return_all_categories()

        if len(filtered_categories) == 0:
            abort(500)

        return jsonify({
            "categories": filtered_categories
        })

    @app.route('/questions')
    def retrieve_questions():
        question = Question.query.all()
        paginated = paginate_questions(request, question)
        filtered_categories = return_all_categories()

        if len(paginated) == 0:
            abort(404)

        else:
            return jsonify({
                'questions': paginated,
                'totalQuestions': len(paginated),
                'categories': filtered_categories,
            })

    @app.route('/questions', methods=['POST'])
    def retrieve_questions_by_search_term():
        body = request.get_json()
        term = body.get("searchTerm", None)
        if term is None:
            question = body.get('question', None)
            answer = body.get('answer', None)
            difficulty = body.get('difficulty', None)
            category = body.get('category', None)

            new_question = Question(
                question=question,
                answer=answer,
                difficulty=int(difficulty),
                category=int(category))

            try:
                new_question.insert()
                return ""

            except BaseException:
                new_question.turn_back()

        else:
            # to search for the term anywhere it is a substring in the column
            questions = Question.query.filter(
                Question.question.contains(f'{term}')).all()
            filtered_questions = [quizz.format() for quizz in questions]

            if len(filtered_questions) == 0:
                abort(404)

            return jsonify({
                'questions': filtered_questions,
                'totalQuestions': len(filtered_questions),
                'currentCategory': questions[0].category
            })

    @app.route('/categories/<int:id>/questions')
    def get_questions_by_category(id):
        '''This would return the questions having the particular category id '''
        Quizz = Question.query.filter_by(category=id)
        selected = [info.format() for info in Quizz]
        category = Category.query.get(id)

        if len(selected) == 0:
            abort(404)

        return jsonify({
            'questions': selected,
            'totalQuestions': len(selected),
            'currentCategory': category.type
        })

    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        question = Question.query.filter_by(id=id).one_or_none()
        id = question.id
        try:
            question.delete()
            return jsonify({
                "id":id
            })
        except BaseException:
            if question is None:
                abort(404)

    @app.route('/quizzes', methods=['POST'])
    def return_quizzes():
        body = request.get_json()
        previous_questions = body.get('previous_questions', None)
        current_category   = body.get('quiz_category',None)
        # returns all the objects of questions whose id's are not in the
        # [previous_questions]
        category = Category.query.filter_by(type=f'{current_category}').first()
        all_questions = Question.query.filter(
            ~Question.id.in_(previous_questions), Question.category==category.id ).all()

        return jsonify({
            'question':random.choice(all_questions).format()
        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': "Resource not found"
        }), 404

    @app.errorhandler(422)
    def uprocessed(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': "Could not be processed"
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': "Server did not load this request"
        }), 500

    @app.errorhandler(405)
    def unsupported_method(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': "Method not allowed for this route"
        }), 405
    return app
