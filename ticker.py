# ticker.py
import json
import uuid
import subprocess
import cv2
import string
import os
import datetime
import shutil
import time
import subprocess
from rapidfuzz import fuzz
import torch
import torch.utils.data
from Urdu_Text_Recognition_official_modified.model import Model
from Urdu_Text_Recognition_official_modified.dataset import NormalizePAD
from Urdu_Text_Recognition_official_modified.utils import CTCLabelConverter, AttnLabelConverter, Logger
from PIL import Image
import pytz
import math
import argparse
import numpy as np
import ffmpeg
import concurrent.futures
import psycopg2
from psycopg2 import sql
import threading
import os
import psycopg2.pool


# In your FastAPI application (model_api.py)
with open("ticker.txt", "w") as pid_file:
    pid_file.write(str(os.getpid()))

def generate_unique_filename():
    unique_id = str(uuid.uuid4())
    valid_chars = string.ascii_letters + string.digits + "_-"
    filename = ''.join(c for c in unique_id if c in valid_chars)
    return filename

# Database connection parameters
DB_PARAMS = {
    'dbname': 'fsma',
    'user': 'postgres',
    'password': 'ticker1234',
    'host': '',  # Replace with your PostgreSQL host
    'port': '5432',  # Default port is 5432
}

connection_pool = psycopg2.pool.ThreadedConnectionPool(1, 10, **DB_PARAMS)

def get_connection():
    return connection_pool.getconn()

def release_connection(conn):
    connection_pool.putconn(conn)

result_final=''

# Connect to PostgreSQL database
conn = psycopg2.connect(**DB_PARAMS)
conn.autocommit = True

output_channel=32
FeatureExtraction="HRNet" 
device_id=None 
if FeatureExtraction == "HRNet":
    output_channel = 32
""" vocab / character number configuration """
file = open("Urdu_Text_Recognition_official_modified/UrduGlyphs.txt","r",encoding="utf-8")
content = file.readlines()
content = ''.join([str(elem).strip('\n') for elem in content])
character = content+" "

cuda_str = 'cuda'
if device_id is not None:
    cuda_str = f'cuda:{device_id}'
