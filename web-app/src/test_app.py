from app import create_app
import pytest


@pytest.fixture
def test_client():
    """Fixture for Flask test client."""
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


def test_home_route(test_client):
    """Test that the home page loads successfully."""
    response = test_client.get("/")
    assert response.status_code == 200


def test_predict_route(test_client):
    """Test that predict routes returns recipe from ML client"""
    response = test_client.get("/predict")
    assert response.data