from django.shortcuts import render
from django.http import JsonResponse
import glob
import os
import json
# from google_ocr.ocr import Drive_OCR

from django.views.decorators.csrf import csrf_exempt
import uuid
import cv2
# import pafy
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import word_to_be_searched_form
from .models import Ticker_Extraction_Model,words_to_be_searched_model
import time
from django.db.models import Q

import requests
from django.core.paginator import Paginator
import random
import string
import os
import datetime
import shutil
from rapidfuzz import fuzz
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
import re
import numpy as np
import ffmpeg
from celery import shared_task
import requests
# import subprocess
# @shared_task
# def streamer(source,y1,y2,x1,x2,folder_save,image_name,channel_name,channel_logo,saving_basename,):

    
#     print(' I am running')

#     date=datetime.datetime.now().date()
#     timeticker=datetime.datetime.now().time()
#     formatted_time = timeticker.strftime("%I:%M %p")
   
#     start_time = time.time()  # Get the current time
#     # if not os.path.exists(f'{folder_save}'):
#     #     os.mkdir(f'{folder_save}')
#     video_url = source

#     # Run the ffmpeg command to extract a frame at 00:00:01 (1 seconds)
#     output_filename = f"frames/{image_name}"
#     command = [
#         r"D:\ffmpeg\bin\ffmpeg.exe",
#         "-i", video_url,
#         "-ss", "00:00:01",  # Specify the time offset (1 seconds)
#         "-frames:v", "1",   # Extract one frame
#         "-vf", f"scale=640:360",  # Resize to 640x360
#         "-y",               # Overwrite output file if it exists
#         output_filename
#     ]
#     print('I am before subprocess')
#     subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     image=cv2.imread(f'frames/{image_name}')
#     ticker=image[y1:y2,x1:x2]
#     characters = generate_unique_filename()
#     os.remove(output_filename)
#     file_name=f"D:/ummar/ticker_new/ticker_images/{folder_save}/{saving_basename+characters}.jpg"
#     cv2.imwrite(file_name, ticker)
#     # return characters

#     # Define the URL of the FastAPI endpoint
#     fastapi_url = "http://192.168.2.168:4000/extract_text/"  # Replace with the actual URL
#     api_key = "apikey1234"

#     # Create a dictionary with the file to be uploaded
#     files = {"file": open(rf"{file_name}", "rb")}

#     # Include the API key in the query parameters
#     params = {"api_key": api_key}

#     # Send the POST request with the API key
#     response = requests.post(fastapi_url, files=files, params=params)

#     # Check the response
#     if response.status_code == 200:
#         text_ticker = response.json().get("extracted_text")
#         print("Extracted Text:", text_ticker)
#     else:
#         print("Error:", response.text)

#     # text_ticker = read(f"D:/ummar/ticker_new/ticker_images/{folder_save}/{saving_basename + characters}.jpg")

#     # print('text_ticker',text_ticker)
#     all_objects = Ticker_Extraction_Model.objects.filter(channel_name=channel_name).order_by('-id')[:5]
#     if len(text_ticker)>6:
#         # if Ticker_Extraction_Model.objects.filter(text_ocr__iexact=text_ticker).exists():
        
#         ticker_write=True
#         # Compare text similarity with each object
#         for obj in all_objects:
#             similarity_ratio = fuzz.ratio(text_ticker, obj.text_ocr)
            
#             if similarity_ratio >= 80:
#                 os.remove(f"D:/ummar/ticker_new/ticker_images/{folder_save}/{saving_basename+characters}.jpg")
#                 print('I am similarity')
#                 ticker_write=False
#                 break
#                 # matching_objects.append(obj)
#                 # ticker_write=True
#         if ticker_write:
#             print('I am writing in database')
#             Ticker_Extraction_Model.objects.create(channel_name=channel_name,channel_image=channel_logo,ticker_image=f"{saving_basename+characters}.jpg",date=date,time=formatted_time,text_ocr=text_ticker)

@shared_task
def streamer(source, y1, y2, x1, x2, folder_save, channel_name, channel_logo, saving_basename):
    try:
        date = datetime.date.today()
        timeticker = datetime.datetime.now().strftime("%I:%M %p")
        start_time = time.time()
        video_url = source
        characters = generate_unique_filename()
        output_filename = os.path.join("frames", f"{characters}.jpg")

        # Use ffmpeg to extract a frame from the video
        ffmpeg.input(video_url, ss="00:00:01").output(output_filename, vf=f"scale=640:360", vframes=1).run(overwrite_output=True)

        image = cv2.imread(output_filename)
        ticker = image[y1:y2, x1:x2]

        file_name = fr"D:\ummar\ticker_new\ticker_images\{folder_save}\{saving_basename+characters}.jpg"
        cv2.imwrite(file_name, ticker)
        
           # Clean up resources (e.g., close files and remove temporary files)
        if os.path.exists(output_filename):
            os.remove(output_filename)

        fastapi_url = "http://192.168.2.168:5000/extract_text/"
        api_key = "apikey1234"

        files = {"file": open(file_name, "rb")}
        params = {"api_key": api_key}
        response = requests.post(fastapi_url, files=files, params=params)

        if response.status_code == 200:
            text_ticker = response.json().get("extracted_text")
        else:
            text_ticker = ""

        all_objects = Ticker_Extraction_Model.objects.filter(channel_name=channel_name).order_by('-id')[:5]

        if len(text_ticker) > 6:
            ticker_write = True
            for obj in all_objects:
                similarity_ratio = fuzz.ratio(text_ticker, obj.text_ocr)
                if similarity_ratio >= 80:
                    os.remove(file_name)
                    ticker_write = False
                    break

            if ticker_write:
                Ticker_Extraction_Model.objects.create(channel_name=channel_name, channel_image=channel_logo,
                                                      ticker_image=f"{saving_basename+characters}.jpg", date=date, time=timeticker,
                                                      text_ocr=text_ticker)


    except Exception as e:
        # Handle exceptions properly, e.g., log the error and clean up resources
        print(f"An error occurred: {e}")
  


# @shared_task
# def streamer(source,y1,y2,x1,x2,folder_save,channel_name,channel_logo,saving_basename):

    


#     date=datetime.datetime.now().date()
#     timeticker=datetime.datetime.now().time()
#     formatted_time = timeticker.strftime("%I:%M %p")
   
#     start_time = time.time()  # Get the current time
#     # # if not os.path.exists(f'{folder_save}'):
#     #     # os.mkdir(f'{folder_save}')
#     video_url = source
#     characters = generate_unique_filename()

#     output_filename = os.path.join("frames", f"{channel_name}.jpg")

#     # # Use ffmpeg-python to extract a frame from the video
#     (
#         ffmpeg.input(video_url, ss="00:00:01")
#         .output(output_filename, vf=f"scale=640:360", vframes=1)
#         .run(overwrite_output=True)
#     )
#     image=cv2.imread(f'frames/{channel_name}.jpg')
#     ticker=image[y1:y2,x1:x2]
#     # # os.remove(output_filename)
#     file_name=fr"D:\ummar\ticker_new\ticker_images\{folder_save}\{saving_basename+characters}.jpg"
#     cv2.imwrite(file_name, ticker)

