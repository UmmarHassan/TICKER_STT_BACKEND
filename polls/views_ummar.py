from django.shortcuts import render
from django.http import JsonResponse
import glob
import os
import json
from google_ocr.ocr import Drive_OCR
all_data_comparer=0
from django.views.decorators.csrf import csrf_exempt
import uuid
import cv2
import pafy
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import word_to_be_searched_form
from .models import Ticker_Extraction_Model,words_to_be_searched_model
import time
import subprocess
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
import cv2

def streamer(source,y1,y2,x1,x2,folder_save):
    if not os.path.exists(f'C:/Users/khan/Desktop/forbmax apps/Fuse-React-v8.3.8-skeleton/public/assets/images/apps/tickers/{folder_save}'):
        os.mkdir(f'C:/Users/khan/Desktop/forbmax apps/Fuse-React-v8.3.8-skeleton/public/assets/images/apps/tickers/{folder_save}')
    video = pafy.new(source)
    best = video.getbest(preftype="mp4")
    cap = cv2.VideoCapture(best.url)
    success, frame = cap.read()
    width = 640
    height = 360
    dim = (width, height)
    if success:
        image = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
        ticker=image[y1:y2,x1:x2]
        characters = generate_unique_filename()

        cv2.imwrite(f"C:/Users/khan/Desktop/forbmax apps/Fuse-React-v8.3.8-skeleton/public/assets/images/apps/tickers/{folder_save}/{characters}.jpg", ticker)
    cap.release()      
    return characters

@csrf_exempt
def index2(request):
        if request.method=="POST":
           
            global all_data_comparer
            all_data_comparer=0
            
             # Parse the JSON data from the request body
            data = json.loads(request.body.decode('utf-8'))
            filters = data.get('filters', {})
            selected_channel = filters.get('selectedChannel', '')  # Default to '' if not provided
            search_text = filters.get('searchText', '')
            start_date = filters.get('startDate', '')
            end_date = filters.get('endDate', '')
            start_time = filters.get('startTime', '')
            end_time = filters.get('endTime', '')

            if selected_channel=='geo_ticker':
                selected_channel='Geo'
            if selected_channel=='ary_ticker':
                selected_channel='Ary'
            if selected_channel=='samaa_ticker':
                selected_channel='Samaa'
            if selected_channel=='express_ticker':
                selected_channel='Express'
            if selected_channel=='dunya_ticker':
                selected_channel='Dunya'
            if selected_channel=='ktn_ticker':
                selected_channel='Ktn'

            if start_time:
                start_time=convert_time_format(start_time)
        
            if end_time:
                end_time=convert_time_format(end_time)
            
            if  selected_channel=='' and start_date and not search_text and  end_date and not start_time and not end_time:
                result= Ticker_Extraction_Model.objects.filter(date__range=[start_date,end_date]).order_by('-id')
            if  selected_channel=='' and not start_date and not search_text and  not end_date and  start_time and  end_time:
                result= Ticker_Extraction_Model.objects.filter(time__range=(start_time,end_time)).order_by('-id')

            if  selected_channel=='' and start_date and not search_text and not end_date and not start_time and not end_time:
                result= Ticker_Extraction_Model.objects.filter(date=start_date).order_by('-id')
            if  selected_channel=='' and not start_date and not search_text and end_date and not start_time and not end_time:
                result= Ticker_Extraction_Model.objects.filter(date=end_date).order_by('-id')
            if  selected_channel=='' and not start_date and not search_text and not end_date and  start_time and not end_time:
                result= Ticker_Extraction_Model.objects.filter(time=start_time).order_by('-id')
            if  selected_channel=='' and not start_date and not search_text and not end_date and not start_time and  end_time:
                result= Ticker_Extraction_Model.objects.filter(time=end_time).order_by('-id')
            if not search_text and selected_channel == '' and start_date and end_date and  start_time and end_time:
                result= Ticker_Extraction_Model.objects.filter(date__range=[start_date, end_date],time__range=(start_time,end_time)).order_by('-id')

            if not search_text and selected_channel != '' and start_date and end_date and  start_time and end_time:
                result= Ticker_Extraction_Model.objects.filter(channel_name=selected_channel,date__range=[start_date, end_date],time__range=(start_time,end_time)).order_by('-id')
            if not search_text and selected_channel != ''  and start_date and end_date and not start_time and not end_time:
                result= Ticker_Extraction_Model.objects.filter(channel_name=selected_channel,date__range=[start_date, end_date]).order_by('-id')
            if not search_text and selected_channel != '' and not start_date and not end_date and start_time and  end_time:
                result = Ticker_Extraction_Model.objects.filter(channel_name=selected_channel,time__range=(start_time, end_time)).order_by('-id')
            if search_text and selected_channel != '' and  start_date and  end_date and not start_time and not end_time:
                result = Ticker_Extraction_Model.objects.filter(channel_name=selected_channel,date__range=[start_date, end_date],text_ocr__icontains=search_text).order_by('-id')
            if search_text and selected_channel == '' and  start_date and  end_date and not start_time and not end_time:
                result = Ticker_Extraction_Model.objects.filter(date__range=[start_date, end_date],text_ocr__icontains=search_text).order_by('-id')
            if search_text and selected_channel != '' and  start_date and  end_date and  start_time and  end_time:
                result = Ticker_Extraction_Model.objects.filter(channel_name=selected_channel,date__range=[start_date, end_date],time__range=(start_time,end_time),text_ocr__icontains=search_text,).order_by('-id')


            if search_text and selected_channel == '' and  start_date and  end_date and  start_time and  end_time:
                result = Ticker_Extraction_Model.objects.filter(date__range=[start_date, end_date],time__range=(start_time,end_time),text_ocr__icontains=search_text,).order_by('-id')
            if not search_text and selected_channel != '' and start_date and not start_time and not end_date and not end_time:
                result=Ticker_Extraction_Model.objects.filter(channel_name=selected_channel,date=start_date).order_by('-id')
                print('result',result)
            if not search_text and selected_channel != '' and start_time and not start_date and not end_date and not end_time:
                result=Ticker_Extraction_Model.objects.filter(channel_name=selected_channel ,time=start_time).order_by('-id')
            
            if not search_text and selected_channel != '' and start_time and start_date and not end_date and not end_time:
                result=Ticker_Extraction_Model.objects.filter(channel_name=selected_channel ,time=start_time,date=start_date).order_by('-id')
            if not search_text  and  selected_channel == '' and not start_date and  not start_time and not end_date and not end_time:
                # return render(request,'index.html')
                result=Ticker_Extraction_Model.objects.all().order_by('-id')
            if not search_text and selected_channel != '' and not search_text and not start_date and not end_date and not start_time and not end_time:
                result= Ticker_Extraction_Model.objects.filter(channel_name=selected_channel).order_by('-id')
            if search_text and selected_channel != '' and  not start_date and  not end_date and  not start_time and not end_time:
                result= Ticker_Extraction_Model.objects.filter(text_ocr__icontains=search_text,channel_name=selected_channel).order_by('-id')


            if search_text and selected_channel != '' and start_date and end_date and  start_time and end_time:
                result= Ticker_Extraction_Model.objects.filter(text_ocr__icontains=search_text,channel_name=selected_channel,date__range=[start_date, end_date],time__range=(start_time,end_time)).order_by('-id')
            if search_text and selected_channel != ''  and start_date and end_date and not start_time and not end_time:
                result= Ticker_Extraction_Model.objects.filter(text_ocr__icontains=search_text,channel_name=selected_channel,date__range=[start_date, end_date]).order_by('-id')
            if search_text and selected_channel != '' and not start_date and not end_date and start_time and  end_time:
                result = Ticker_Extraction_Model.objects.filter(text_ocr__icontains=search_text,channel_name=selected_channel,time__range=(start_time, end_time)).order_by('-id')


            if search_text and selected_channel != '' and start_date and not start_time and not end_date and not end_time:
                result=Ticker_Extraction_Model.objects.filter(text_ocr__icontains=search_text,channel_name=selected_channel,date=start_date).order_by('-id')
                print('result',result)
            if search_text and selected_channel != '' and start_time and not start_date and not end_date and not end_time:
                result=Ticker_Extraction_Model.objects.filter(text_ocr__icontains=search_text,channel_name=selected_channel ,time=start_time).order_by('-id')
            
            if search_text and selected_channel != '' and start_time and start_date and not end_date and not end_time:
                result=Ticker_Extraction_Model.objects.filter(text_ocr__icontains=search_text,channel_name=selected_channel ,time=start_time,date=start_date).order_by('-id')

            if  selected_channel == '' and search_text  and not start_date and  not start_time and not end_date and not end_time:
            # else :
                result=Ticker_Extraction_Model.objects.filter(text_ocr__icontains=search_text).order_by('-id')

            if  selected_channel == '' and not search_text and  not start_date and  not start_time and not end_date and not end_time:
                # return render(request,'index.html')
                result=Ticker_Extraction_Model.objects.all().order_by('-id')

                  # Pagination
            if result:
                global data_result
                data_result=list(result.values())

                return JsonResponse({'tickers': data_result[:100], 'channel_name': selected_channel})
            else:
                return JsonResponse({'failed':'failed'})

        else:
               return JsonResponse({'tickers': 'data'})

