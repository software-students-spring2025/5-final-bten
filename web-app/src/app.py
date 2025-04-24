from flask import Flask, jsonify, request, render_template
import requests
import os
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId


def create_app():
    app = Flask(__name__)
    load_dotenv()
    client = MongoClient(('mongodb://localhost:27017'))
    db = client['recipes']

    """
    openai_api_key = os.getenv("OPENAI_API_KEY")
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client.get_database("Recipe")
    collection = db.get_collection("logs")
    
    """

    @app.route("/")
    def home():
        """Home Route"""
        return render_template("index.html")

    @app.route("/predict", methods=["POST"])
    def predict():
        data = request.get_json()
        ingredient = data.get("ingredients")
        # call chatgpt api here
        recipe = {"recipe" : "recipe"}
        result = db.recipes.insert_one(recipe)
        recipe['_id'] = str(result.inserted_id)
        return jsonify(recipe)   
        
    
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
