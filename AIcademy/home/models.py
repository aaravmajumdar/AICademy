from django.db import models

# Create your models here.

class studyresource(models.Model):
    subjectid = models.AutoField(primary_key=True)
    subject = models.CharField(max_length = 255)
    chaptername = models.CharField(max_length = 255)
    standard = models.CharField(max_length = 255)
    booktitle = models.CharField(max_length = 255)
    file = models.FileField(upload_to='uploads/')

def __str__(self):
    return "%s %s" %(self.name, self.email)