# @login_required(login_url=reverse_lazy('login'))
@csrf_exempt
def index(request):
    if request.method=='POST':
            receiving_word=json.loads(request.body)
            word_notification=receiving_word.get('word','')
            if word_notification:
                checking=words_to_be_searched_model.objects.filter(word=word_notification).exists()
                if checking:
                    return JsonResponse({'words': 'exists'})

                else:
                   word= words_to_be_searched_model.objects.create(word=word_notification)
                   object_for_word=words_to_be_searched_model.objects.get(id=word.id)

                   return JsonResponse({'word':object_for_word.word })
            else:
                return JsonResponse({'word':'word not received' })
    else:
        return JsonResponse({'word': 'Method not supported' })


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

# @login_required(login_url=reverse_lazy('login'))
@csrf_exempt
def dunya_ticker(request):
    timedata_dunya=[]
    all_files_with_names_dunya={}
    all_files_with_names_dunya_list=[]

    date=datetime.datetime.now().date()
    timeticker=datetime.datetime.now().time()
    formatted_time = timeticker.strftime("%I:%M %p")
   
    start_time = time.time()  # Get the current time

    characters=streamer(source="https://www.youtube.com/watch?v=Jr5abATDcXc",y1=297,y2=335,x1=89,x2=550,folder_save='dunya_tickers')            

    text_ticker = Drive_OCR(f"C:/Users/khan/Desktop/forbmax apps/Fuse-React-v8.3.8-skeleton/public/assets/images/apps/tickers/dunya_tickers/{characters}.jpg")

    text_ticker=text_ticker.main()
    # print('text_ticker',text_ticker)
    all_objects = Ticker_Extraction_Model.objects.filter(channel_name='Dunya').order_by('-id')[:20]
   
    if len(text_ticker)>=3:
        # if Ticker_Extraction_Model.objects.filter(text_ocr__iexact=text_ticker).exists():
        ticker_write=True
        # Compare text similarity with each object
        for obj in all_objects:
            similarity_ratio = fuzz.ratio(text_ticker, obj.text_ocr)
            
            if similarity_ratio >= 80:
                
                os.remove(f"C:/Users/khan/Desktop/forbmax apps/Fuse-React-v8.3.8-skeleton/public/assets/images/apps/tickers/dunya_tickers/{characters}.jpg")
                print('I am similarity')
                ticker_write=False
                break
              
        if ticker_write:
            print('I am writing in database')
            Ticker_Extraction_Model.objects.create(channel_name="Dunya",channel_image="dunya.png",ticker_image=f"{characters}.jpg",date=date,time=formatted_time,text_ocr=text_ticker)

    all_objects_ten = all_objects[:10]
    for v, i in enumerate(all_objects_ten):
        # file_name=os.path.basename(i)
        all_files_with_names_dunya[f'data_{v}'] = {
            'id': i.id, 'channel_image': i.channel_image, 'ticker_image': i.ticker_image, 'date': i.date, 'time': i.time,'text_ocr': i.text_ocr}
    for key,val in all_files_with_names_dunya.items():
        all_files_with_names_dunya_list.append(val)
    
    # time_data.append(i.time)
    # print('all_ocr_result',all_ocr_result)

    end_time = time.time()  # Get the current time after the task is completed
    execution_time = end_time - start_time  # Calculate the execution time

    print(f"Function executed in {execution_time:.2f} seconds")
    return JsonResponse({'tickers':all_files_with_names_dunya_list})

