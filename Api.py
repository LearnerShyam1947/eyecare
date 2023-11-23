from flask_restx import Api, Namespace, Resource
from predict import classify_using_bytes
from flask import request

api = Api(
    version="1.0",
    title="Eye Disease Predictor",
    description="This api help to predict the eye disease of an infected eye using its image",
    doc="/api",
    validate=True
)

requestCtrl = Namespace("Prediction", "Send an image file in post to predict.....!!!", path="/api-predict")

@requestCtrl.route("/")
class RequestController(Resource):
    def get(self):
        return {'hello' : "world"}
    
    def post(self):
        image = request.files.get("image")
        result = classify_using_bytes(image.read(), "models/model.h5")
        return result
    
api.add_namespace(requestCtrl)
