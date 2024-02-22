import torch
import torch.utils.data
from Urdu_Text_Recognition_official_modified.model import Model
from Urdu_Text_Recognition_official_modified.dataset import NormalizePAD
from Urdu_Text_Recognition_official_modified.utils import CTCLabelConverter, AttnLabelConverter, Logger
from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, Query
from fastapi.security import APIKeyQuery
import os
from PIL import Image
from io import BytesIO
import math
import datetime
import pytz
import io
<<<<<<< HEAD
# app = FastAPI()

# # Define an API key security scheme using a query parameter
# # api_key_query = APIKeyQuery(name="api_key")
# result_final=''
# # reader = easyocr.Reader(['ch_sim','en'],gpu=True) # this needs to run only once to load the model into memory

# output_channel=32
# FeatureExtraction="HRNet" 
# device_id=None 
# if FeatureExtraction == "HRNet":
#     output_channel = 32
# """ vocab / character number configuration """
# file = open("Urdu_Text_Recognition_official_modified/UrduGlyphs.txt","r",encoding="utf-8")
# content = file.readlines()
# content = ''.join([str(elem).strip('\n') for elem in content])
# character = content+" "

# cuda_str = 'cuda'
# if device_id is not None:
#     cuda_str = f'cuda:{device_id}'
# global device
# device = torch.device(cuda_str if torch.cuda.is_available() else 'cpu')
# print("Device : ", device)
# image_path=None   
# saved_model="Urdu_Text_Recognition_official_modified/best_norm_ED.pth" 
# batch_max_length=100 
# imgH=32  
# imgW=400 
# rgb=False
# SequenceModeling="DBiLSTM" 
# Prediction="CTC" 
# num_fiducial=20 
# input_channel=1 
# output_channel=output_channel
# hidden_size=256 
# device = device
# os.makedirs("Urdu_Text_Recognition_official_modified/read_outputs", exist_ok=True)
# datetime_now = str(datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%Y-%m-%d_%H-%M-%S"))
# logger = Logger(f'Urdu_Text_Recognition_official_modified/read_outputs/{datetime_now}.txt')
# """ model configuration """
# if 'CTC' in Prediction:
#     converter = CTCLabelConverter(character)
# else:
#     converter = AttnLabelConverter(character)
# num_class = len(converter.character)

# if rgb:
#     input_channel = 3
# opt=[image_path,saved_model,batch_max_length,imgH,imgW,rgb,FeatureExtraction,SequenceModeling,Prediction,num_fiducial,input_channel,output_channel,hidden_size,device_id,num_class,device]
# # opt=[image_path 0,saved_model 1,batch_max_length 2,imgH 3,imgW 4,rgb 5,FeatureExtraction 6,SequenceModeling 7,Prediction 8,num_fiducial 9,input_channel 10,output_channel 11,hidden_size 12,device_id 13,num_class 14]

# model = Model(opt)
# logger.log('model input parameters', imgH, imgW, num_fiducial, input_channel, output_channel,
#         hidden_size, num_class, batch_max_length, FeatureExtraction,
#         SequenceModeling, Prediction)
# model = model.to(device)

# # load model
# model.load_state_dict(torch.load(saved_model, map_location=device))
# logger.log('Loaded pretrained model from %s' % saved_model)
# model.eval()
# def read(file_path):
    
#     image_path=file_path
   
    
#     if rgb:
#         img = Image.open(image_path).convert('RGB')
#     else:
#         img = Image.open(image_path).convert('L')
#     img = img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
#     w, h = img.size
#     ratio = w / float(h)
#     if math.ceil(imgH * ratio) > imgW:
#         resized_w = imgW
#     else:
#         resized_w = math.ceil(imgH * ratio)
#     img = img.resize((resized_w, imgH), Image.Resampling.BICUBIC)
#     transform = NormalizePAD((1, imgH, imgW))
#     img = transform(img)
#     img = img.unsqueeze(0)
#     # print(img.shape) # torch.Size([1, 1, 32, 400])
#     batch_size = img.shape[0] # 1
#     img = img.to(device)
#     preds = model(img)
#     preds_size = torch.IntTensor([preds.size(1)] * batch_size)
    
#     _, preds_index = preds.max(2)
#     preds_str = converter.decode(preds_index.data, preds_size.data)[0]
#     return preds_str
# # FastAPI route for text extraction


# # FastAPI route for text extraction from an image
# @app.post("/extract_text/")
# async def extract_text(
#     file: UploadFile = File(...),
#     # api_key: str = Depends(api_key_query),
# ):
#     print('***********************************************************')
#     # Check the API key
#     # if api_key != "api1234":
#         # raise HTTPException(status_code=401, detail="API Key not valid")