# @login_required(login_url=reverse_lazy('login'))
@csrf_exempt
def geo_ticker(request):


    start_time = time.time()  # Get the current time

    date=datetime.datetime.now().date()
    timeticker=datetime.datetime.now().time()
    formatted_time = timeticker.strftime("%I:%M %p")
 
    timedata_geo=[]
    all_files_with_names_geo={}
    all_files_with_names_geo_list=[]
            
    characters=streamer(source="https://www.youtube.com/watch?v=O3DPVlynUM0",y1=305,y2=344,x1=1,x2=520,folder_save='geo_tickers')            


    text_ticker = Drive_OCR(f"C:/Users/khan/Desktop/forbmax apps/Fuse-React-v8.3.8-skeleton/public/assets/images/apps/tickers/geo_tickers/{characters}.jpg")


    text_ticker=text_ticker.main()

    all_objects = Ticker_Extraction_Model.objects.filter(channel_name='Geo').order_by('-id')[:20]
     
    if len(text_ticker)>=3:
        # if Ticker_Extraction_Model.objects.filter(text_ocr__iexact=text_ticker).exists():
        ticker_write=True
        # Compare text similarity with each object
        for obj in all_objects:
            similarity_ratio = fuzz.ratio(text_ticker, obj.text_ocr)
            
            if similarity_ratio >= 80:
                os.remove(f"C:/Users/khan/Desktop/forbmax apps/Fuse-React-v8.3.8-skeleton/public/assets/images/apps/tickers/geo_tickers/{characters}.jpg")
                # print('I am similarity')
                ticker_write=False
                break
                # matching_objects.append(obj)
                # ticker_write=True
        if ticker_write:
            # print('I am writing in database')
            Ticker_Extraction_Model.objects.create(channel_name="Geo",channel_image="geo.png",ticker_image=f"{characters}.jpg",date=date,time=formatted_time,text_ocr=text_ticker)         

    all_objects_ten = all_objects[:10]
    for v, i in enumerate(all_objects_ten):
        # file_name=os.path.basename(i)
        all_files_with_names_geo[f'data_{v}'] = {
            'id': i.id, 'channel_image': i.channel_image, 'ticker_image': i.ticker_image, 'date': i.date, 'time': i.time,'text_ocr': i.text_ocr}
    for key,val in all_files_with_names_geo.items():
        all_files_with_names_geo_list.append(val)
    
    # time_data.append(i.time)
    # print('all_ocr_result',all_ocr_result)

    end_time = time.time()  # Get the current time after the task is completed
    execution_time = end_time - start_time  # Calculate the execution time

    print(f"Function executed in {execution_time:.2f} seconds")
    return JsonResponse({'tickers':all_files_with_names_geo_list})
   
result_all=[]

# @login_required(login_url=reverse_lazy('login'))
@csrf_exempt

def convert_time_format(time_str):
    # Parse the time string into a datetime object
    time_obj = datetime.datetime.strptime(time_str, "%H:%M")
    
    # Convert the time to 12-hour format with AM/PM indicator
    formatted_time = time_obj.strftime("%I:%M %p")
    
    return formatted_time

# @login_required(login_url=reverse_lazy('login'))
@csrf_exempt
def table_view(request):
    global all_data_comparer, data_result
    
    data = data_result[all_data_comparer:all_data_comparer+10]
    length_of_data = len(data_result)
    
    if all_data_comparer < length_of_data:
        paginator = Paginator(data_result, 10)  # Use the full data for counting the total pages
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        all_data_comparer += 10
        
        return render(request, 'index.html', {'result': page_obj, 'clear': 'True'})

    all_data_comparer = 0  # Reset the comparer when all data is loaded
    return JsonResponse({'message': 'All data has been loaded'}, status=200)


# @login_required(login_url=reverse_lazy('login'))
@csrf_exempt

