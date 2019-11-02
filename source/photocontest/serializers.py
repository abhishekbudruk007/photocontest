from rest_framework import serializers
from .models import Contest,Participants,Winner



class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model=Contest
        fields= "__all__"


class ParticipantsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Participants
        fields= "__all__"



class WinnerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Winner
        fields= "__all__"




