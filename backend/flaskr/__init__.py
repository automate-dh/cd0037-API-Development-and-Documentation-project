import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

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

        return jsonify(
            {
                'categories': {category.id: category.type for category in categories}
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

        questions = Question.query.order_by(Question.id).all()
        categories = Category.query.all()

        return jsonify(
            {
                "questions": [question.format() for question in questions][start:end],
                "totalQuestions": len(questions),
                "categories": {category.id: category.type for category in categories},
                "currentCategory": "category"  # CHANGE this
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

        question = Question.query.get(question_id)
        question.delete()

        return jsonify({'id': question_id})

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route('/questions', methods=['POST'])
    def add_or_search_question():

        data = request.json

        if "searchTerm" in data.keys():
            questions = Question.query.filter(Question.question.ilike("%%%s%%" % data["searchTerm"])).all()

            return jsonify(
                {
                    "questions": [question.format() for question in questions],
                    "totalQuestions": len(questions),
                    "currentCategory": 'category' # CHANGE this
                }
            )

        elif "question" in data.keys():
            try:
                question = Question(**{i:data[i] for i in data})
                question.insert()

                return jsonify({"succes": True})

            except:
                abort() # CHANGE this to include status code

        else:
            abort() # CHANGE this to include status code


    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_based_on_category(category_id):

        questions = Question.query.filter(Question.category == category_id).all()

        return jsonify(
            {
                "questions": [question.format() for question in questions],
                "totalQuestions": len(questions),
                "currentCategory": Category.query.get(category_id).type
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

        category = data["quiz_category"]["id"]
        previous_questions_id = data["previous_questions"]

        previous_questions = [Question.query.get(i) for i in previous_questions_id]

        if category != 0:
            questions_in_category = Question.query.filter(Question.category == category).all() #.filter(Question.id not in previous_questions_id).all()
            breakpoint()
            print (questions_in_category)
        else:
            questions_in_category = Question.query.filter(Question.id not in previous_questions_id).all()

        response = [question.format() for question in questions_in_category]

        return jsonify({"question" : random.choice(response)})
       

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app

