import sys
from django.db import models

class Instructor(models.Model):
    name = models.CharField(max_length=80, primary_key=True)

class Course(models.Model):
    com_cod = models.IntegerField()
    course_number = models.CharField(max_length=20)
    course_title = models.CharField(max_length=50)
    course_lec_units = models.IntegerField(null=True)
    course_prac_units = models.IntegerField(null=True)
    course_units = models.IntegerField()

class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    section_code = models.CharField(max_length=10)
    instructors = models.ManyToManyField(Instructor)
    room = models.CharField(max_length=20, null=True)
    compre_date = models.DateField(null=True)
    compre_session = models.BooleanField(null=True)
    days_and_hours = models.CharField(max_length=20, null=True) # replace with a more suitable model later

