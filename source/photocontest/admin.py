from django.contrib import admin
from django.contrib.admin import DateFieldListFilter

# Register your models here.

# Register your models here.
from .models import Contest,Participants,Winner



# Register your models here.


class ContestFilters(admin.ModelAdmin):
    list_display = ('id', 'contest_name', 'contest_lastdate', 'created_at', 'updated_at')
    search_fields = ( 'id','contest_name','contest_lastdate')
    list_filter = (
        ('contest_lastdate', DateFieldListFilter),
    )


admin.site.register(Contest,ContestFilters)
admin.site.register(Participants)
admin.site.register(Winner)
