import os
from unicodedata import category
from urllib import response
import random
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, origins="*")

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Header', 'Content-Type')
        response.headers.add('Access-Control-Allow-Method', 'GET, POST, DELETE')
        
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=["GET"])
    def get_categories():

        categories = Category.query.all()
        categories = {category.id: category.type for category in categories}

        return jsonify(
            {
                'categories': categories
            }
        )

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route('/questions', methods=["GET"])
    def get_questions():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        categories = Category.query.all()
        categories = {category.id: category.type for category in categories}
        questions = Question.query.order_by(Question.id).all()
        formatted_questions = [question.format() for question in questions]
        questions_in_next_page = formatted_questions[start:end]
        current_category = {question['category'] for question in questions_in_next_page}

        if len(questions) < start:
            abort(404)
        else:
            return jsonify(
                {
                    "questions": questions_in_next_page,
                    "totalQuestions": len(questions),
                    "categories": categories,
                    "currentCategory": list(current_category)
                }
            )

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):

        try:
            question = Question.query.get(question_id)
            question.delete()
        except AttributeError:
            abort(422, description="question with id provided does not exist")

        return jsonify({
            'id': question_id,
            'deleted': True
            })
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        data = request.json
        try:
            search_term = data["searchTerm"]              
            questions = Question.query.filter(Question.question.ilike(f"%{search_term}%")).all()
        except KeyError:
            abort(400, description="Incomplete Data: Requests to this endpoint should contain searchTerm")

        return jsonify(
                {
                    "questions": [question.format() for question in questions],
                    "totalQuestions": len(questions),
                    "currentCategory": None
                }
            )

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def add_question():
        data = request.json
 
        try:
            question = Question(**{i:data[i] for i in data})
            question.insert()

            return jsonify({"success": True})
        except TypeError:
            abort(400, description="Incomplete Data: Requests to this endpoint should contain question, answer, difficulty and category")

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_based_on_category(category_id):

        try:       
            questions = Question.query.filter(Question.category == category_id).all()
            current_category = Category.query.get(category_id).type
        except AttributeError:
            abort(422, description="category with id specified does not exist")

        return jsonify(
            {
                "questions": [question.format() for question in questions],
                "totalQuestions": len(questions),
                "currentCategory": current_category
            }
        )

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route('/quizzes', methods=['POST'])
    def get_next_question():

        data = request.json
        category_id = data["quiz_category"]["id"]
        previous_questions_id = data["previous_questions"]

        if category_id == 0:
            questions_left_in_category = Question.query.filter(
                Question.id.notin_(previous_questions_id)).all()
        else:
            try:
                category_id = int(category_id)
                questions_left_in_category = Question.query.filter(
                    Question.category == category_id).filter(
                        Question.id.notin_(previous_questions_id)).all()
            except ValueError:
                abort(400, description="Category specified is invalid: category Id should be an integer")

        question = random.choice(questions_left_in_category).format() if len(
            questions_left_in_category) else False

        return jsonify({"question" : question})
       

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request",
            "Additional info": error.description
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Page Not Found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable",
            "Additional info": error.description
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    return app

