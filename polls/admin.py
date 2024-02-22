from django.contrib import admin
from .models import words_to_be_searched_model,Ticker_Extraction_Model,Character_Comparison,Notification,UserKeyword
admin.site.register(Ticker_Extraction_Model)
admin.site.register(Character_Comparison)
admin.site.register(words_to_be_searched_model)
#Notification Models
admin.site.register(Notification)
admin.site.register(UserKeyword)


# Register your models here.
