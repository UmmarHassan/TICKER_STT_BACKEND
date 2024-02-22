import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticker_new.settings')

app = Celery('ticker_new')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.broker_connection_retry_on_startup = True


# celery.py
import os
from celery import Celery, group
import django
# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticker_new.settings')
django.setup()


app = Celery('ticker_new')
from polls.views import streamer

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.broker_connection_retry_on_startup = True
app.conf.worker_concurrency = 20  # Set it to a value higher than the number of tasks

import asyncio
@app.task
async def parallel_video_downloads():
    urls = [
        {
            "source": "udp://@238.190.1.73:5500",
            "y1": 305,
            "y2": 344,
            "x1": 1,
            "x2": 520,
            "folder_save": 'Geo_Ticker',

            "channel_name": 'Geo',
            "channel_logo": 'geo.png',
            "saving_basename": 'Geonews',
            
        },
        {
            "source": "udp://@238.190.1.54:5500",
            "y1": 302,
            "y2": 359,
            "x1": 0,
            "x2": 531,
            "folder_save": 'Ary_Ticker',


            "channel_name": 'Ary',
            "channel_logo": 'ary.png',
            "saving_basename": 'Arynews',
            
        },
        {
            "source": "udp://@238.190.1.81:5500",
            "y1": 305,
            "y2": 345,
            "x1": 1,
            "x2": 515,
            "folder_save": 'Samaa_Ticker',

            "channel_name": 'Samaa',
            "channel_logo": 'samaa.png',
            "saving_basename": 'Samaanews',
            # "frames_to_be_skipped": 120
        },
        {
            "source": "udp://@238.190.1.3:5500",
            "y1": 310,
            "y2": 358,
            "x1": 0,
            "x2": 495,
            "folder_save": 'Express_Ticker',


            "channel_name": 'Express',
            "channel_logo": 'express.png',
            "saving_basename": 'Expressnews',
            
        },
        {
            "source":"udp://@238.190.1.92:5500",
            "y1":295,
             "y2":360,
             "x1":0,
             "x2":544,
             "folder_save":'Gnn_Ticker',


             "channel_name":'Gnn',
             "channel_logo":'gnn.png',
             "saving_basename":'Gnnnews',
            #  "frames_to_be_skipped":60
        },
        {
            "source": "udp://@238.190.1.4:5500",
            "y1": 297,
            "y2": 335,
            "x1": 89,
            "x2": 550,
            "folder_save": 'Dunya_Ticker',


            "channel_name": 'Dunya',
            "channel_logo": 'dunya.png',
            "saving_basename": 'Dunyanews',
            # "frames_to_be_skipped": 35
        },


        {
        "source":"udp://@238.190.1.179:5500",
        "y1":287,
        "y2":360,
        "x1":0,
        "x2":521,
        "folder_save":'Twenty_Four_Ticker',


        "channel_name":'Twenty_Four',
        "channel_logo":'twentyfour.png',
        "saving_basename":'TwentyFournews',
        # "frames_to_be_skipped":60
        },

        {
            "source":"udp://@238.190.1.28:5500",
            "y1":318,
            "y2":354,
            "x1":0,
            "x2":555,
            "folder_save":'Ptv_Ticker',


            "channel_name":'Ptv',
            "channel_logo":'ptv.png',
            "saving_basename":'Ptvnews',
            # "frames_to_be_skipped":60
        },

        {

"source":"udp://@238.190.1.84:5500",
"y1":294,
"y2":330,
"x1":0,
"x2":528,
"folder_save":'Dawn_Ticker',


"channel_name":'Dawn',
"channel_logo":'dawn.png',
"saving_basename":'Dawnnews',
# "frames_to_be_skipped":60
        },


        {
            "source": "udp://@238.190.1.48:5500",
            "y1": 297,
            "y2": 335,
            "x1": 40,
            "x2": 550,
            "folder_save": 'Ninety_Two_Ticker',


            "channel_name": 'Ninety_Two',
            "channel_logo": 'ninetytwo.png',
            "saving_basename": 'NinetyTwonews',
            
        }
        # Add more dictionaries for additional URLs if needed
        ]


    # Create a list of signature objects for the video_chunk_downloader tasks
# Create a list of signature objects for the video_chunk_downloader tasks
    tasks = [streamer.si(
        url["source"],
        url["y1"],
        url["y2"],
        url["x1"],
        url["x2"],
        url["folder_save"],
        url["channel_name"],
        url["channel_logo"],
        url["saving_basename"],
    ).delay() for url in urls]

    # Use asyncio.gather to run the tasks asynchronously
    results = await asyncio.gather(*tasks)

    return results

# Define the beat schedule to run parallel_video_downloads every 1 minute
app.conf.beat_schedule = {
    'task_name_1': {
        'task': 'ticker_new.celery.parallel_video_downloads',  # Use the correct task name
        'schedule': 1.0,  # Every 1 minute
    },
}

# ************************************************************************************************************************************************************************************************************************
# app.conf.beat_schedule = {
#     'task_name_1': {
#         'task': 'whisper_app.tasks.video_chunk_downloader',
#         'schedule': 60.0,  # Every 1 minute
#         'args': ("https://www.youtube.com/@ExpressNewspkofficial/live", "express_news"),
#     },
#     'task_name_2': {
#         'task': 'whisper_app.tasks.video_chunk_downloader',
#         'schedule': 60.0,  # Every 1 minute
#         'args': ("https://www.youtube.com/@geonews/live", "geo_news"),
#     },
#     'task_name_3': {
#         'task': 'whisper_app.tasks.video_chunk_downloader',
#         'schedule': 60.0,  # Every 1 minute
#         'args': ("https://www.youtube.com/ArynewsTvofficial/live", "ary_news"),
#     },
#     'task_name_4': {
#         'task': 'whisper_app.tasks.video_chunk_downloader',
#         'schedule': 60.0,  # Every 1 minute
#         'args': ("https://www.youtube.com/@DunyanewsOfficial/live", "dunya_news"),
#     },
#     'task_name_5': {
#         'task': 'whisper_app.tasks.video_chunk_downloader',
#         'schedule': 60.0,  # Every 1 minute
#         'args': ("https://www.youtube.com/@92newshdTv/live", "ninety_two"),
#     },
#     # Add more tasks for other URLs and channel names with the same 1-minute schedule
# }
