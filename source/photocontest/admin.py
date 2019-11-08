from django.contrib import admin
from django.contrib.admin import DateFieldListFilter

# Register your models here.

# Register your models here.
from .models import Contest,Participants,Winner,Likes
from django.db.models import Count
from django.db.models import Max




# Register your models here.
from operator import attrgetter
from accounts.utils import send_mail_to_winner
def declare_winner(modeladmin,request,queryset):
    for contest_object in queryset:
        print("qs",contest_object)
        like_objects =Likes.objects.annotate(likescount=Count('participant_user')).filter(participant_contest=contest_object)
        winner_list = max(like_objects, key=attrgetter('likescount')) #To return the object of max count of likecount
        print("Winner",winner_list.participant_id.participant_user.email)
        email = winner_list.participant_id.participant_user.email
        send_mail_to_winner(winner_list,email)



class ContestFilters(admin.ModelAdmin):
    list_display = ('id', 'contest_name', 'contest_lastdate', 'created_at', 'updated_at')
    search_fields = ( 'id','contest_name','contest_lastdate')
    list_filter = (
        ('contest_lastdate', DateFieldListFilter),
    )
    actions = [declare_winner]



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
