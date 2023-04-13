from fastapi import APIRouter, File, UploadFile
from fastapi.encoders import jsonable_encoder

import io
from routes.recognition import model
from PIL import Image

router = APIRouter(
    prefix="/api/recognition",
    tags=["recognition"]
)

@router.post('/torch')
async def predict_torch(file: UploadFile = File(...)):
    # start_time = time.time()
    # print('stream is called')
    img = await file.read()
    img = Image.open(io.BytesIO(img))
    img = img.convert("RGB") 
    # print("get %s seconds ---" % (time.time() - start_time))
    prediction = model.predict_torch(img)
    print("test")
    resultJson = jsonable_encoder(prediction)
    return resultJson

@router.post('/onnx')
async def predict_onnx(file: UploadFile = File(...)):
    # start_time = time.time()
    # print('stream is called')
    img = await file.read()
    img = Image.open(io.BytesIO(img))
    img = img.convert("RGB") 
    # print("get %s seconds ---" % (time.time() - start_time))
    prediction = model.predict_onnx(img)
    resultJson = jsonable_encoder(prediction)
    return resultJson