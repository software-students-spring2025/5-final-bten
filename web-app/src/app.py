from flask import Flask, jsonify, request, render_template
import requests
import os
from dotenv import load_dotenv


def create_app():
    app = Flask(__name__)
    load_dotenv()

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
        # call chatgpt here
        recipe = {"recipe" : "recipe"}
        return jsonify(recipe)
        
    
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
