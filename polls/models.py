from django.db import models
from django.conf import settings


# Create your models here.
class Ticker_Extraction_Model(models.Model):
    channel_name=models.CharField(max_length=30,null=True,blank=True)
    channel_image=models.CharField(max_length=80,null=True,blank=True)
    ticker_image=models.CharField(max_length=60,null=True,blank=True)
    date=models.CharField(max_length=15,null=True,blank=True)
    time=models.CharField(max_length=12,null=True,blank=True)
    text_ocr=models.CharField(max_length=500,null=True,blank=True)


    def __str__(self):
        return self.date

class Character_Comparison(models.Model):
    characters_comparing=models.CharField(max_length=80,null=True,blank=True)
    def __str__(self):
        return self.characters_comparing


# class FrameSaver(models.Model):
#     Ticker_Model=models.ForeignKey(Ticker_Extraction_Model,related_name='related_ticker_model',on_delete=models.CASCADE)
#     character_foreign=models.CharField(max_length=80,null=True,blank=True)
#     def __str__(self):
#         return self.character_foreign
class words_to_be_searched_model(models.Model):
    word=models.CharField(max_length=100)
    def __str__(self):
        return self.word




#Notificaiton models


# 1. 👇 Add the following line
class Notification(models.Model):
    message = models.CharField(max_length=100)
    
    def __str__(self):
        return self.message


class UserKeyword(models.Model):
    user = models.CharField(max_length=100)
    keyword = models.CharField(max_length=100)

    def __str__(self):
        return self.keyword
    
