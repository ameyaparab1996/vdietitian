from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class UserDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    #additional attributes
    date_of_birth = models.DateField()
    weight = models.FloatField()
    height = models.FloatField()
    gender = models.CharField(max_length=6,choices=(('Male','Male'),
                                                    ('Female','Female')))
    goal = models.CharField(max_length=20,choices=(('Gain weight','Gain weight'),
                                                    ('Loose weight','Loose weight'),
                                                    ('Stay Fit','Stay Fit')))
    profession = models.CharField(max_length=50,choices=(('Student','Student'),
                                                        ('Graduate/Intern/Fresher Job/Work from Home','Graduate/Intern/Fresher Job/Work from Home'),
                                                        ('Corporate Work','Corporate Work'),
                                                        ('Medical/Education/Governmental work','Medical/Education/Governmental work'),
                                                        ('Physical Labour Work','Physical Labour Work')))
    lifestyle = models.CharField(max_length=20,choices=(('Sedentary','Sedentary'),
                                                        ('Lightly active','Lightly active'),
                                                        ('Moderately active','Moderately active'),
                                                        ('Very active','Very active'),
                                                        ('Extremely active','Extremely active')))
    medical_history = models.CharField(max_length=40,choices=(('None','None'),
                                                            ('Diabities','Diabities'),
                                                            ('Hypothyroidism','Hypothyroidism'),
                                                            ('Cholesterol','Cholesterol')))
    food_preference = models.CharField(max_length=20,choices=(('Veg','Veg'),
                                                            ('Non-veg','Non-veg'),
                                                            ('Veg including Egg','Veg including Egg')))


    #Dietplan attribute
    dietPlan = JSONField(default={})

    BMR = models.FloatField(default=0)

    calorieintake = models.FloatField(default=0)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'UserDetails'


class feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback_on = models.DateTimeField(default=timezone.now())
    weight = models.FloatField()
    is_positive = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