def ary_ticker(request):
    
    timedata_ary=[]
    all_files_with_names_ary={}
    all_files_with_names_ary_list=[]


    start_time = time.time()  # Get the current time

    date=datetime.datetime.now().date()
    timeticker=datetime.datetime.now().time()
    formatted_time = timeticker.strftime("%I:%M %p")
   
    # timedata_ary.clear()
    # all_files_with_names_ary.clear()
 

    characters=streamer(source="https://www.youtube.com/watch?v=sUKwTVAc0Vo",y1=302,y2=359,x1= 0,x2=531,folder_save='ary_tickers')            
    text_ticker = Drive_OCR(f"C:/Users/khan/Desktop/forbmax apps/Fuse-React-v8.3.8-skeleton/public/assets/images/apps/tickers/ary_tickers/{characters}.jpg")

    text_ticker=text_ticker.main()
    print('text_ticker',text_ticker)
    all_objects = Ticker_Extraction_Model.objects.filter(channel_name="Ary").order_by('-id')[:20]
     
    if len(text_ticker)>=3:
        # if Ticker_Extraction_Model.objects.filter(text_ocr__iexact=text_ticker).exists():
        ticker_write=True
        # Compare text similarity with each object
        for obj in all_objects:
            similarity_ratio = fuzz.ratio(text_ticker, obj.text_ocr)
            
            if similarity_ratio >= 80:
                os.remove(f"C:/Users/khan/Desktop/forbmax apps/Fuse-React-v8.3.8-skeleton/public/assets/images/apps/tickers/ary_tickers/{characters}.jpg")
                print('I am similarity')
                ticker_write=False
                break
                # matching_objects.append(obj)
                # ticker_write=True
        if ticker_write:
            print('I am writing in database')
            Ticker_Extraction_Model.objects.create(channel_name="Ary",channel_image="ary.png",ticker_image=f"{characters}.jpg",date=date,time=formatted_time,text_ocr=text_ticker)

    #_files=Ticker_Extraction_Model.objects.filter(channel_name='Ary').order_by('-id')[:10]

    all_objects_ten = all_objects[:10]
    for v, i in enumerate(all_objects_ten):
        # file_name=os.path.basename(i)
        all_files_with_names_ary[f'data_{v}'] = {
            'id': i.id, 'channel_image': i.channel_image, 'ticker_image': i.ticker_image, 'date': i.date, 'time': i.time,'text_ocr': i.text_ocr}
    for key,val in all_files_with_names_ary.items():
        all_files_with_names_ary_list.append(val)
    
    # time_data.append(i.time)
    # print('all_ocr_result',all_ocr_result)

    end_time = time.time()  # Get the current time after the task is completed
    execution_time = end_time - start_time  # Calculate the execution time

    print(f"Function executed in {execution_time:.2f} seconds")
    return JsonResponse({'tickers':all_files_with_names_ary_list})


# @login_required(login_url=reverse_lazy('login'))
@csrf_exempt

def samaa_ticker(request):
    timedata_samaa=[]
    all_files_with_names_samaa={}
    all_files_with_names_samaa_list=[]
    start_time = time.time()  # Get the current time

    date=datetime.datetime.now().date()
    timeticker=datetime.datetime.now().time()
    formatted_time = timeticker.strftime("%I:%M %p")   
              
    characters=streamer(source="https://www.youtube.com/watch?v=yHi3yIkPcLE",y1=304,y2=345,x1= 1,x2=515,folder_save='samaa_tickers')            

    text_ticker = Drive_OCR(f"C:/Users/khan/Desktop/forbmax apps/Fuse-React-v8.3.8-skeleton/public/assets/images/apps/tickers/samaa_tickers/{characters}.jpg")

    text_ticker=text_ticker.main()
  
    all_objects = Ticker_Extraction_Model.objects.filter(channel_name="Samaa").order_by('-id')[:20]
   
    if len(text_ticker)>=3:
        ticker_write=True
        for obj in all_objects:
            similarity_ratio = fuzz.ratio(text_ticker, obj.text_ocr)
            
            if similarity_ratio >= 80:
                os.remove(f"C:/Users/khan/Desktop/forbmax apps/Fuse-React-v8.3.8-skeleton/public/assets/images/apps/tickers/samaa_tickers/{characters}.jpg")
                print('I am similarity')
                ticker_write=False
                break
        
        if ticker_write:
            print('I am writing in database')
            Ticker_Extraction_Model.objects.create(channel_name="Samaa",channel_image="samaa.png",ticker_image=f"{characters}.jpg",date=date,time=formatted_time,text_ocr=text_ticker)

    all_objects_ten = all_objects[:10]
    for v, i in enumerate(all_objects_ten):
        # file_name=os.path.basename(i)
        all_files_with_names_samaa[f'data_{v}'] = {
            'id': i.id, 'channel_image': i.channel_image, 'ticker_image': i.ticker_image, 'date': i.date, 'time': i.time,'text_ocr': i.text_ocr}
    for key,val in all_files_with_names_samaa.items():
        all_files_with_names_samaa_list.append(val)
    
    # time_data.append(i.time)
    # print('all_ocr_result',all_ocr_result)

    end_time = time.time()  # Get the current time after the task is completed
    execution_time = end_time - start_time  # Calculate the execution time

    print(f"Function executed in {execution_time:.2f} seconds")
    return JsonResponse({'tickers':all_files_with_names_samaa_list})

# count_express=0
# @login_required(login_url=reverse_lazy('login'))
@csrf_exempt

