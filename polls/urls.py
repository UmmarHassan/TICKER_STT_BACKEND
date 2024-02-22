
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
        path('index/', index, name='index'),

        path('geo_ticker/' ,geo_ticker, name='geo_ticker' ),
        path('dunya_ticker/' ,dunya_ticker, name='dunya_ticker' ),
        path('ary_ticker/' ,ary_ticker, name='ary_ticker' ),
        path('samaa_ticker/' ,samaa_ticker, name='samaa_ticker' ),
        path('express_ticker/' ,express_ticker, name='express_ticker' ),
        path('gnn_ticker/' ,gnn_ticker, name='gnn_ticker' ),
        path('hum_ticker/' ,hum_ticker, name='hum_ticker' ),
        path('aaj_ticker/' ,aaj_ticker, name='aaj_ticker' ),
        path('dawn_ticker/' ,dawn_ticker, name='dawn_ticker' ),
        path('ptv_ticker/' ,ptv_ticker, name='ptv_ticker' ),
        path('neo_ticker/' ,neo_ticker, name='neo_ticker' ),
        path('24_ticker/' ,twenty_four_ticker, name='24_ticker' ),
        path('92_ticker/' ,ninety_two_ticker, name='92_ticker' ),

        path('india_today_ticker/' ,india_today_ticker, name='india_today_ticker' ),
        path('aljazeera_ticker/' ,aljazeera_ticker, name='aljazeera_ticker' ),
        path('cnn_ticker/', cnn_ticker, name='cnn_ticker'),
        path('rt_ticker/', rt_ticker, name='rt_ticker'),
        path('bbc_ticker/', bbc_ticker, name='bbc_ticker'),

        path('trending_words_local/', trending_words_local, name='trending_words_local'),
        path('trending_words_foreign/', trending_words_foreign, name='trending_words_foreign'),

        path('notifications/', notifications, name='notifications'),

        path('geo_news/' ,geo_ticker, name='geo_ticker' ),
        path('dunya_news/' ,dunya_ticker, name='dunya_ticker' ),
        path('ary_news/' ,ary_ticker, name='ary_ticker' ),
        path('samaa_news/' ,samaa_ticker, name='samaa_ticker' ),
        path('express_news/' ,express_ticker, name='express_ticker' ),
        path('gnn_news/' ,gnn_ticker, name='gnn_ticker' ),
        path('hum_news/' ,hum_ticker, name='hum_ticker' ),
        path('aaj_news/' ,aaj_ticker, name='aaj_ticker' ),
        path('dawn_news/' ,dawn_ticker, name='dawn_ticker' ),
        path('ptv_news/' ,ptv_ticker, name='ptv_ticker' ),
        path('neo_news/' ,neo_ticker, name='neo_ticker' ),
        path('24_news/' ,twenty_four_ticker, name='24_ticker' ),
        path('92_news/' ,ninety_two_ticker, name='92_ticker' ),

        path('india_today_news/' ,india_today_ticker, name='india_today_ticker' ),
        path('aljazeera_news/' ,aljazeera_ticker, name='aljazeera_ticker' ),
        path('cnn_news/', cnn_ticker, name='cnn_ticker'),
        path('rt_news/', rt_ticker, name='rt_ticker'),
        path('bbc_news/', bbc_ticker, name='bbc_ticker'),

        path('keywords_cloud_local/', keywords_cloud_local, name='keywords_cloud_local'),
        path('trending_words_foreign/', trending_words_foreign, name='trending_words_foreign'),
      path('keywords_cloud_local_offline/', keywords_cloud_local_offline, name='keywords_cloud_local_offline'),
        # path('notifications/', notifications, name='notifications'),
        path('list_clearer/', list_clearer, name='list_clearer'),
        path('all_ticker/', all_ticker, name='all_ticker'),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
