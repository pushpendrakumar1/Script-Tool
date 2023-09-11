from django.contrib import admin
# from myapp.models import signup


 
# admin.site.register(signup)

# Register your models here.
from django.contrib import admin

from myapp.models import ScriptProcessingConfig


    

class con(admin.ModelAdmin):

    list_display = ('input_folder1','input_folder2','enter_id1','enter_id2')    
    
   





admin.site.register(ScriptProcessingConfig, con)