def express_ticker(request):
    # global count_express
    current_count_express = request.session.get('counter', 0)

    new_count = current_count_express + 1
    timedata_express=[]
    all_files_with_names_express={}
    all_files_with_names_express_list=[]
    start_time = time.time()  # Get the current time

    date=datetime.datetime.now().date()
    timeticker=datetime.datetime.now().time()
    formatted_time = timeticker.strftime("%I:%M %p")

    characters=streamer(source="https://www.youtube.com/watch?v=muBr6a3Xi2c",y1=310,y2=358,x1=0,x2=495,folder_save='express_tickers')            
    
    print(' I am inside try')
    text_ticker = Drive_OCR(f"C:/Users/khan/Desktop/forbmax apps/Fuse-React-v8.3.8-skeleton/public/assets/images/apps/tickers/express_tickers/{characters}.jpg")
 
    try:
       text_ticker=text_ticker.main()
       if  text_ticker:
        count_express=0 
        request.session['counter'] = count_express

    except:
        if current_count_express==1:
            os.remove('google_ocr/token.pickle')
        new_count = current_count_express + 1
        request.session['counter'] = new_count

    all_objects = Ticker_Extraction_Model.objects.filter(channel_name='Express').order_by('-id')[:20]

    if text_ticker:
        if len(text_ticker)>=3:
            ticker_write=True
            for obj in all_objects:
                similarity_ratio = fuzz.ratio(text_ticker, obj.text_ocr)
                
                if similarity_ratio >= 80:
                    os.remove(f"C:/Users/khan/Desktop/forbmax apps/Fuse-React-v8.3.8-skeleton/public/assets/images/apps/tickers/express_tickers/{characters}.jpg")
                    # print('I am similarity')
                    ticker_write=False
                    break
                   
            if ticker_write:
                Ticker_Extraction_Model.objects.create(channel_name="Express",channel_image="express.png",ticker_image=f"{characters}.jpg",date=date,time=formatted_time,text_ocr=text_ticker)

    all_objects_ten = all_objects[:10]
    for v, i in enumerate(all_objects_ten):
        # file_name=os.path.basename(i)
        all_files_with_names_express[f'data_{v}'] = {
            'id': i.id, 'channel_image': i.channel_image, 'ticker_image': i.ticker_image, 'date': i.date, 'time': i.time,'text_ocr': i.text_ocr}
    for key,val in all_files_with_names_express.items():
        all_files_with_names_express_list.append(val)
    
    # time_data.append(i.time)
    # print('all_ocr_result',all_ocr_result)

    end_time = time.time()  # Get the current time after the task is completed
    execution_time = end_time - start_time  # Calculate the execution time

    print(f"Function executed in {execution_time:.2f} seconds")
    return JsonResponse({'tickers':all_files_with_names_express_list})

# inside geo the dunya is running and inside dunya the geo is running

# @login_required(login_url=reverse_lazy('login'))
@csrf_exempt

def ktn_ticker(request):    
    timedata_ktn_news=[]
    all_files_with_names_ktn_news={}
    all_files_with_names_ktn_news_list=[]

    date=datetime.datetime.now().date()
    timeticker=datetime.datetime.now().time()
    formatted_time = timeticker.strftime("%I:%M %p")
   
    start_time = time.time()  # Get the current time
 
    characters=streamer(source="https://www.youtube.com/watch?v=gQAl_fWayjA",y1=323,y2=355,x1=22,x2=510,folder_save='ktn_tickers')            

    text_ticker = Drive_OCR(f"C:/Users/khan/Desktop/forbmax apps/Fuse-React-v8.3.8-skeleton/public/assets/images/apps/tickers/ktn_tickers/{characters}.jpg")

    text_ticker=text_ticker.main()
    # print('text_ticker',text_ticker)
    all_objects = Ticker_Extraction_Model.objects.filter(channel_name='Ktn').order_by('-id')[:20]
    if len(text_ticker)>=3:
        # if Ticker_Extraction_Model.objects.filter(text_ocr__iexact=text_ticker).exists():
        
        ticker_write=True
        # Compare text similarity with each object
        for obj in all_objects:
            similarity_ratio = fuzz.ratio(text_ticker, obj.text_ocr)
            
            if similarity_ratio >= 80:
                os.remove(f"C:/Users/khan/Desktop/forbmax apps/Fuse-React-v8.3.8-skeleton/public/assets/images/apps/tickers/ktn_tickers/{characters}.jpg")
                print('I am similarity')
                ticker_write=False
                break
                # matching_objects.append(obj)
                # ticker_write=True
        if ticker_write:
            print('I am writing in database')
            Ticker_Extraction_Model.objects.create(channel_name="Ktn",channel_image="ktn.png",ticker_image=f"{characters}.jpg",date=date,time=formatted_time,text_ocr=text_ticker)

    all_objects_ten = all_objects[:10]
    for v, i in enumerate(all_objects_ten):
        # file_name=os.path.basename(i)
        all_files_with_names_ktn_news[f'data_{v}'] = {
            'id': i.id, 'channel_image': i.channel_image, 'ticker_image': i.ticker_image, 'date': i.date, 'time': i.time,'text_ocr': i.text_ocr}
    for key,val in all_files_with_names_ktn_news.items():
        all_files_with_names_ktn_news_list.append(val)
    
    # time_data.append(i.time)
    # print('all_ocr_result',all_ocr_result)

    end_time = time.time()  # Get the current time after the task is completed
    execution_time = end_time - start_time  # Calculate the execution time

    print(f"Function executed in {execution_time:.2f} seconds")
    return JsonResponse({'tickers':all_files_with_names_ktn_news_list})


# import numpy as np
# import cv2
# import io
# import numpy as np
# from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageFilter
# date_images=[]
# time_images=[]

# def make_image(date_live, saver_name, list_saver):
#     image_size = (200, 100)  # Desired image size
#     background_color = (255, 255, 255)  # RGB color for the background
#     text_color = (0, 0, 0)  # RGB color for the text
#     font_size = 35
#     font_path = r"D:\ticker_new\Times New Roman\times new roman bold.ttf"  # Replace with the path to your desired font file

#     if list_saver == 'date':
#         date_images.clear()
#     elif list_saver == 'time':
#         time_images.clear()

#     for i in range(len(date_live)):
#         # Create a new image with the specified background color
#         image = Image.new('RGB', image_size, background_color)

#         # Create a draw object
#         draw = ImageDraw.Draw(image)

#         # Define the font and load it with the specified size
#         font = ImageFont.truetype(font_path, font_size)

#         # Calculate the position to center the text
#         text_width, text_height = draw.textsize(date_live[i], font=font)
#         position = ((image_size[0] - text_width) // 2, (image_size[1] - text_height) // 2)

#         # Draw the text on the image
#         draw.text(position, date_live[i], font=font, fill=text_color)

