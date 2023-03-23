from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)

def test_null_prediction():
    response = client.post('/v1/prediction', json = {
                                                    'opening_gross': 0,
                                                    'screens': 0,
                                                    'production_budget': 0,
                                                    'title_year': 0,
                                                    'aspect_ratio': 0,
                                                    'duration': 0,
                                                    'cast_total_facebook_likes': 0,
                                                    'budget': 0,
                                                    'imdb_score': 0
                                                    })
    assert response.status_code == 200
    assert response.json()['worldwide_gross'] == 0

def test_random_prediction():
    response = client.post('/v1/prediction', json = {
                                                    "opening_gross": -0.204070235848411, 
                                                    "screens": 0.2720718520157005, 
                                                    "production_budget": 1.4462286612410742, 
                                                    "title_year": 0.6945119541987584, 
                                                    "aspect_ratio": -1.2536853385188789, 
                                                    "duration": 0.6771937154413307, 
                                                    "cast_total_facebook_likes": -1.313758953592533, 
                                                    "budget": 1.3865529826041392, 
                                                    "imdb_score": -1.069728136935526
                                                    })
    assert response.status_code == 200
    assert response.json()['worldwide_gross'] >= 0 