#     # Read the uploaded image file
#     image_data = await file.read()
#     # image = Image.open(BytesIO(image_data))

#     # Perform text extraction on the image
#     extracted_text = read(image_data)  # Modify read function to accept the image

#     return {"extracted_text": extracted_text}
# import torch
# import torch.utils.data
# from Urdu_Text_Recognition_official_modified.model import Model
# from Urdu_Text_Recognition_official_modified.dataset import NormalizePAD
# from Urdu_Text_Recognition_official_modified.utils import CTCLabelConverter, AttnLabelConverter, Logger
# from fastapi import FastAPI, File, UploadFile
# from PIL import Image
# from io import BytesIO
# import math
# import datetime
# import pytz
=======
import os

# In your FastAPI application (model_api.py)
with open("fastapi_pid.txt", "w") as pid_file:
    pid_file.write(str(os.getpid()))
>>>>>>> master

app = FastAPI()
api_key_query = APIKeyQuery(name="api_key")

result_final = ''
output_channel = 32
FeatureExtraction = "HRNet"
device_id = None
if FeatureExtraction == "HRNet":
    output_channel = 32

file = open("Urdu_Text_Recognition_official_modified/UrduGlyphs.txt", "r", encoding="utf-8")
content = file.readlines()
content = ''.join([str(elem).strip('\n') for elem in content])
character = content + " "

cuda_str = 'cuda'
if device_id is not None:
    cuda_str = f'cuda:{device_id}'
global device
device = torch.device(cuda_str if torch.cuda.is_available() else 'cpu')
print("Device: ", device)
image_path = None
saved_model = "Urdu_Text_Recognition_official_modified/best_norm_ED.pth"
batch_max_length = 100
imgH = 32
imgW = 400
rgb = False
SequenceModeling = "DBiLSTM"
Prediction = "CTC"
num_fiducial = 20
input_channel = 1
output_channel = output_channel
hidden_size = 256
device = device
os.makedirs("Urdu_Text_Recognition_official_modified/read_outputs", exist_ok=True)
datetime_now = str(datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%Y-%m-%d_%H-%M-%S"))
logger = Logger(f'Urdu_Text_Recognition_official_modified/read_outputs/{datetime_now}.txt')

if 'CTC' in Prediction:
    converter = CTCLabelConverter(character)
else:
    converter = AttnLabelConverter(character)
num_class = len(converter.character)

if rgb:
    input_channel = 3

opt = [image_path, saved_model, batch_max_length, imgH, imgW, rgb, FeatureExtraction, SequenceModeling, Prediction,
       num_fiducial, input_channel, output_channel, hidden_size, device_id, num_class, device]

model = Model(opt)
logger.log('model input parameters', imgH, imgW, num_fiducial, input_channel, output_channel,
        hidden_size, num_class, batch_max_length, FeatureExtraction,
        SequenceModeling, Prediction)
model = model.to(device)

# Load model
model.load_state_dict(torch.load(saved_model, map_location=device))
logger.log('Loaded pretrained model from %s' % saved_model)
model.eval()


def read(file_path):
    image_path = file_path

    if rgb:
        img = Image.open(io.BytesIO(image_path)).convert('RGB')
    else:
        img = Image.open(io.BytesIO(image_path)).convert('L')
    img = img.transpose(Image.FLIP_LEFT_RIGHT)
    w, h = img.size
    ratio = w / float(h)
    if math.ceil(imgH * ratio) > imgW:
        resized_w = imgW
    else:
        resized_w = math.ceil(imgH * ratio)
    img = img.resize((resized_w, imgH), Image.BICUBIC)
    transform = NormalizePAD((1, imgH, imgW))
    img = transform(img)
    img = img.unsqueeze(0)
    batch_size = img.shape[0]
    img = img.to(device)
    preds = model(img)
    preds_size = torch.IntTensor([preds.size(1)] * batch_size)

    _, preds_index = preds.max(2)
    preds_str = converter.decode(preds_index.data, preds_size.data)[0]
    return preds_str


@app.post("/extract_text/")
async def extract_text(
    file: UploadFile = File(...),
    api_key: str = Depends(api_key_query),

):
    print('***********************************************************')
    if api_key != "apikey1234":
        raise HTTPException(status_code=401, detail="API Key not valid")
    image_data = await file.read()
    extracted_text = read(image_data)
    print('extracted_text',extracted_text)
    return {"extracted_text": extracted_text}
<<<<<<< HEAD
=======
if __name__ == "__main__":
    # Run the FastAPI application
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
>>>>>>> master