#         # Apply contrast enhancement to the image
#         enhancer = ImageEnhance.Contrast(image)
#         enhanced_image = enhancer.enhance(1.5)  # Adjust the contrast factor as desired

#         # Apply brightness enhancement to the image
#         enhancer = ImageEnhance.Brightness(enhanced_image)
#         brightened_image = enhancer.enhance(1.2)  # Adjust the brightness factor as desired

#         # Apply sharpening filter to the image
#         sharpened_image = brightened_image.filter(ImageFilter.SHARPEN)

#         border_color = (0, 0, 255)  # RGB color for the border
#         border_size = 5
#         border_box = [(0, 0), (image_size[0] - 1, image_size[1] - 1)]
#         draw = ImageDraw.Draw(sharpened_image)
#         # draw.rectangle(border_box, outline=border_color, width=border_size)

#         if list_saver == 'date':
#             date_images.append(np.array(sharpened_image))
#         elif list_saver == 'time':
#             time_images.append(np.array(sharpened_image))

# @csrf_exempt
# def getting_live_collage(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         getting_name = data.get('channelNameValue')
#         print('i am channel', getting_name)
#         getting_live_collage_list = data.get('liveCollageList')
#         all_images_files = []
#         all_images_files.clear()

#         time_live=data.get('timeLive')
#         date_live=data.get('dateLive')
#         print('time_live',time_live)
#         print('date_live',date_live)
#         # Size of the font
#         date_list_maker=make_image(date_live=date_live,saver_name='date',list_saver='date')
#         time_list_maker=make_image(date_live=time_live,saver_name='time',list_saver='time')
#         print('date_images',date_images)
#         print('time_images',time_images)
   
#         for i in getting_live_collage_list:
#             if getting_name == 'option1':
#                 logo = cv2.imread('image_detections/geo.png')
#                 # logo = cv2.resize(logo, (100, image_height))
#                 all_images_files.append('geo_tickers/' + os.path.basename(i))
#             elif getting_name == 'option2':
#                 logo = cv2.imread('image_detections/ary.png')
#                 # logo = cv2.resize(logo, (100, image_height))
#                 all_images_files.append('ary_tickers/' + os.path.basename(i))
#             elif getting_name == 'option3':
#                 logo = cv2.imread('image_detections/samaa.png')
#                 # logo = cv2.resize(logo, (100, image_height))
#                 all_images_files.append('samaa_tickers/' + os.path.basename(i))
#             elif getting_name == 'option4':
#                 logo = cv2.imread('image_detections/express.png')
#                 # logo = cv2.resize(logo, (100, image_height))
#                 all_images_files.append('express_tickers/' + os.path.basename(i))
#             elif getting_name == 'option5':
#                 logo = cv2.imread('image_detections/dunya.png')
#                 # logo = cv2.resize(logo, (100, image_height))
#                 all_images_files.append('dunya_tickers/' + os.path.basename(i))
#             elif getting_name == 'option6':
#                 logo = cv2.imread('image_detections/ktn.png')
#                 # logo = cv2.resize(logo, (100, image_height))
#                 all_images_files.append('ktn_tickers/' + os.path.basename(i))

#         # print('getting_live_collage_list', getting_live_collage_list)

#         resized_images = []
        
#         stacked_vertical_images=[]
#         for i in range(len(date_images)):
#                 # date_image_stack=cv2.imread(date_images[i])
#                 date_image_resized = cv2.resize(date_images[i], (200,90))

#                 # time_image_stack=cv2.imread(time_images[i])
#                 time_image_resized = cv2.resize(time_images[i], (200,90))

#                 logo = cv2.resize(logo, (200,150)) 
#                 stacked_vertical = np.vstack((logo, date_image_resized,time_image_resized))
#                 # cv2.imwrite('stacked.jpg',stacked_vertical)

#                 stacked_vertical_images.append(stacked_vertical)

#         print('len_date_images',len(date_images))
#         print('len_time_images',len(time_images))
#         print('len_all_images_files',len(all_images_files))
#         # Resize and horizontally stack the logo and each image
#         for i in range(len(all_images_files)):
#             image = cv2.imread(all_images_files[i])
#             resized_image = cv2.resize(image, (730, 110))
#             resized_stacked_image=cv2.resize(stacked_vertical_images[i],(80,110))
#             # stacked=np.vstack(())
#             stacked = np.hstack(( resized_image,resized_stacked_image))
#             resized_images.append(stacked)

#         # Vertically stack the stacked images
#         output_final = np.vstack(resized_images)
#         cv2.imwrite('Collage/ticker.png', output_final)
#         return JsonResponse({'success': 'success'})
#     else:
#         return JsonResponse({'error': 'error'})


# @csrf_exempt
# def getting_offline_collage(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         getting_name = data.get('channelNameValue')
#         print('i am channel', getting_name)
#         getting_live_collage_list = data.get('liveCollageList')
#         all_images_files = []
#         all_images_files.clear()
        
#         time_offline=data.get('timeOffline')
#         date_offline=data.get('dateOffline')
#         print('time_offline',time_offline)
#         print('date_offline',date_offline)
#         # Size of the font
#         date_list_maker=make_image(date_live=date_offline,saver_name='date',list_saver='date')
#         time_list_maker=make_image(date_live=time_offline,saver_name='time',list_saver='time')

