from fastapi import FastAPI
from .app.models import PredictionResponse, PredictionRequest
from .app.views import get_prediction

# esto es para que la documentacion que se genera con fastapi este en el origen
app = FastAPI(docs_url='/')


@app.post('/v1/prediction')
def make_model_prediction(request: PredictionRequest):
    return PredictionResponse(worldwide_gross=get_prediction(request))