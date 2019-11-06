from django.contrib import admin
from django.contrib.admin import DateFieldListFilter

# Register your models here.

# Register your models here.
from .models import Contest,Participants,Winner,Likes



# Register your models here.


class ContestFilters(admin.ModelAdmin):
    list_display = ('id', 'contest_name', 'contest_lastdate', 'created_at', 'updated_at')
    search_fields = ( 'id','contest_name','contest_lastdate')
    list_filter = (
        ('contest_lastdate', DateFieldListFilter),
    )

class ParticipantFilters(admin.ModelAdmin):
    list_display = ('id', 'participant_user', 'participant_contest', 'photo','created_at', 'updated_at')
    search_fields = ( 'id','participant_user','participant_contest')
    list_filter = (
        ('updated_at', DateFieldListFilter),
    )
class LikesFilters(admin.ModelAdmin):
    list_display = ('id','participant_id', 'participant_contest')
    search_fields = ('id','participant_id','participant_contest')



admin.site.register(Contest,ContestFilters)
admin.site.register(Participants,ParticipantFilters)
admin.site.register(Winner)
admin.site.register(Likes,LikesFilters)