global device
device = torch.device(cuda_str if torch.cuda.is_available() else 'cpu')
print("Device : ", device)
image_path=None   
saved_model="Urdu_Text_Recognition_official_modified/best_norm_ED.pth" 
batch_max_length=100 
imgH=32  
imgW=400 
rgb=False
SequenceModeling="DBiLSTM" 
Prediction="CTC" 
num_fiducial=20 
input_channel=1 
output_channel=output_channel
hidden_size=256 
os.makedirs("Urdu_Text_Recognition_official_modified/read_outputs", exist_ok=True)
datetime_now = str(datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%Y-%m-%d_%H-%M-%S"))
logger = Logger(f'Urdu_Text_Recognition_official_modified/read_outputs/{datetime_now}.txt')
""" model configuration """
if 'CTC' in Prediction:
    converter = CTCLabelConverter(character)
else:
    converter = AttnLabelConverter(character)
num_class = len(converter.character)

if rgb:
    input_channel = 3
opt=[image_path,saved_model,batch_max_length,imgH,imgW,rgb,FeatureExtraction,SequenceModeling,Prediction,num_fiducial,input_channel,output_channel,hidden_size,device_id,num_class,device]
# opt=[image_path 0,saved_model 1,batch_max_length 2,imgH 3,imgW 4,rgb 5,FeatureExtraction 6,SequenceModeling 7,Prediction 8,num_fiducial 9,input_channel 10,output_channel 11,hidden_size 12,device_id 13,num_class 14]

model = Model(opt)
logger.log('model input parameters', imgH, imgW, num_fiducial, input_channel, output_channel,
        hidden_size, num_class, batch_max_length, FeatureExtraction,
        SequenceModeling, Prediction)
model = model.to(device)

# load model
model.load_state_dict(torch.load(saved_model, map_location=device))
logger.log('Loaded pretrained model from %s' % saved_model)
model.eval()
def read(file_path):
    
    image_path=file_path
   
    
    if rgb:
        img = Image.open(image_path).convert('RGB')
    else:
        img = Image.open(image_path).convert('L')
    img = img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    w, h = img.size
    ratio = w / float(h)
    if math.ceil(imgH * ratio) > imgW:
        resized_w = imgW
    else:
        resized_w = math.ceil(imgH * ratio)
    img = img.resize((resized_w, imgH), Image.Resampling.BICUBIC)
    transform = NormalizePAD((1, imgH, imgW))
    img = transform(img)
    img = img.unsqueeze(0)
    # print(img.shape) # torch.Size([1, 1, 32, 400])
    batch_size = img.shape[0] # 1
    img = img.to(device)
    preds = model(img)
    preds_size = torch.IntTensor([preds.size(1)] * batch_size)
    
    _, preds_index = preds.max(2)
    preds_str = converter.decode(preds_index.data, preds_size.data)[0]
    return preds_str
# def process_frame(conn, frame, y1, y2, x1, x2, folder_save, channel_name, channel_logo, saving_basename):
#     os.makedirs(f'D:/ummar/ticker_new/ticker_images/{folder_save}', exist_ok=True)
#     date = datetime.datetime.now().date()
#     timeticker = datetime.datetime.now().time()
#     formatted_time = timeticker.strftime("%I:%M %p")

#     width = 640  # keep the original width
#     height = 360
#     dim = (width, height)

#     image = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
#     ticker = image[y1:y2, x1:x2]

#     characters = generate_unique_filename()

#     image_path = f"D:/ummar/ticker_new/ticker_images/{folder_save}/{saving_basename + characters}.jpg"
#     cv2.imwrite(image_path, ticker)

#     text_ticker = read(image_path)

#     if len(text_ticker) > 6:
#         all_objects = Ticker_Extraction_Model.objects.filter(channel_name=channel_name).order_by('-id')[:5]
#         ticker_write = True

#         for obj in all_objects:
#             similarity_ratio = fuzz.ratio(text_ticker, obj.text_ocr)

#             if similarity_ratio >= 80:
#                 ticker_write = False
#                 os.remove(image_path)
#                 break

#         if ticker_write:
#             with conn.cursor() as cursor:
#                 cursor.execute("""
#                     INSERT INTO ticker_extraction_model (channel_name, channel_image, ticker_image, date, time, text_ocr)
#                     VALUES (%s, %s, %s, %s, %s, %s)
#                 """, (channel_name, channel_logo, f"{saving_basename + characters}.jpg", date, formatted_time, text_ticker))
#                 # Commit the changes to the database
#                 conn.commit()



# def streamer(source, y1, y2, x1, x2, folder_save, channel_name,image_name, channel_logo, saving_basename, frames_to_be_skipped):
#     while True:
#         try:
#             input_stream = source  
#             output_pipe = ffmpeg.input(input_stream)

#             frame_count = 0

#             while True:
#                 # Read a frame using ffmpeg
#                 frame, _ = output_pipe.output('pipe:', format='rawvideo', pix_fmt='bgr24').run(capture_stdout=True)

#                 # Convert the raw frame to a numpy array
#                 frame = np.frombuffer(frame, np.uint8).reshape(360, 640, 3)

#                 if frame_count % frames_to_be_skipped == 0:
#                     with concurrent.futures.ThreadPoolExecutor() as executor:
#                         executor.submit(process_frame, frame, y1, y2, x1, x2, folder_save, channel_name, channel_logo, saving_basename)

#                 frame_count += 1

#         except Exception as e:
#             print(f"An error occurred: {str(e)}")
#             time.sleep(2)  # Wait for a few seconds before retrying
#             continue

# def streamer(conn,source, y1, y2, x1, x2, folder_save,image_name, channel_name, channel_logo, saving_basename, frames_to_be_skipped):
#     # while True:
#         try:
#             input_stream = source

#             # Set the frame rate to 30 fps and specify frame dimensions
#             output_pipe = (
#                 ffmpeg.input(input_stream, r=30)
#                 .output('pipe:', format='rawvideo', pix_fmt='bgr24', s='640x360')
#                 .run_async(pipe_stdout=True)
#             )

#             frame_count = 0

#             while True:
#                 # Read a frame using ffmpeg
#                 in_bytes = output_pipe.stdout.read(640 * 360 * 3)  # Read a frame's worth of bytes
#                 if not in_bytes:
#                     continue

#                 frame = np.frombuffer(in_bytes, np.uint8).reshape(360, 640, 3)

#                 if frame_count % frames_to_be_skipped == 0:
#                      with concurrent.futures.ThreadPoolExecutor() as executor:
#                         executor.submit(process_frame, conn,frame, y1, y2, x1, x2, folder_save, channel_name, channel_logo, saving_basename)

#                 frame_count += 1
              

#         except Exception as e:
#             print(f"An error occurred: {str(e)}")
#             time.sleep(2)  # Wait for a few seconds before retrying
#             pass
def streamer(conn,source,y1,y2,x1,x2,folder_save,image_name,channel_name,channel_logo,saving_basename,frames_to_be_skipped):

    target_width = 640
    target_height = 360

    date = datetime.datetime.now().date()
    timeticker = datetime.datetime.now().time()
    formatted_time = timeticker.strftime("%I:%M %p")

    start_time = time.time()

    video_url = source

    # Run the ffmpeg command to extract a frame as a numpy array
    command = [
        r"D:\ffmpeg\bin\ffmpeg",  # Use ffmpeg from system PATH
        "-i", video_url,
        "-vf", f"scale={target_width}:{target_height}",
        "-frames:v", "1",
        "-f", "image2pipe",
        "pipe:1"
    ]

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, _ = process.communicate()

    # Convert the output to a numpy array
    frame = np.frombuffer(output, dtype=np.uint8)

    # Release resources
    process.terminate()

    # Resize the frame to the target dimensions
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

    if frame is not None:
        # Crop the frame using OpenCV
        ticker = frame[y1:y2, x1:x2]
        characters = generate_unique_filename()

        # Save the frame as a PNG image in the specified folder
        cv2.imwrite(f"D:/ummar/ticker_new/ticker_images/{folder_save}/{saving_basename+characters}.jpg", ticker)
            
        text_ticker = read(f"D:/ummar/ticker_new/ticker_images/{folder_save}/{saving_basename + characters}.jpg")

        # print('text_ticker',text_ticker)
        all_objects = None
        with conn.cursor() as cursor:
            try:
                # Fetch latest 5 rows from ticker_extraction_model for the given channel
                cursor.execute("""
                    SELECT * FROM ticker_extraction_model
                    WHERE channel_name = %s
                    ORDER BY id DESC
                    LIMIT 5
                """, (channel_name,))
                all_objects = cursor.fetchall()

                if len(text_ticker) > 6:
                    ticker_write = True

                    # Compare text similarity with each object
                    for obj in all_objects:
                        similarity_ratio = fuzz.ratio(text_ticker, obj[5])  # Assuming text_ocr is at index 5
                        if similarity_ratio >= 80:
                            os.remove(f"D:/ummar/ticker_new/ticker_images/{folder_save}/{saving_basename + characters}.jpg")
                            print('I am similarity')
                            ticker_write = False
                            break

                    if ticker_write:
                        # Insert a new row into ticker_extraction_model
                        cursor.execute("""
                            INSERT INTO ticker_extraction_model (channel_name, channel_image, ticker_image, date, time, text_ocr)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """, (channel_name, channel_logo, f"{saving_basename + characters}.jpg", date, formatted_time, text_ticker))
                        
                        # Commit the changes to the database
                        conn.commit()

            except psycopg2.Error as e:
                # Handle the exception (print or log the error, rollback the transaction if needed)
                print(f"Error executing query: {e}")




def geo_ticker():
    while True:
        conn = get_connection()

        try:
            
            geo_news=streamer(conn,source="udp://@238.190.1.73:5500",y1=305,y2=344,x1=1,x2=520,folder_save='Geo_Ticker',image_name='geoframe.jpg',channel_name='Geo',channel_logo='geo.png',saving_basename='Geonews',frames_to_be_skipped=None)                       
        except Exception as e:
            print(e)
        finally:
           release_connection(conn)

def ary_ticker():
    while True:
        conn = get_connection()

        try:
           ary_news=streamer(conn,source="udp://@238.190.1.54:5500",y1=302,y2=359,x1= 0,x2=531,folder_save='Ary_Ticker',channel_name='Ary',image_name='aryframe.jpg',channel_logo='ary.png',saving_basename='Arynews',frames_to_be_skipped=None)            
        except Exception as e:
            print(e)
        finally:
           release_connection(conn)



def samaa_ticker():
    while True:
        conn = get_connection()

        try:
            samaa_news=streamer(conn,source="udp://@238.190.1.81:5500",y1=305,y2=345,x1=1,x2=515,folder_save='Samaa_Ticker',image_name='samaaframe.jpg',channel_name='Samaa',channel_logo='samaa.png',saving_basename='Samaanews',frames_to_be_skipped=None)            
        except Exception as e:
            print(e)
        finally:
           release_connection(conn)
   


def express_ticker():
    while True:   
        conn = get_connection()

        try:
           express_news= streamer(conn,source="udp://@238.190.1.3:5500",y1=310,y2=358,x1=0,x2=495,folder_save='Express_Ticker',image_name='expressframe.jpg',channel_name='Express',channel_logo='express.png',saving_basename='Expressnews',frames_to_be_skipped=None)            
        except Exception as e:
           print(e)
        finally:
           release_connection(conn)

def dunya_ticker():
    while True :
        conn = get_connection()

        try:
         dunya_news= streamer(conn,source="udp://@238.190.1.4:5500",y1=297,y2=335,x1=89,x2=550,folder_save='Dunya_Ticker',image_name='dunyaframe.jpg',channel_name='Dunya',channel_logo='dunya.png',saving_basename='Dunyanews',frames_to_be_skipped=None)            
        except Exception as e:
          print(e)
        finally:
           release_connection(conn)    
def cnn():
    while True:
        try:
            # conn = get_connection()
 
            cnn_news=streamer_foreign(conn,source= "https://cnn-cnninternational-1-eu.rakuten.wurl.tv/206849c7acd1570962df1ad525fa8688.m3u8",y1=257,y2=330,x1=25,x2=534,folder_save='Cnn_Ticker',channel_name='Cnn',channel_logo="cnn.png",saving_basename='Cnnnews')            

            # cnn_news=streamer_foreign(conn,source= "https://cnn-cnninternational-1-eu.rakuten.wurl.tv/206849c7acd1570962df1ad525fa8688.m3u8",y1=257,y2=330,x1=25,x2=534,folder_save='Cnn_Ticker',image_name='cnn.jpg',channel_name='Cnn',channel_logo="cnn.png",saving_basename='Cnnnews')            
        except Exception as e:
            print(e)
def rt():
    while True:

        try: 
          rt_news= streamer_foreign(conn,source= "https://rt-glb.rttv.com/dvr/rtnews/playlist_4500Kb.m3u8",y1=251,y2=354,x1=94,x2=611,folder_save='Rt_Ticker',image_name='rt.jpg',channel_name='Rt',channel_logo="rt.png",saving_basename='Rtnews')            
        except Exception as e:
          print(e)
        finally:
           release_connection(conn)
def bbc():
    while True:
        
        try: 
          bbc_news= streamer_foreign(conn,source= "http://1292072398.rsc.cdn77.org/NXkCCzWTmdq6H_OMXwUT9Q==,1693473955/1292072398/tracks-v1a1/mono.m3u8",y1=313,y2=359,x1=0,x2=639,folder_save='Bbc_Ticker',image_name='bbc.jpg',channel_name='Bbc',channel_logo="bbc.png",saving_basename='Bbcnews')            
        except Exception as e:
            print(e)
        finally:
           release_connection(conn)
def aljazeera():
    while True:
        conn = get_connection()
        
        try:
           aljazeera_news=   streamer(conn,source="https://www.youtube.com/@aljazeeraenglish/live",y1=292,y2=333,x1=91,x2=608,folder_save='Aljazeera_Ticker',channel_name='Aljazeera',channel_logo='aljazeera.png',saving_basename='Aljazeeranews',frames_to_be_skipped=None)            
        except Exception as e:
            print(e)
        finally:
           release_connection(conn)
def india_today():
    while True :
        conn = get_connection()
       
        try:
           india_today_news= streamer(conn,source="https://www.youtube.com/watch?v=sYZtOFzM78M",y1=256,y2=361,x1=1,x2=641,folder_save='India_Today_Ticker',channel_name='India_Today',channel_logo='india_today.png',saving_basename='IndiaTodaynews',frames_to_be_skipped=None)            
        except Exception as e:
            print(e)
        finally:
           release_connection(conn)


def ninety_two_news():
    while True :
        conn = get_connection()
        
        try:
           ninety_two_news= streamer(conn,source="udp://@238.190.1.48:5500",y1=297,y2=335,x1=40,x2=550,folder_save='Ninety_Two_Ticker',image_name='ninetytwoframe.jpg',channel_name='Ninety_Two',channel_logo='ninetytwo.png',saving_basename='NinetyTwonews',frames_to_be_skipped=None)            
        except Exception as e:
            print(e) 
        finally:
           release_connection(conn)
                      
def twenty_four_news():
    while True :
        conn = get_connection()
       
        try:
           twenty_four_news= streamer(conn,source="udp://@238.190.1.179:5500",y1=287,y2=360,x1=0,x2=521,folder_save='Twenty_Four_Ticker',image_name='twentyfourframe.jpg',channel_name='Twenty_Four',channel_logo='twentyfour.png',saving_basename='TwentyFournews',frames_to_be_skipped=None)            
        except Exception as e:
            print(e)     
        finally:
           release_connection(conn)         

def gnn_news():
    while True :
        conn = get_connection()
        
        try:
           gnn_news= streamer(conn,source="udp://@238.190.1.92:5500",y1=295,y2=360,x1=0,x2=544,folder_save='Gnn_Ticker',channel_name='Gnn',image_name='gnnframe.jpg',channel_logo='gnn.png',saving_basename='Gnnnews',frames_to_be_skipped=None)            
        except Exception as e:
            print(e)     
        finally:
           release_connection(conn) 


def hum_news():
    while True :
        conn = get_connection()
        
        try:
            hum_news= streamer(conn,source="udp://@238.190.1.57:5500",y1=311,y2=349,x1=33,x2=538,folder_save='Hum_Ticker',channel_name='Hum',image_name='humframe.jpg',channel_logo='hum.png',saving_basename='Humnews',frames_to_be_skipped=None)            
        except Exception as e:
            print(e)
        finally:
           release_connection(conn)

def aaj_news():
    while True :
        conn = get_connection()
       
        try:
            aaj_news= streamer(conn,source="udp://@238.190.1.25:5500",y1=314,y2=358,x1=0,x2=506,folder_save='Aaj_Ticker',image_name='aajframe.jpg',channel_name='Aaj',channel_logo='aaj.png',saving_basename='Aajnews',frames_to_be_skipped=None)            
        except Exception as e:
            print(e)
        finally:
           release_connection(conn)

def dawn_news():
    while True :
        conn = get_connection()
        
        try:
            dawn_news= streamer(conn,source="udp://@238.190.1.84:5500",y1=294,y2=330,x1=0,x2=528,folder_save='Dawn_Ticker',channel_name='Dawn',image_name='dawnframe.jpg',channel_logo='dawn.png',saving_basename='Dawnnews',frames_to_be_skipped=None)            
        except Exception as e:
            print(e)
        finally:
           release_connection(conn)


def ptv_news():
    while True :
        conn = get_connection()
        
        try:
            ptv_news= streamer(conn,source="udp://@238.190.1.28:5500",y1=318,y2=354,x1=0,x2=555,folder_save='Ptv_Ticker',image_name='ptvframe.jpg',channel_name='Ptv',channel_logo='ptv.png',saving_basename='Ptvnews',frames_to_be_skipped=None)            
        except Exception as e:
            print(e)
        finally:
           release_connection(conn)

def neo_news():
    while True :
        conn = get_connection()
        
        try:
            neo_news= streamer(conn,source="udp://@238.190.1.180:5500",y1=304,y2=343,x1=30,x2=530,folder_save='Neo_Ticker',image_name='neoframe.jpg',channel_name='Neo',channel_logo='neo.png',saving_basename='Neonews',frames_to_be_skipped=None)            
        except Exception as e:
            print(e)
        finally:
           release_connection(conn)
# from concurrent.futures import ThreadPoolExecutor




def running_all_time():
        # ninety_two_ticker()
        
        p1=threading.Thread(target=dunya_ticker)
        p2=threading.Thread(target=ary_ticker)
        p3=threading.Thread(target=express_ticker)
        p4=threading.Thread(target=samaa_ticker)
        p5=threading.Thread(target=geo_ticker)
        # p6=threading.Thread(target=aljazeera)
        # p7=threading.Thread(target=india_today)
        p8=threading.Thread(target=ninety_two_news)
        p9=threading.Thread(target=twenty_four_news)
        p10=threading.Thread(target=gnn_news)

        # p11=threading.Thread(target=hum_news)

        # p12=threading.Thread(target=aaj_news)
        p13=threading.Thread(target=dawn_news)
        p14=threading.Thread(target=ptv_news)
        # p15=threading.Thread(target=neo_news)

        # p8=threading.Thread(target=cnn)
        # p9=threading.Thread(target=rt)
        # p10=threading.Thread(target=bbc)


        # p7=threading.Thread(target=express_ticker_ocr)

        p1.start()
        p2.start()
        p3.start()
        p4.start()
        p5.start()
        # p6.start()
        # p7.start()
        p8.start()
        p9.start()
        p10.start()
        # p11.start()
        # p12.start()
        p13.start()
        p14.start()
        # p15.start()

        p1.join()
        p2.join()
        p3.join()
        p4.join()
        p5.join()
        # p6.join()
        # p7.join()
        p8.join()
        p9.join()
        p10.join()
        # p11.join()
        # p12.join()
        p13.join()
        p14.join()
        # p15.join()
#

        
        return 'Done'

if __name__ == "__main__":
    conn = get_connection()

    running_all_time()