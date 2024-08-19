import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    """Create and configure the app"""
    app = Flask(__name__)

    # Version of flask used here requires app context for initialization.
    with app.app_context():
        if test_config is None:
            setup_db(app)
        else:
            database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
            setup_db(app, database_path=database_path)

    # Set up CORS, allowing '*' for origins (default)
    CORS(app)

    @app.after_request
    def after_request(response):
        """Access control."""
        response.headers.add('Access-Control-Allow-Origin', '*') # allow all origins
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization') # allow content type and auth headers
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS') # allow most types of requests
        return response

    @app.route('/categories', methods=['GET'])
    def get_categories():
        """GET endpoint to query all categories."""
        categories = Category.query.all() # query all categories during a GET

        # construct a dict for the categories using list comprehension
        categories_dict = {category.id: category.type for category in categories}

        # return a JSON response on successful query with all the categories
        return jsonify(
            {
                'success': True,
                'categories': categories_dict
            }
        )

    def paginate_questions(request, selection):
        """Helper function to paginate questions."""
        page = request.args.get('page', 1, type=int) # default to page 1
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        # select questions with list comprehension
        questions = [question.format() for question in selection]
        paginated_questions = questions[start:end] # filter questions based on pagination rules
        
        return paginated_questions

    @app.route('/questions', methods=['GET'])
    def get_questions():
        """Endpoint to handle GET requests for questions,
        including pagination (every 10 questions).
        Returns a list of questions,
        number of total questions, current category, categories."""
        # First, query all questions in the db
        selection = Question.query.all()
        total_questions = len(selection)
        current_questions = paginate_questions(request, selection)

        if len(current_questions) == 0:
            abort(404)

        # Next, query all categories in the db
        categories = Category.query.all()
        # Construct dict with list comprehension
        categories_dict = {category.id: category.type for category in categories}

        # Construct the response JSON
        return jsonify(
            {
                'success': True,
                'questions': current_questions,
                'total_questions': total_questions,
                'current_category': None,
                'categories': categories_dict
            }
        ), 200

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        """endpoint to DELETE question using a question ID."""
        try:
            # Query question by ID provided in the API call
            question = Question.query.get(question_id)

            # If not found, abort with 404
            if question is None:
                abort(404)
        
            # Delete question from database
            db.session.delete(question)
            db.session.commit()

            # Return JSON on success
            return jsonify(
                {
                    'success': True,
                    'deleted': question_id
                }
            ), 200
        except Exception as e:
            # Rollback session if error occurred
            db.session.rollback()
            abort(404)
        
        finally:
            db.session.close()

    @app.route('/questions', methods=['POST'])
    def add_question():
        """Endpoint to POST a new question, which requires the question and answer text,
        category, and difficulty score."""
        body = request.get_json()

        # get relevant data from the JSON provided in the request
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)

        # validate that all requisite data has been provided, throw a 400 error if not
        if not (new_question and new_answer and new_category and new_difficulty):
            abort(400)
        
        try:
            # Construct new Question object for db insert
            question = Question(
                question = new_question,
                answer = new_answer,
                category = new_category,
                difficulty = new_difficulty
            )

            # Add question to db
            db.session.add(question)
            db.session.commit()

            # Return JSON on success
            return jsonify(
                {
                    'success': True,
                    'created': question.id,
                    'question': question.question,
                    'answer': question.answer,
                    'category': question.category,
                    'difficulty': question.difficulty
                }
            ), 201

        except Exception as e:
            db.session.rollback()
            abort(500)
        
        finally:
            db.session.close()

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        """POST endpoint to get questions based on a search term."""
        body = request.get_json()

        # From the provided JSON, get the search term
        search_term = body.get('searchTerm', None)

        # Throw a 400 error if no search term
        if not search_term:
            abort(400)

        try:
            # Query by search term using ilike
            results = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()

            # Construct results JSON after formatting questions using list comprehension
            questions = [question.format() for question in results]
            total_questions = len(questions)

            return jsonify(
                {
                    'success': True,
                    'questions': questions,
                    'total_questions': total_questions,
                    'current_category': None
                }
            ), 200

        except Exception as e:
            abort(500)

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        """GET endpoint to get questions based on category."""
        # Throw a 404 if category DNE
        category = Category.query.get(category_id)
        if category is None:
            abort(404)
        
        try:
            # query all questions in a category
            questions = Question.query.filter_by(category=category_id).all()

            # Use list comprehension to format as JSON
            formatted_questions = [question.format() for question in questions]

            # return JSON on success
            return jsonify(
                {
                    'success': True,
                    'questions': formatted_questions,
                    'total_questions': len(formatted_questions),
                    'current_category': category.type
                }
            ), 200
        except Exception as e:
            abort(500)

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        """POST endpoint to get questions to play the quiz."""
        try:
            body = request.get_json()

            # Get category and previous questions from JSON
            category = body.get('quiz_category', None)
            previous_questions = body.get('previous_questions', None)

            # Throw a 400 if input data is bad
            if category is None or previous_questions is None:
                abort(400)

            # Query questions based on category. Return all questions if category id matches 0, filtering by excluding previous questions
            if category['id'] == 0:
                available_questions = Question.query.filter(
                    ~Question.id.in_(previous_questions)
                ).all()
            else:
                available_questions = Question.query.filter_by(
                    category=category['id']
                ).filter(
                    ~Question.id.in_(previous_questions)
                ).all()
            
            # Random selection from the available question bank
            if available_questions:
                new_question = random.choice(available_questions).format()
            else:
                new_question = None
            
            # Format the success JSON (question may be None if not available)
            return jsonify(
                {
                    'success': True,
                    'question': new_question
                }
            ), 200

        except Exception as e:
            abort(400) # 400 here as error is always going to be expected to be bad input
    
    # Error handlers below. 400, 404, 405, 422, and 500 are all handled.

    @app.errorhandler(400)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 400,
            "message": "bad request!"
            }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "resource not found!"
            }), 404
    
    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed!"
        })
    
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable!"
        }), 422
    
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error!"
        }), 500

    return app

