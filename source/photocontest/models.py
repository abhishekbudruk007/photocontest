from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Contest(BaseModel):
    contest_name = models.CharField(max_length=20)
    contest_lastdate=models.DateTimeField(null=True,blank=True)


class Participants(BaseModel):
    participant_user = models.ForeignKey(User, on_delete=models.CASCADE)
    participant_contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    photo = models.ImageField(default='image-not-found.png')
    photo_thumbnail = ImageSpecField(source='photo',
                                        processors=[ResizeToFill(150, 100)],
                                        format='PNG',
                                        options={'quality': 60})
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)


class Winner(BaseModel):
    winner_name = models.ForeignKey(User, on_delete=models.CASCADE)