#         image_width = 700
#         image_height = 100
#         for i in getting_live_collage_list:
#             if getting_name == 'option1':
#                 logo = cv2.imread('image_detections/geo.png')
#                 logo = cv2.resize(logo, (100, image_height))
#                 all_images_files.append('geo_tickers/' + os.path.basename(i))
#             elif getting_name == 'option2':
#                 logo = cv2.imread('image_detections/ary.png')
#                 logo = cv2.resize(logo, (100, image_height))
#                 all_images_files.append('ary_tickers/' + os.path.basename(i))
#             elif getting_name == 'option3':
#                 logo = cv2.imread('image_detections/samaa.png')
#                 logo = cv2.resize(logo, (100, image_height))
#                 all_images_files.append('samaa_tickers/' + os.path.basename(i))
#             elif getting_name == 'option4':
#                 logo = cv2.imread('image_detections/express.png')
#                 logo = cv2.resize(logo, (100, image_height))
#                 all_images_files.append('express_tickers/' + os.path.basename(i))
#             elif getting_name == 'option5':
#                 logo = cv2.imread('image_detections/dunya.png')
#                 logo = cv2.resize(logo, (100, image_height))
#                 all_images_files.append('dunya_tickers/' + os.path.basename(i))
#             elif getting_name == 'option6':
#                 logo = cv2.imread('image_detections/Ktn.png')
#                 logo = cv2.resize(logo, (100, image_height))
#                 all_images_files.append('ktn_tickers/' + os.path.basename(i))

#         resized_images = []
      
#         stacked_vertical_images=[]
#         for i in range(len(date_images)):
#                 # date_image_stack=cv2.imread(date_images[i])
#                 date_image_resized = cv2.resize(date_images[i], (200,90))

#                 # time_image_stack=cv2.imread(time_images[i])
#                 time_image_resized = cv2.resize(time_images[i], (200,90))

#                 logo = cv2.resize(logo, (200,150)) 
#                 stacked_vertical = np.vstack((logo, date_image_resized,time_image_resized))
#                 # cv2.imwrite('stacked.jpg',stacked_vertical)

#                 stacked_vertical_images.append(stacked_vertical)

#         print('len_date_images',len(date_images))
#         print('len_time_images',len(time_images))
#         print('len_all_images_files',len(all_images_files))
#         # Resize and horizontally stack the logo and each image
#         for i in range(len(all_images_files)):
#             image = cv2.imread(all_images_files[i])
#             resized_image = cv2.resize(image, (730, 110))
#             resized_stacked_image=cv2.resize(stacked_vertical_images[i],(80,110))
#             # stacked=np.vstack(())
#             stacked = np.hstack(( resized_image,resized_stacked_image))
#             resized_images.append(stacked)

#         # Vertically stack the stacked images
#         output_final = np.vstack(resized_images)
#         cv2.imwrite('Collage/ticker.png', output_final)
#         return JsonResponse({'success': 'success'})
#     else:
#         return JsonResponse({'error': 'error'})

# from django.http import HttpResponse
# from django.conf import settings
# import os
# import datetime

# def download_image(request):
#     image_path = os.path.join(settings.BASE_DIR, 'Collage', 'ticker.png')
#     # Replace 'Collage/ticker.png' with the actual path to your image file
#     with open(image_path, 'rb') as f:
#         response = HttpResponse(f.read(), content_type='image/png')

#         timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
#         response['Content-Disposition'] = f'attachment; filename="ticker_{timestamp}.png"'
#         return response


# import pywhatkit
# import keyboard

#     # whatsapp.close()
# @csrf_exempt
# def whatsapp_sender(request):

#     if request.method=="POST":

#         number=request.POST['numbersent']
#         print('number',number)
#         print('numbertype',type(number))
       
      
#         pywhatkit.sendwhats_image(number , r'Collage\ticker.png')
#         # time.sleep(5)
#         time.sleep(3)
#         keyboard.press_and_release('ctrl+w')
#         # pywhatkit.sendwhatmsg_instantly("+923119633700", "Test msg.", 10, tab_close=True)



#         return JsonResponse({'success':'success'})
#     else:
#         return JsonResponse({'error':'error'})

# @csrf_exempt
# def login_view(request):
#     if request.user.is_authenticated:
#         return redirect('index')
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         print('user',user)
#         if user is not None:
#             login(request, user)
#             return redirect('index')
#         else:
#             error_message = 'Invalid username or password.'
#     else:
#         error_message = ''

#     return render(request, 'login.html', {'error_message': error_message})
# @csrf_exempt
# def logout_view(request):
#     logout(request)
#     return redirect('login')

# @csrf_exempt
# def register_view(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             if get_user_model().objects.filter(is_superuser=True).exists():
#                 # Additional users should not have superuser privileges
#                 user.is_superuser = False
#             user.save()
#             return redirect('login')
#     else:
#         form = UserCreationForm()
#     return render(request, 'register.html', {'form': form})

@csrf_exempt
def notifications(request):
    receiving_word = json.loads(request.body)
    get_words = receiving_word.get('wordsList', [])

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
    date = datetime.datetime.now().date()
    all_ids = []

    print(notifications_list)

    try:
        notifications_list_int_ids = [int(id) for id in notifications_list]
        max_id = max(notifications_list_int_ids)
    except:
        max_id = 0

    if len(get_words) >= 1:
        for i in get_words:
            results = Ticker_Extraction_Model.objects.filter(text_ocr__icontains=i, date=date, id__gt=max_id).order_by('id').values()
            data = list(results)
            if data:
                for entry in data:
                    all_ids.append(entry['id'])
                official_result.extend(data)
                official_word.extend([i] * len(data))
            else:
                print(f"No data found for '{i}'")

        # Update the session data with the latest values
        request.session['notifications_data'] = {
            'clear_list_and_word': clear_list_and_word,
            'notifications_list': notifications_list,
            'official_result': official_result,
            'official_word': official_word,
        }

        return JsonResponse({
            'notification_data': official_result,
            'id': all_ids,
        }, safe=False)
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
#     print('notifications_list',notifications_list)
#     print('official_result',len(official_result))

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
#             else:
#                 print(f"No data found for '{word}'")

#         length = len(official_result)

