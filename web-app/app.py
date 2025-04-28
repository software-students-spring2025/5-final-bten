from flask import Flask, jsonify, request, render_template
import requests
import os
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId
from datetime import datetime


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
        ingredients = data.get("ingredients")
        goals = data.get("goals")
        additional_notes = data.get("additionalNotes")

        # Create recipe document
        recipe_doc = {
            "ingredients": ingredients,
            "goals": goals,
            "additional_notes": additional_notes,
            "timestamp": datetime.utcnow(),
            "recipe": "Sample recipe instructions" # Replace with actual recipe generation
        }

        # Store in MongoDB
        result = db.recipes.insert_one(recipe_doc)
        recipe_doc['_id'] = str(result.inserted_id)
        
        return jsonify(recipe_doc)

    @app.route("/recipes", methods=["GET"])
    def get_recipes():
        """Get all recipes for the current session"""
        recipes = list(db.recipes.find().sort("timestamp", -1))
        
        # Convert ObjectId to string for JSON serialization
        for recipe in recipes:
            recipe['_id'] = str(recipe['_id'])
            recipe['timestamp'] = recipe['timestamp'].isoformat()
            
        return jsonify(recipes)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=3000, debug=True) 