#     # Define the URL of the FastAPI endpoint
#     fastapi_url = "http://192.168.2.168:1000/extract_text/"  # Replace with the actual URL
#     api_key = "apikey1234"
#     # file_name=r"D:\ummar\ticker_new\ticker_images\Ary_Ticker\Arynews0000bce4-c158-4e4b-8489-9563f46c1c9a.jpg"
#     # Create a dictionary with the file to be uploaded
#     files = {"file": open(rf"{file_name}", "rb")}

#     # Include the API key in the query parameters
#     params = {"api_key": api_key}

#     # Send the POST request with the API key
#     response = requests.post(fastapi_url, files=files, params=params)

#     # Check the response
#     if response.status_code == 200:
#         text_ticker = response.json().get("extracted_text")
#         print("Extracted Text:*******************************************************************", text_ticker)
#     else:
#         print("NOT WORKING:", response.text)

#     # text_ticker = read(f"ticker_images/{folder_save}/{saving_basename + characters}.jpg")

#     # print('text_ticker',text_ticker)
#     all_objects = Ticker_Extraction_Model.objects.filter(channel_name=channel_name).order_by('-id')[:5]
#     if len(text_ticker)>6:
        
#         ticker_write=True
#         for obj in all_objects:
#             similarity_ratio = fuzz.ratio(text_ticker, obj.text_ocr)
            
#             if similarity_ratio >= 80:
#                 os.remove(f"ticker_images/{folder_save}/{saving_basename+characters}.jpg")
#                 print('I am similarity')
#                 ticker_write=False
#                 break
#                 # matching_objects.append(obj)
#                 # ticker_write=True
#         if ticker_write:
#             print('I am writing in database')
#             Ticker_Extraction_Model.objects.create(channel_name=channel_name,channel_image=channel_logo,ticker_image=f"{saving_basename+characters}.jpg",date=date,time=formatted_time,text_ocr=text_ticker)
          
channel_mapping = {
            'all_channels': '',
            'geo_news': 'Geo',
            'ary_news': 'Ary',
            'samaa_news': 'Samaa',
            'express_news': 'Express',
            'dunya_news': 'Dunya',
            'india_today_news': 'IndiaToday',
            'aljazeera_news': 'Aljazeera',
            'cnn_news': 'Cnn',
            'rt_news': 'Rt',
            'bbc_news': 'Bbc',
            '24_news': 'Twenty_Four',
            '92_news': 'Ninety_Two',
            'gnn_news': 'Gnn',
            'hum_news': 'Hum',
            'ptv_news': 'Ptv',
            'dawn_news': 'Dawn',
            'neo_news': 'Neo',
            'aaj_news': 'Aaj',



        }
