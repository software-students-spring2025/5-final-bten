from flask import Flask, jsonify, request, render_template
import requests
import os
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId


from mlclient import get_recipe_reccomendation

apiKey = str(input("Please copy in OpenAI API Key: "))
os.environ["OPENAI_API_KEY"] = apiKey

def create_app():
    app = Flask(__name__)
    load_dotenv()

    MONGO_URI = os.getenv("MONGO_URI")
    client = MongoClient(MONGO_URI)

    db = client['recipes']

    @app.route("/")
    def home():
        """Home Route"""
        return render_template("index.html")

    @app.route("/predict", methods=["POST"])
    def predict():
        data = request.get_json()
        user_input = data.get("ingredients","")
        # call chatgpt api here
        if not user_input:
            return jsonify({"error": "no ingredients"})

        recipe = get_recipe_reccomendation(user_input)

        result = db.recipes.insert_one(recipe)
        recipe['_id'] = str(result.inserted_id)
        return jsonify(recipe)

    # exception handling?


    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", debug=True)