#         # Update the session data with the latest values
#         request.session['notifications_data'] = {
#             'clear_list_and_word': clear_list_and_word,
#             'notifications_list': notifications_list,
#             'official_result': official_result,
#             'official_word': official_word,
#         }

#         return JsonResponse({
#             'notification_data': official_result,

#             # 'id': all_ids,

#             # 'official_word': official_word,
#             # 'notification_increment': notification_increment,
#             # 'get_words_dict': get_words,
#             # 'success': 'success',
#             # 'data_length': length_all,
#             # 'data_length_all': length,
#         }, safe=False)
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

import nltk
nltk.download("punkt")
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
from collections import Counter
from django.http import JsonResponse
from .models import Ticker_Extraction_Model

# def trending_words(request):
#     common_urdu_conjunctions = [
#     'اور', 'یا', 'لیکن', 'مگر', 'کیوں کہ', 'چونکہ', 'کہ', 'جب تک', 'کہاں تک', 'اگر', 'جیسا کہ',
#     'لہٰذا', 'اس لئے', 'استمبالکہ', 'یعنی', 'اگرچہ', 'یوں تو', 'تاکہ', 'اگرچہ کہ', 'جو بھی', 'یاہو',
#     'جیسے', 'خواہش کے برعکس', 'خلاف', 'مخالفت کے برعکس', 'کی بجائے', 'کہتے ہیں کہ',
#     'ہاں', 'نہیں', 'مگر', 'تاہم', 'لیکن', 'لہٰذا', 'مگر', 'مگرچہ', 'اگرچہ', 'مگر کہ', 'چاہے کہ',
#     'چاہوں کہ', 'تاکہ', 'یہاں تک کہ', 'کی بجائے', 'تاہم', 'کی بجائے', 'جب تک کہ', 'کی بجائے', 'ہاں',
#     'میں تو', 'مگر تم تو', 'لیکن تم تو', 'مگر ہم تو', 'یہ بات ہے کہ', 'لیکن یہ بات ہے کہ'
#         'اور', 'یا', 'لیکن', 'مگر', 'کیوں کہ', 'میں', 'نہ', 'سے',
#         'کے', 'کا', 'کی', 'کو', 'کہ', 'میں', 'نے', 'سے', 'ہوتا', 'ہوتی', 'ہوتے',
#     'یہ', 'وہ', 'ایک', 'ایسا', 'واحد', 'ذرا', 'جب', 'کب', 'کیوں', 'کیا',
#     'تو', 'بھی', 'جیسا', 'جیسے', 'اور', 'یا', 'لیکن', 'مگر', 'لہٰذا',
#     'میں', 'نہ', 'اگر', 'ہو', 'رہا', 'رہی', 'رہے', 'رہتا', 'رہتی', 'رہتے',
#     'ہوا', 'ہوئی', 'ہوئے', 'ہوتا', 'ہوتی', 'ہوتے', 'ہوگا', 'ہوگی', 'ہوگے',
#     'تھا', 'تھی', 'تھے', 'گیا', 'گئی', 'گئے', 'جائے', 'گا', 'گی', 'گے',
#     'کر', 'کرتا', 'کرتی', 'کرتے', 'کیا', 'کرنا', 'کرتے', 'کرنے', 'کریں',
#     'کیوںکہ', 'کیونکہ', 'تاکہ', 'تاکے', 'چاہئے', 'چاہتا', 'چاہتی', 'چاہتے',
#     'ہوشک', 'نہیں', 'کیسا', 'کیسی', 'کیسے', 'و', 'نے', 'نیچے', 'سوال', 'کیونکہ'
# ]
#     current_time = datetime.datetime.now()
#     new_time = current_time - datetime.timedelta(hours=6)
#     getting_six_hours_object = Ticker_Extraction_Model.objects.filter(time__range=(new_time.time(), current_time.time()))
#     # Create a dictionary to keep track of phrase frequencies
#     trending_phrases = Counter()
#     for obj in getting_six_hours_object:
#         if obj.text_ocr:
#             getting_split_words = obj.text_ocr
#             getting_split_words = re.sub(r'[^\w\sءاآأؤإئابةتثجحخدذرزسشصضطظعغفقكلمنهوىيa-zA-Z]', '', getting_split_words)
#             words_tokenized = word_tokenize(getting_split_words)
#             for n in range(2, 4):
#                 ngram_list = list(ngrams(words_tokenized, n))
#                 for ngram in ngram_list:
#                     if all(word not in common_urdu_conjunctions for word in ngram):
#                         trending_phrases.update([ngram])
#     # Filter n-grams that appear frequently (above a certain threshold)
#     min_frequency_threshold = 2  # Adjust the threshold as needed
#     common_phrases = [phrase for phrase, count in trending_phrases.items() if count >= min_frequency_threshold]

#     # Create a list to store common phrases in the desired structure
#     trending_words_list = [{'text': ' '.join(phrase), 'value': count} for phrase, count in trending_phrases.items()]
#     trending_words_list = sorted(trending_words_list, key=lambda x: x['value'], reverse=True)


def trending_words(request):
    common_urdu_conjunctions = [
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
    date=datetime.datetime.now().date()
    current_time = datetime.datetime.now()
    new_time = current_time - datetime.timedelta(hours=6)
    getting_six_hours_object = Ticker_Extraction_Model.objects.filter(date=date,time__range=(new_time.time(), current_time.time()))
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
            getting_split_words = re.sub(r'[^\w\sءاآأؤإئابةتثجحخدذرزسشصضطظعغفقكلمنهوىيa-zA-Z]', '', getting_split_words)
            words_tokenized = word_tokenize(getting_split_words)
            for n in range(2, 4):
                ngram_list = list(ngrams(words_tokenized, n))
                for ngram in ngram_list:
                    if all(word not in common_urdu_conjunctions for word in ngram):
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