@csrf_exempt
def index(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        filters = data.get('filters', {})
        selected_channel_type = filters.get('selectedChannelType', 'localChannels')
        selected_channel_type = ''

        selected_channel = filters.get('selectedChannel', '')
        search_text = filters.get('searchText', '')
        print('search_text',search_text)
        start_date = filters.get('startDate', '')
        end_date = filters.get('endDate', '')
        start_time = filters.get('startTime', '')
        end_time = filters.get('endTime', '')
        old_data_count = filters.get('oldDataCount', None)
        keyword_cloud=filters.get('keywordCloud','')

        # Create a base queryset
        result = Ticker_Extraction_Model.objects.all().order_by('-id')  # Order by id in descending order

        selected_channel = channel_mapping.get(selected_channel, '')

        if selected_channel_type == 'localChannels':
            result = result.filter(channel_name__in=['Geo', 'Ary', 'Samaa', 'Express', 'Dunya', 'Twenty_Four', 'Ninety_Two', 'Gnn', 'Hum', 'Ptv', 'Dawn', 'Neo', 'Aaj'])

        if selected_channel_type == 'foreignChannels':
            result = result.filter(channel_name__in=['IndiaToday', 'Aljazeera', 'Cnn', 'Rt', 'Bbc'])

        if selected_channel:
            result = result.filter(channel_name=selected_channel)
        # Search for multiple words

        print('Search_word(s)', search_text)
        query = Q()  # Initialize an empty Q object
        search_words = search_text.split(',')
        for word in search_words:
            if word:
                query |= Q(text_ocr__icontains=word)  # Use "|" operator to combine queries with "OR" condition

                # result = result.filter(text_ocr__icontains=word)
        result = result.filter(query)

        # if search_text:
        #     result = result.filter(text_ocr__icontains=search_text)
  
        result = filter_by_date(result, start_date, end_date)
        if start_time or end_time:
           result = filter_by_time(result, start_time, end_time)
        if keyword_cloud:
            # data_result=[data.text_ocr for data in result]
            return JsonResponse({'tickers':  list(result.values()), 'channel_name': selected_channel})

        if old_data_count:
            data_result = list(result.values()[:old_data_count + 20])
            for entry in data_result:
                entry['time'] = convert_to_ampm_format(entry['time'])
        else:
            # Convert time to AM/PM format before sending the response
            data_result = list(result.values()[:20])
            for entry in data_result:
                entry['time'] = convert_to_ampm_format(entry['time'])

        return JsonResponse({'tickers': data_result, 'channel_name': selected_channel})

def convert_to_ampm_format(time_str):
    datetime_obj = datetime.datetime.strptime(time_str, '%H:%M:%S')
    ampm_time_str = datetime_obj.strftime('%I:%M %p')
    return ampm_time_str


def filter_by_date(result, start_date, end_date):
    if start_date and end_date:
        return result.filter(date__range=[start_date, end_date])
  
    elif start_date:
        return result.filter(date=start_date)
    elif end_date:
        return result.filter(date=end_date)
    else:
        return result

def filter_by_time(result, start_time, end_time):
    if start_time and end_time:
        return result.filter(time__range=(start_time, end_time))
    elif start_time:
        return result.filter(time__gte=start_time)
    elif end_time:
        return result.filter(time__lte=end_time)
    else:
        return result

    
    if start_time and end_time:
        # Perform range query
        result = result.filter(
            time__gte=start_time,
            time__lt=end_time
        )
        print(str(result.query))
        return result
    elif start_time:
        return result.filter(time=start_time)
    elif end_time:
        return result.filter(time=end_time)
    else:
        return result

    
def generate_unique_filename():
    unique_id = str(uuid.uuid4())
    valid_chars = string.ascii_letters + string.digits + "_-"
    filename = ''.join(c for c in unique_id if c in valid_chars)
    return filename

def file_remover(folder_name,extension_name,appended_file_name):
    # jpg_files = glob.glob('headline_checker/*.jpg')
    jpg_files = glob.glob(f'{folder_name}/*.jpg')

    sorted_files = sorted(jpg_files, key=lambda x: os.path.getctime(x))
    
    for i in sorted_files:
        print('os.path.basename(i[0:3])',os.path.basename(i)[0:3])
        # if os.path.basename(i)[0:3]=='Geo':
        if os.path.basename(i)[0:3]==extension_name:

            # geo_ticker_remove.append(i)
            appended_file_name.append(i)
    # print('geo_ticker_remove',geo_ticker_remove)
    if len(appended_file_name)>=100:
      for i in appended_file_name[0:96]:
          os.remove(i)

@csrf_exempt
def dunya_ticker(request):
    all_files_with_names_dunya={}
    all_files_with_names_dunya_list=[]

    date=datetime.datetime.now().date()
    timeticker=datetime.datetime.now().time()
    formatted_time = timeticker.strftime("%I:%M %p")
   
    start_time = time.time()  # Get the current time

    
    all_objects = Ticker_Extraction_Model.objects.filter(channel_name='Dunya').order_by('-id')[:20]
   

    for v, i in enumerate(all_objects):
        # file_name=os.path.basename(i)
        all_files_with_names_dunya[f'data_{v}'] = {
            'id': i.id, 'channel_image': i.channel_image, 'ticker_image': i.ticker_image, 'date': i.date, 'time': convert_to_ampm_format(i.time),'text_ocr': i.text_ocr}
    for key,val in all_files_with_names_dunya.items():
        all_files_with_names_dunya_list.append(val)

    end_time = time.time()  # Get the current time after the task is completed
    execution_time = end_time - start_time  # Calculate the execution time

    # print(f"Function executed in {execution_time:.2f} seconds")
    return JsonResponse({'tickers':all_files_with_names_dunya_list})

@csrf_exempt
def all_ticker(request):
    start_time = time.time()  # Get the current time
    date=datetime.datetime.now().date()
    timeticker=datetime.datetime.now().time()
    formatted_time = timeticker.strftime("%I:%M %p")
 
   
    all_files_with_names_all_channels={}
    all_files_with_names_all_channels_list=[]

    all_objects_ten = Ticker_Extraction_Model.objects.filter(channel_name__in=['Geo', 'Ary', 'Samaa', 'Express', 'Dunya','Twenty_Four','Ninety_Two','Gnn','Hum','Ptv','Dawn','Neo','Aaj']).order_by('-id')[:10]

    for v, i in enumerate(all_objects_ten):
        # file_name=os.path.basename(i)
        all_files_with_names_all_channels[f'data_{v}'] = {
            'id': i.id, 'channel_image': i.channel_image, 'ticker_image': i.ticker_image, 'date': i.date, 'time': i.time,'text_ocr': i.text_ocr}
    for key,val in all_files_with_names_all_channels.items():
        all_files_with_names_all_channels_list.append(val)

    end_time = time.time()  # Get the current time after the task is completed
    execution_time = end_time - start_time  # Calculate the execution time

    # print(f"Function executed in {execution_time:.2f} seconds")
    return JsonResponse({'tickers':all_files_with_names_all_channels_list})
   
@csrf_exempt
def geo_ticker(request):
    start_time = time.time()  # Get the current time
    date=datetime.datetime.now().date()
    timeticker=datetime.datetime.now().time()
    formatted_time = timeticker.strftime("%I:%M %p")
 
   
    all_files_with_names_geo={}
    all_files_with_names_geo_list=[]

    all_objects_ten = Ticker_Extraction_Model.objects.filter(channel_name='Geo').order_by('-id')[:10]

    for v, i in enumerate(all_objects_ten):
        # file_name=os.path.basename(i)
        all_files_with_names_geo[f'data_{v}'] = {
            'id': i.id, 'channel_image': i.channel_image, 'ticker_image': i.ticker_image, 'date': i.date, 'time': convert_to_ampm_format(i.time),'text_ocr': i.text_ocr}
    for key,val in all_files_with_names_geo.items():
        all_files_with_names_geo_list.append(val)

    end_time = time.time()  # Get the current time after the task is completed
    execution_time = end_time - start_time  # Calculate the execution time

    # print(f"Function executed in {execution_time:.2f} seconds")
    return JsonResponse({'tickers':all_files_with_names_geo_list})
   
result_all=[]

@csrf_exempt
def ary_ticker(request):
    
    all_files_with_names_ary={}
    all_files_with_names_ary_list=[]


    start_time = time.time()  # Get the current time

    date=datetime.datetime.now().date()
    timeticker=datetime.datetime.now().time()
    formatted_time = timeticker.strftime("%I:%M %p") 

    all_objects_ten = Ticker_Extraction_Model.objects.filter(channel_name="Ary").order_by('-id')[:20]
    
    for v, i in enumerate(all_objects_ten):
        # file_name=os.path.basename(i)
        all_files_with_names_ary[f'data_{v}'] = {
            'id': i.id, 'channel_image': i.channel_image, 'ticker_image': i.ticker_image, 'date': i.date, 'time': i.time,'text_ocr': i.text_ocr}
    for key,val in all_files_with_names_ary.items():
        all_files_with_names_ary_list.append(val)

    end_time = time.time()  # Get the current time after the task is completed
    execution_time = end_time - start_time  # Calculate the execution time

    # print(f"Function executed in {execution_time:.2f} seconds")
    return JsonResponse({'tickers':all_files_with_names_ary_list})


@csrf_exempt
def samaa_ticker(request):
    all_files_with_names_samaa={}
    all_files_with_names_samaa_list=[]
    start_time = time.time()  # Get the current time

    date=datetime.datetime.now().date()
    timeticker=datetime.datetime.now().time()
    formatted_time = timeticker.strftime("%I:%M %p")   
              

  
    all_objects_ten = Ticker_Extraction_Model.objects.filter(channel_name="Samaa").order_by('-id')[:20]
   
    for v, i in enumerate(all_objects_ten):
        # file_name=os.path.basename(i)
        all_files_with_names_samaa[f'data_{v}'] = {
            'id': i.id, 'channel_image': i.channel_image, 'ticker_image': i.ticker_image, 'date': i.date, 'time': i.time,'text_ocr': i.text_ocr}
    for key,val in all_files_with_names_samaa.items():
        all_files_with_names_samaa_list.append(val)

    end_time = time.time()  # Get the current time after the task is completed
    execution_time = end_time - start_time  # Calculate the execution time

    # print(f"Function executed in {execution_time:.2f} seconds")
    return JsonResponse({'tickers':all_files_with_names_samaa_list})

@csrf_exempt
def express_ticker(request):
    current_count_express = request.session.get('counter', 0)

    new_count = current_count_express + 1
    timedata_express=[]
    all_files_with_names_express={}
    all_files_with_names_express_list=[]
    start_time = time.time()  # Get the current time

    date=datetime.datetime.now().date()
    timeticker=datetime.datetime.now().time()
    formatted_time = timeticker.strftime("%I:%M %p")

    all_objects_ten = Ticker_Extraction_Model.objects.filter(channel_name='Express').order_by('-id')[:20]

    for v, i in enumerate(all_objects_ten):
        # file_name=os.path.basename(i)
        all_files_with_names_express[f'data_{v}'] = {
            'id': i.id, 'channel_image': i.channel_image, 'ticker_image': i.ticker_image, 'date': i.date, 'time': i.time,'text_ocr': i.text_ocr}
    for key,val in all_files_with_names_express.items():
        all_files_with_names_express_list.append(val)

    end_time = time.time()  # Get the current time after the task is completed
    execution_time = end_time - start_time  # Calculate the execution time

    # print(f"Function executed in {execution_time:.2f} seconds")
    return JsonResponse({'tickers':all_files_with_names_express_list})

@csrf_exempt
def india_today_ticker(request):
    all_files_with_names_india_today_news={}
    all_files_with_names_india_today_list=[]
    date=datetime.datetime.now().date()
    all_objects=Ticker_Extraction_Model.objects.filter(channel_name='IndiaToday').order_by('-id')[:10]
    for v, i in enumerate(all_objects):
        # file_name=os.path.basename(i)
        all_files_with_names_india_today_news[f'data_{v}'] = {
            'id': i.id, 'channel_image': i.channel_image, 'ticker_image': i.ticker_image, 'date': i.date, 'time': i.time,'text_ocr': i.text_ocr}
    for key,val in all_files_with_names_india_today_news.items():
        all_files_with_names_india_today_list.append(val)
    return JsonResponse({'tickers':all_files_with_names_india_today_list})

@csrf_exempt
def aljazeera_ticker(request):
    all_files_with_names_aljazeera_news={}
    all_files_with_names_aljazeera_list=[]
    date=datetime.datetime.now().date()
    all_objects=Ticker_Extraction_Model.objects.filter(channel_name='aljazeera').order_by('-id')[:10]
    for v, i in enumerate(all_objects):
        # file_name=os.path.basename(i)
        all_files_with_names_aljazeera_news[f'data_{v}'] = {
            'id': i.id, 'channel_image': i.channel_image, 'ticker_image': i.ticker_image, 'date': i.date, 'time': i.time,'text_ocr': i.text_ocr}
    for key,val in all_files_with_names_aljazeera_news.items():
        all_files_with_names_aljazeera_list.append(val)
    return JsonResponse({'tickers':all_files_with_names_aljazeera_list})



# Foreign Channels


@csrf_exempt
def cnn_ticker(request):
    all_files_with_names_cnn_news={}
    all_files_with_names_cnn_list=[]

    all_objects = Ticker_Extraction_Model.objects.filter(channel_name='Cnn').order_by('-id')[:10]
    for v, i in enumerate(all_objects):
        # file_name=os.path.basename(i)
        all_files_with_names_cnn_news[f'data_{v}'] = {
            'id': i.id, 'channel_image': i.channel_image, 'ticker_image': i.ticker_image, 'date': i.date, 'time': i.time,'text_ocr': i.text_ocr}
    for key,val in all_files_with_names_cnn_news.items():
        all_files_with_names_cnn_list.append(val)

    return JsonResponse({'tickers':all_files_with_names_cnn_list})


@csrf_exempt
def rt_ticker(request):
    all_files_with_names_rt_news={}
    all_files_with_names_rt_list=[]
    
    all_objects = Ticker_Extraction_Model.objects.filter(channel_name='Rt').order_by('-id')[:10]
    for v, i in enumerate(all_objects):
        # file_name=os.path.basename(i)
        all_files_with_names_rt_news[f'data_{v}'] = {
            'id': i.id, 'channel_image': i.channel_image, 'ticker_image': i.ticker_image, 'date': i.date, 'time': i.time,'text_ocr': i.text_ocr}
    for key,val in all_files_with_names_rt_news.items():
        all_files_with_names_rt_list.append(val)
    return JsonResponse({'tickers':all_files_with_names_rt_list})

@csrf_exempt
def bbc_ticker(request):
    all_files_with_names_bbc_news={}
    all_files_with_names_bbc_list=[]
  # Get the current time
    all_objects = Ticker_Extraction_Model.objects.filter(channel_name='Bbc').order_by('-id')[:10]
    for v, i in enumerate(all_objects):
        # file_name=os.path.basename(i)
        all_files_with_names_bbc_news[f'data_{v}'] = {
            'id': i.id, 'channel_image': i.channel_image, 'ticker_image': i.ticker_image, 'date': i.date, 'time': i.time,'text_ocr': i.text_ocr}
    for key,val in all_files_with_names_bbc_news.items():
        all_files_with_names_bbc_list.append(val)
    return JsonResponse({'tickers':all_files_with_names_bbc_list})


@csrf_exempt
def notifications(request):
    receiving_word=json.loads(request.body)
    get_words=receiving_word.get('wordsList',[])

    # Retrieve data from the session or initialize if not present
    session_data = request.session.get('notifications_data', {
        'clear_list_and_word': False,
        'notifications_list': [],
        'official_result': [],
        'official_word': [],
    })

    clear_list_and_word = session_data['clear_list_and_word']
    notifications_list = session_data['notifications_list']
    official_result = session_data['official_result']
    official_word = session_data['official_word']

    if clear_list_and_word:
            official_result.clear()
            official_word.clear()
            clear_list_and_word = False

    notification_increment = True
    length = 0
    length_all = 0
    date = datetime.datetime.now().date()
    all_ids=[]


    try:
        notifications_list_int_ids=[int(id) for id in notifications_list]
        max_id=max(notifications_list_int_ids)
    except:
        max_id=0
    if len(get_words) >= 1:
        results_dict = {}

        for i in get_words:
            results = Ticker_Extraction_Model.objects.filter(text_ocr__icontains=i, date=date).order_by('-id').values()
            length_all += len(results)
            data = list(results)
            results_dict[i] = data
         
        for word, data_list in results_dict.items():
            if data_list:
                all_words_list_of_dict = data_list
                for i in all_words_list_of_dict:
                    if i not in official_result and int(i['id']) > max_id and not clear_list_and_word:
                        all_ids.append(i['id'])
                        official_result.append(i)
                        official_word.append(word)
            # else:
                # print(f"No data found for '{word}'")

        length = len(official_result)

        # Update the session data with the latest values
        request.session['notifications_data'] = {
            'clear_list_and_word': clear_list_and_word,
            'notifications_list': notifications_list,
            'official_result': official_result,
            'official_word': official_word,
        }

        return JsonResponse({'notification_data': official_result})
    else:
        return JsonResponse({'error': 'error'})

# @csrf_exempt
# def notifications(request):
#     receiving_word=json.loads(request.body)
#     get_words=receiving_word.get('wordsList',[])

#     # Retrieve data from the session or initialize if not present
#     session_data = request.session.get('notifications_data', {
#         'clear_list_and_word': False,
#         'notifications_list': [],
#         'official_result': [],
#         'official_word': [],
#     })

#     clear_list_and_word = session_data['clear_list_and_word']
#     notifications_list = session_data['notifications_list']
#     official_result = session_data['official_result']
#     official_word = session_data['official_word']

#     if clear_list_and_word:
#             official_result.clear()
#             official_word.clear()
#             clear_list_and_word = False

#     notification_increment = True
#     length = 0
#     length_all = 0
#     date = datetime.datetime.now().date()
#     all_ids=[]


#     try:
#         notifications_list_int_ids=[int(id) for id in notifications_list]
#         max_id=max(notifications_list_int_ids)
#     except:
#         max_id=0
#     if len(get_words) >= 1:
#         results_dict = {}

#         for i in get_words:
#             results = Ticker_Extraction_Model.objects.filter(text_ocr__icontains=i, date=date).order_by('-id').values()
#             length_all += len(results)
#             data = list(results)
#             results_dict[i] = data
         
#         for word, data_list in results_dict.items():
#             if data_list:
#                 all_words_list_of_dict = data_list
#                 for i in all_words_list_of_dict:
#                     if i not in official_result and int(i['id']) > max_id and not clear_list_and_word:
#                         all_ids.append(i['id'])
#                         official_result.append(i)
#                         official_word.append(word)
#             # else:
#                 # print(f"No data found for '{word}'")

#         length = len(official_result)

#         # Update the session data with the latest values
#         request.session['notifications_data'] = {
#             'clear_list_and_word': clear_list_and_word,
#             'notifications_list': notifications_list,
#             'official_result': official_result,
#             'official_word': official_word,
#         }

#         return JsonResponse({'notification_data': official_result})
#     else:
#         return JsonResponse({'error': 'error'})

@csrf_exempt
def list_clearer(request):
    if request.method == "POST":
        data = json.loads(request.body)
        notificationIds = data['notificationIds']

        request.session['notifications_data'] = {
            'clear_list_and_word': True,
            'notifications_list': notificationIds,
            'official_result': [],
            'official_word': [],
        }

        return JsonResponse({'success': 'success'})
    else:
        return JsonResponse({'error': 'error'})



@csrf_exempt
def twenty_four_ticker(request):
    
    all_files_with_names_twenty_four={}
    all_files_with_names_twenty_four_list=[]


    start_time = time.time()  # Get the current time

    date=datetime.datetime.now().date()
    timeticker=datetime.datetime.now().time()
    formatted_time = timeticker.strftime("%I:%M %p") 

    all_objects_ten = Ticker_Extraction_Model.objects.filter(channel_name="Twenty_Four").order_by('-id')[:20]
    
    for v, i in enumerate(all_objects_ten):
        # file_name=os.path.basename(i)
        all_files_with_names_twenty_four[f'data_{v}'] = {
            'id': i.id, 'channel_image': i.channel_image, 'ticker_image': i.ticker_image, 'date': i.date, 'time': i.time,'text_ocr': i.text_ocr}
    for key,val in all_files_with_names_twenty_four.items():
        all_files_with_names_twenty_four_list.append(val)

    end_time = time.time()  # Get the current time after the task is completed
    execution_time = end_time - start_time  # Calculate the execution time

    # print(f"Function executed in {execution_time:.2f} seconds")
    return JsonResponse({'tickers':all_files_with_names_twenty_four_list})   




@csrf_exempt
def gnn_ticker(request):
    
    all_files_with_names_gnn={}
    all_files_with_names_gnn_list=[]


    start_time = time.time()  # Get the current time

    date=datetime.datetime.now().date()
    timeticker=datetime.datetime.now().time()
    formatted_time = timeticker.strftime("%I:%M %p") 

    all_objects_ten = Ticker_Extraction_Model.objects.filter(channel_name="Gnn").order_by('-id')[:20]
    
    for v, i in enumerate(all_objects_ten):
        # file_name=os.path.basename(i)
        all_files_with_names_gnn[f'data_{v}'] = {
            'id': i.id, 'channel_image': i.channel_image, 'ticker_image': i.ticker_image, 'date': i.date, 'time': i.time,'text_ocr': i.text_ocr}
    for key,val in all_files_with_names_gnn.items():
        all_files_with_names_gnn_list.append(val)

    end_time = time.time()  # Get the current time after the task is completed
    execution_time = end_time - start_time  # Calculate the execution time

    # print(f"Function executed in {execution_time:.2f} seconds")
    return JsonResponse({'tickers':all_files_with_names_gnn_list})





@csrf_exempt
def hum_ticker(request):
    
    all_files_with_names_hum={}
    all_files_with_names_hum_list=[]


    start_time = time.time()  # Get the current time

    date=datetime.datetime.now().date()
    timeticker=datetime.datetime.now().time()
    formatted_time = timeticker.strftime("%I:%M %p") 

    all_objects_ten = Ticker_Extraction_Model.objects.filter(channel_name="Hum").order_by('-id')[:20]
    
    for v, i in enumerate(all_objects_ten):
        # file_name=os.path.basename(i)
        all_files_with_names_hum[f'data_{v}'] = {
            'id': i.id, 'channel_image': i.channel_image, 'ticker_image': i.ticker_image, 'date': i.date, 'time': i.time,'text_ocr': i.text_ocr}
    for key,val in all_files_with_names_hum.items():
        all_files_with_names_hum_list.append(val)

    end_time = time.time()  # Get the current time after the task is completed
    execution_time = end_time - start_time  # Calculate the execution time

    # print(f"Function executed in {execution_time:.2f} seconds")
    return JsonResponse({'tickers':all_files_with_names_hum_list})    




@csrf_exempt
def aaj_ticker(request):
    
    all_files_with_names_aaj={}
    all_files_with_names_aaj_list=[]


    start_time = time.time()  # Get the current time

    date=datetime.datetime.now().date()
    timeticker=datetime.datetime.now().time()
    formatted_time = timeticker.strftime("%I:%M %p") 

    all_objects_ten = Ticker_Extraction_Model.objects.filter(channel_name="Aaj").order_by('-id')[:20]
    
    for v, i in enumerate(all_objects_ten):
        # file_name=os.path.basename(i)
        all_files_with_names_aaj[f'data_{v}'] = {
            'id': i.id, 'channel_image': i.channel_image, 'ticker_image': i.ticker_image, 'date': i.date, 'time': i.time,'text_ocr': i.text_ocr}
    for key,val in all_files_with_names_aaj.items():
        all_files_with_names_aaj_list.append(val)

    end_time = time.time()  # Get the current time after the task is completed
    execution_time = end_time - start_time  # Calculate the execution time

    # print(f"Function executed in {execution_time:.2f} seconds")
    return JsonResponse({'tickers':all_files_with_names_aaj_list})   




@csrf_exempt
def dawn_ticker(request):
    
    all_files_with_names_dawn={}
    all_files_with_names_dawn_list=[]


    start_time = time.time()  # Get the current time

    date=datetime.datetime.now().date()
    timeticker=datetime.datetime.now().time()
    formatted_time = timeticker.strftime("%I:%M %p") 

    all_objects_ten = Ticker_Extraction_Model.objects.filter(channel_name="Dawn").order_by('-id')[:20]
    
    for v, i in enumerate(all_objects_ten):
        # file_name=os.path.basename(i)
        all_files_with_names_dawn[f'data_{v}'] = {
            'id': i.id, 'channel_image': i.channel_image, 'ticker_image': i.ticker_image, 'date': i.date, 'time': i.time,'text_ocr': i.text_ocr}
    for key,val in all_files_with_names_dawn.items():
        all_files_with_names_dawn_list.append(val)

    end_time = time.time()  # Get the current time after the task is completed
    execution_time = end_time - start_time  # Calculate the execution time

    # print(f"Function executed in {execution_time:.2f} seconds")
    return JsonResponse({'tickers':all_files_with_names_dawn_list})   




@csrf_exempt
def ptv_ticker(request):
    
    all_files_with_names_ptv={}
    all_files_with_names_ptv_list=[]


    start_time = time.time()  # Get the current time

    date=datetime.datetime.now().date()
    timeticker=datetime.datetime.now().time()
    formatted_time = timeticker.strftime("%I:%M %p") 

    all_objects_ten = Ticker_Extraction_Model.objects.filter(channel_name="Ptv").order_by('-id')[:20]
    
    for v, i in enumerate(all_objects_ten):
        # file_name=os.path.basename(i)
        all_files_with_names_ptv[f'data_{v}'] = {
            'id': i.id, 'channel_image': i.channel_image, 'ticker_image': i.ticker_image, 'date': i.date, 'time': i.time,'text_ocr': i.text_ocr}
    for key,val in all_files_with_names_ptv.items():
        all_files_with_names_ptv_list.append(val)

    end_time = time.time()  # Get the current time after the task is completed
    execution_time = end_time - start_time  # Calculate the execution time

    # print(f"Function executed in {execution_time:.2f} seconds")
    return JsonResponse({'tickers':all_files_with_names_ptv_list})   





@csrf_exempt
def neo_ticker(request):
    
    all_files_with_names_neo={}
    all_files_with_names_neo_list=[]


    start_time = time.time()  # Get the current time

    date=datetime.datetime.now().date()
    timeticker=datetime.datetime.now().time()
    formatted_time = timeticker.strftime("%I:%M %p") 

    all_objects_ten = Ticker_Extraction_Model.objects.filter(channel_name="Neo").order_by('-id')[:20]
    
    for v, i in enumerate(all_objects_ten):
        # file_name=os.path.basename(i)
        all_files_with_names_neo[f'data_{v}'] = {
            'id': i.id, 'channel_image': i.channel_image, 'ticker_image': i.ticker_image, 'date': i.date, 'time': i.time,'text_ocr': i.text_ocr}
    for key,val in all_files_with_names_neo.items():
        all_files_with_names_neo_list.append(val)

    end_time = time.time()  # Get the current time after the task is completed
    execution_time = end_time - start_time  # Calculate the execution time

    # print(f"Function executed in {execution_time:.2f} seconds")
    return JsonResponse({'tickers':all_files_with_names_neo_list})   


   
@csrf_exempt
def ninety_two_ticker(request):
    
    all_files_with_names_ninety_two={}
    all_files_with_names_ninety_two_list=[]


    start_time = time.time()  # Get the current time

    date=datetime.datetime.now().date()
    timeticker=datetime.datetime.now().time()
    formatted_time = timeticker.strftime("%I:%M %p") 

    all_objects_ten = Ticker_Extraction_Model.objects.filter(channel_name="Ninety_Two").order_by('-id')[:20]
    
    for v, i in enumerate(all_objects_ten):
        # file_name=os.path.basename(i)
        all_files_with_names_ninety_two[f'data_{v}'] = {
            'id': i.id, 'channel_image': i.channel_image, 'ticker_image': i.ticker_image, 'date': i.date, 'time': i.time,'text_ocr': i.text_ocr}
    for key,val in all_files_with_names_ninety_two.items():
        all_files_with_names_ninety_two_list.append(val)

    end_time = time.time()  # Get the current time after the task is completed
    execution_time = end_time - start_time  # Calculate the execution time

    # print(f"Function executed in {execution_time:.2f} seconds")
    return JsonResponse({'tickers':all_files_with_names_ninety_two_list})   
 
import nltk
nltk.download("punkt")
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
from collections import Counter
# from django.http import JsonResponse
# from .models import Ticker_Extraction_Model
from django.db.models import Q

common_conjunctions_urdu = [
    'اور', 'یا', 'لیکن', 'مگر', 'کیوں کہ', 'چونکہ', 'کہ', 'جب تک', 'کہاں تک', 'اگر', 'جیسا کہ',
    'لہٰذا', 'اس لئے', 'استمبالکہ', 'یعنی', 'اگرچہ', 'یوں تو', 'تاکہ', 'اگرچہ کہ', 'جو بھی', 'یاہو',
    'جیسے', 'خواہش کے برعکس', 'خلاف', 'مخالفت کے برعکس', 'کی بجائے', 'کہتے ہیں کہ',
    'ہاں', 'نہیں', 'مگر', 'تاہم', 'لیکن', 'لہٰذا', 'مگر', 'مگرچہ', 'اگرچہ', 'مگر کہ', 'چاہے کہ',
    'چاہوں کہ', 'تاکہ', 'یہاں تک کہ', 'کی بجائے', 'تاہم', 'کی بجائے', 'جب تک کہ', 'کی بجائے', 'ہاں',
    'میں تو', 'مگر تم تو', 'لیکن تم تو', 'مگر ہم تو', 'یہ بات ہے کہ', 'لیکن یہ بات ہے کہ',
    'اور', 'یا', 'لیکن', 'مگر', 'کیوں کہ', 'میں', 'نہ', 'سے',
    'کے', 'کا', 'کی', 'کو', 'کہ', 'میں', 'نے', 'سے', 'ہوتا', 'ہوتی', 'ہوتے',
    'یہ', 'وہ', 'ایک', 'ایسا', 'واحد', 'ذرا', 'جب', 'کب', 'کیوں', 'کیا',
    'تو', 'بھی', 'جیسا', 'جیسے', 'اور', 'یا', 'لیکن', 'مگر', 'لہٰذا',
    'میں', 'نہ', 'اگر', 'ہو', 'رہا', 'رہی', 'رہے', 'رہتا', 'رہتی', 'رہتے',
    'ہوا', 'ہوئی', 'ہوئے', 'ہوتا', 'ہوتی', 'ہوتے', 'ہوگا', 'ہوگی', 'ہوگے',
    'تھا', 'تھی', 'تھے', 'گیا', 'گئی', 'گئے', 'جائے', 'گا', 'گی', 'گے',
    'کر', 'کرتا', 'کرتی', 'کرتے', 'کیا', 'کرنا', 'کرتے', 'کرنے', 'کریں',
    'کیوںکہ', 'کیونکہ', 'تاکہ', 'تاکے', 'چاہئے', 'چاہتا', 'چاہتی', 'چاہتے',
    'ہوشک', 'نہیں', 'کیسا', 'کیسی', 'کیسے', 'و', 'نے', 'نیچے', 'سوال', 'کیونکہ',
    'اب', 'ابھی', 'آپ', 'آپکا', 'آپکی', 'آگئے'
    ]
@csrf_exempt
def trending_words_local(request):
 


    date=datetime.datetime.now().date()
    current_time = datetime.datetime.now()
    new_time = current_time - datetime.timedelta(hours=1)
    
    getting_six_hours_object = Ticker_Extraction_Model.objects.filter(Q(channel_name='Geo') | Q(channel_name='Ary') | Q(channel_name='Samaa') | Q(channel_name='Express') | Q(channel_name='Dunya'),date=date,time__range=(new_time.time(), current_time.time()))
    if not getting_six_hours_object:
            getting_six_hours_object = Ticker_Extraction_Model.objects.filter(Q(channel_name='Geo') | Q(channel_name='Ary') | Q(channel_name='Samaa') | Q(channel_name='Express') | Q(channel_name='Dunya'),date=date).order_by('-id')[:50]

    # Create a dictionary to keep track of phrase frequencies
    trending_phrases = Counter()
    # Dictionary to store n-grams and their associated objects
    ngram_objects = {}

    # Helper function to check if a 3-gram contains a 2-gram
    def is_similar_2gram(ngram):
        for i in range(len(ngram) - 1):
            if ' '.join(ngram[i:i+2]) in ngram_objects:
                return True
        return False
    for obj in getting_six_hours_object:
        if obj.text_ocr:

            getting_split_words = obj.text_ocr
            getting_split_words = re.sub(r'[^\w\sءاآأؤإئابةتثجحخدذرزسشصضطظعغفقكلمنهوىيa-zA-Z]', '', getting_split_words)
            words_tokenized = word_tokenize(getting_split_words)
            if ':' in words_tokenized and words_tokenized.index(':') == 1:
                phrase_text = words_tokenized[0]
                trending_phrases.update([phrase_text])

            # Extract words before colons and after commas in Urdu text
            urdu_pattern = r'(\w+),|(\w+):'
            matches = re.findall(urdu_pattern, getting_split_words, re.UNICODE)

            for n in range(2, 4):
                ngram_list = list(ngrams(words_tokenized, n))
                for ngram in ngram_list:
                    if all(word not in common_conjunctions for word in ngram):
                        if n == 3 and is_similar_2gram(ngram):
                            continue  # Skip 2-grams similar to 3-grams
                        phrase_text = ' '.join(ngram)
                        trending_phrases.update([phrase_text])
                        if phrase_text not in ngram_objects:
                            ngram_objects[phrase_text] = []
                        ngram_objects[phrase_text].append(obj)
    # Create a list to store common phrases and their associated objects in the desired structure
    trending_words_list = []
    for phrase, count in trending_phrases.items():
        objects_info = []
        for obj in ngram_objects.get(phrase, []):
            obj_info = {
                'id': obj.id,
                'channel_name': obj.channel_name,
                'channel_image': obj.channel_image,
                'ticker_image': obj.ticker_image,
                'date': obj.date,
                'time': obj.time,
                'text_ocr': obj.text_ocr,
            }
            objects_info.append(obj_info)
        trending_words_list.append({'text': phrase, 'value': count, 'objects': objects_info})
    trending_words_list = sorted(trending_words_list, key=lambda x: x['value'], reverse=True)
    print('trending_word_list',trending_words_list)
    return JsonResponse({'trending_words': trending_words_list[:50]})




common_conjunctions_english = [
        'and',
        'but',
        'or',
        'nor',
        'for',
        'so',
        'yet',
        'although',
        'because',
        'since',
        'unless',
        'while',
        'after',
        'before',
        'if',
        'though',
        'until',
        'whether',
        'as',
        'even though',
        'either',
        'neither',
        'not only',
        'rather than',
        'both',
        'so that'
    ]



    
@csrf_exempt
def keywords_cloud_local(request):
 

    if request.method=='POST':
        data=json.loads(request.body.decode('utf-8'))
        hour=data.get('hour','')
        if hour:
            interval=int(hour)
        else:
            interval=1
        print('hour',hour)
        # Create a dictionary to keep track of phrase frequencies
        trending_phrases = Counter()
        # Dictionary to store n-grams and their associated objects
        ngram_objects = {}
        keywords_cloud_list = []

        def database_grams_keyword_cloud(objects):

            # Helper function to check if a 3-gram contains a 2-gram
            def is_similar_2gram(ngram):
                for i in range(len(ngram) - 1):
                    if ' '.join(ngram[i:i+2]) in ngram_objects:
                        return True
                return False
            for obj in objects:
                if obj.text_ocr:

                    getting_split_words = obj.text_ocr
                    getting_split_words = re.sub(r'[^\w\sءاآأؤإئابةتثجحخدذرزسشصضطظعغفقكلمنهوىيa-zA-Z]', '', getting_split_words)
                    words_tokenized = word_tokenize(getting_split_words)
                    if ':' in words_tokenized and words_tokenized.index(':') == 1:
                        phrase_text = words_tokenized[0]
                        trending_phrases.update([phrase_text])

                    # Extract words before colons and after commas in Urdu text
                    urdu_pattern = r'(\w+),|(\w+):'
                    matches = re.findall(urdu_pattern, getting_split_words, re.UNICODE)

                    for n in range(2, 4):
                        ngram_list = list(ngrams(words_tokenized, n))
                        for ngram in ngram_list:
                            if all(word not in common_conjunctions_urdu for word in ngram):
                                if n == 3 and is_similar_2gram(ngram):
                                    continue  # Skip 2-grams similar to 3-grams
                                phrase_text = ' '.join(ngram)
                                trending_phrases.update([phrase_text])
                                if phrase_text not in ngram_objects:
                                    ngram_objects[phrase_text] = []
                                ngram_objects[phrase_text].append(obj)
            # Create a list to store common phrases and their associated objects in the desired structure
            for phrase, count in trending_phrases.items():
                objects_info = []
                for obj in ngram_objects.get(phrase, []):
                    obj_info = {
                        'id': obj.id,
                        'channel_name': obj.channel_name,
                        'channel_image': obj.channel_image,
                        'ticker_image': obj.ticker_image,
                        'date': obj.date,
                        'time': obj.time,
                        'text_ocr': obj.text_ocr,
                    }
                    objects_info.append(obj_info)
                keywords_cloud_list.append({'text': phrase, 'value': count, 'objects': objects_info})
            
        date=datetime.datetime.now().date()
        current_time = datetime.datetime.now()
        new_time = current_time - datetime.timedelta(interval)
        
        getting_six_hours_object = Ticker_Extraction_Model.objects.filter(Q(channel_name='Geo') | Q(channel_name='Ary') | Q(channel_name='Samaa') | Q(channel_name='Express') | Q(channel_name='Dunya'),date=date,time__range=(new_time.time(), current_time.time()))
        database_grams_keyword_cloud(getting_six_hours_object)
        if not getting_six_hours_object:
                data= Ticker_Extraction_Model.objects.filter(Q(channel_name='Geo') | Q(channel_name='Ary') | Q(channel_name='Samaa') | Q(channel_name='Express') | Q(channel_name='Dunya'),date=date).order_by('-id')[:50]
                database_grams_keyword_cloud(data)
        keywords_cloud_list = sorted(keywords_cloud_list, key=lambda x: x['value'], reverse=True)

        print('trending_word_list',keywords_cloud_list)
        return JsonResponse({'keywords_cloud': keywords_cloud_list[:50]})
    else:
        return JsonResponse({'error': 'Method not Allowed'}, status=500)


@csrf_exempt
def keywords_cloud_local_offline(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        filters = data.get('keywordsCloudFilters', {})
        print('filters',filters)
        selected_channel_type = filters.get('selectedChannelType', 'localChannels')
        selected_channel = filters.get('selectedChannel', '')
        print('selected_channel',selected_channel)
        # selected_channel ='Geo'

        search_text = filters.get('searchText', '')
        # search_text='اسلام آباد'
        start_date = filters.get('startDate', '')
        end_date = filters.get('endDate', '')
        start_time = filters.get('startTime', '')
        end_time = filters.get('endTime', '')
        old_data_count = filters.get('oldDataCount', None)

        # print('data',data)
       
        # Create a base queryset
        result = Ticker_Extraction_Model.objects.all().order_by('-id')

        selected_channel = channel_mapping.get(selected_channel, '')
        print('selected_channel',selected_channel)

        if selected_channel_type == 'localChannels':
            result = result.filter(channel_name__in=['Geo', 'Ary', 'Samaa', 'Express', 'Dunya','Twenty_Four','Ninety_Two','Gnn','Hum','Ptv','Dawn','Neo','Aaj'])

        if selected_channel_type == 'foreignChannels':
            result = result.filter(channel_name__in=['IndiaToday', 'Aljazeera', 'Cnn', 'Rt', 'Bbc'])

        if selected_channel:
            result = result.filter(channel_name=selected_channel)

        if search_text:
            result = result.filter(text_ocr__icontains=search_text)

        result = filter_by_date(result, start_date, end_date)
        result = filter_by_time(result, start_time, end_time)
        data_result=result
        # for i in data_result:
        #     print(i.channel_name)
        trending_phrases = Counter()
        ngram_objects = {}

        def is_similar_2gram(ngram):
            for i in range(len(ngram) - 1):
                if ' '.join(ngram[i:i+2]) in ngram_objects:
                    return True
            return False
        for obj in data_result:
            if obj.text_ocr:

                getting_split_words = obj.text_ocr
                getting_split_words = re.sub(r'[^\w\sءاآأؤإئابةتثجحخدذرزسشصضطظعغفقكلمنهوىيa-zA-Z]', '', getting_split_words)
                words_tokenized = word_tokenize(getting_split_words)
                if ':' in words_tokenized and words_tokenized.index(':') == 1:
                    phrase_text = words_tokenized[0]
                    trending_phrases.update([phrase_text])

                # Extract words before colons and after commas in Urdu text
                urdu_pattern = r'(\w+),|(\w+):'
                matches = re.findall(urdu_pattern, getting_split_words, re.UNICODE)

                for n in range(2, 4):
                    ngram_list = list(ngrams(words_tokenized, n))
                    for ngram in ngram_list:
                        if all(word not in common_conjunctions_urdu for word in ngram):
                            if n == 3 and is_similar_2gram(ngram):
                                continue  # Skip 2-grams similar to 3-grams
                            phrase_text = ' '.join(ngram)
                            trending_phrases.update([phrase_text])
                            if phrase_text not in ngram_objects:
                                ngram_objects[phrase_text] = []
                            ngram_objects[phrase_text].append(obj)
        # Create a list to store common phrases and their associated objects in the desired structure
        keywords_cloud_list = []
        for phrase, count in trending_phrases.items():
            objects_info = []
            for obj in ngram_objects.get(phrase, []):
                obj_info = {
                    'id': obj.id,
                    'channel_name': obj.channel_name,
                    'channel_image': obj.channel_image,
                    'ticker_image': obj.ticker_image,
                    'date': obj.date,
                    'time': obj.time,
                    'text_ocr': obj.text_ocr,
                }
                objects_info.append(obj_info)
            keywords_cloud_list.append({'text': phrase, 'value': count, 'objects': objects_info})
        keywords_cloud_list = sorted(keywords_cloud_list, key=lambda x: x['value'], reverse=True)
        # print('trending_word_list',keywords_cloud_list)
        return JsonResponse({'keywords_cloud_offline': keywords_cloud_list[:50]})
    else:
             return JsonResponse({'GET':'GET' })
# change trending_words_foreigb according to keyword_cloud_local

@csrf_exempt
def trending_words_foreign(request):

    current_time = datetime.datetime.now()
    new_time = current_time - datetime.timedelta(hours=1)
    date = datetime.datetime.now().date()

    getting_six_hours_object = Ticker_Extraction_Model.objects.filter(
        Q(channel_name='IndiaToday') | Q(channel_name='Aljazeera') | Q(channel_name='Rt') |
        Q(channel_name='Cnn') | Q(channel_name='Bbc'),
        date=date, time__range=(new_time.time(), current_time.time()))
    if not getting_six_hours_object:
            getting_six_hours_object = Ticker_Extraction_Model.objects.filter(
        Q(channel_name='IndiaToday') | Q(channel_name='Aljazeera') | Q(channel_name='Rt') |
        Q(channel_name='Cnn') | Q(channel_name='Bbc'),
        date=date).order_by('-id')[:50]
    # Create a dictionary to keep track of phrase frequencies
    trending_phrases = Counter()
    ngram_objects = {}  # Dictionary to store n-grams and their associated objects

    # Helper function to check if a 3-gram contains a 2-gram
    def is_similar_2gram(ngram):
        for i in range(len(ngram) - 1):
            if ' '.join(ngram[i:i+2]) in ngram_objects:
                return True
        return False

    for obj in getting_six_hours_object:
        if obj.text_ocr:

            getting_split_words = obj.text_ocr

            # Updated regular expression for English text
            getting_split_words = re.sub(r'[^a-zA-Z\s]', '', getting_split_words)
            words_tokenized = word_tokenize(getting_split_words)

            for n in range(2, 4):
                ngram_list = list(ngrams(words_tokenized, n))
                for ngram in ngram_list:

                    if all(word.lower() not in common_conjunctions_english for word in ngram):
                        if n == 3 and is_similar_2gram(ngram):
                            continue  # Skip 2-grams similar to 3-grams
                        phrase_text = ' '.join(ngram)
                        trending_phrases.update([phrase_text])
                        if phrase_text not in ngram_objects:
                            ngram_objects[phrase_text] = []
                        ngram_objects[phrase_text].append(obj)

    # Create a list to store common phrases and their associated objects in the desired structure
    trending_words_list = []
    for phrase, count in trending_phrases.items():
        objects_info = []
        for obj in ngram_objects.get(phrase, []):
            obj_info = {
                'id': obj.id,
                'channel_name': obj.channel_name,
                'channel_image': obj.channel_image,
                'ticker_image': obj.ticker_image,
                'date': obj.date,
                'time': obj.time,
                'text_ocr': obj.text_ocr,
            }
            objects_info.append(obj_info)
        trending_words_list.append({'text': phrase, 'value': count, 'objects': objects_info})
    
    trending_words_list = sorted(trending_words_list, key=lambda x: x['value'], reverse=True)

    return JsonResponse({'trending_words': trending_words_list[:50]})


