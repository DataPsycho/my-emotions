from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from modelboy.flow import loader
from .config import config_by_name, model_dir


def create_app(config_obj=config_by_name, config_name=None):
    if config_name:
        app = Flask(__name__)
        app.config.from_object(config_obj[config_name])
        CORS(app)
    else:
        app = Flask(__name__)
        CORS(app)

    @app.before_first_request
    def load_models():
        global model
        global tf_idf
        model, tf_idf = loader(model_dir, version=2)

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true'
        )
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PATCH,POST,DELETE,OPTIONS'
        )
        return response

    @app.route("/")
    def welcome():
        return "Welcome"

    @app.route("/scores", methods=["POST",])
    def classify_message():
        score_map = {0: "not satisfied", 1: "moderate", 2: "satisfied"}
        body = request.get_json()
        if not body:
            abort(400)
        text = body.get("text")
        if not text:
            abort(400, {
                "success": False,
                "error": 400,
                "message": "text json header is missing."
            })
        try:
            a_data = [text]
            transformed = tf_idf.transform(a_data)
            score = int(model.predict(transformed))
            proba = model.predict_proba(transformed)[0][score]*100
            return jsonify({
                "success": True,
                "score": score,
                "label": score_map.get(score),
                "confidence": round(proba, 2)
            })
        except Exception as e:
            print(e)
            abort(422)

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(404)
    def ressource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404
    return app
