from django.db import models

# Create your models here.


class Question(models.Model):
    text = models.CharField(max_length=1000)
    difficulty = models.IntegerField()
    option_1 = models.CharField(max_length=255)
    option_2 = models.CharField(max_length=255)
    option_3 = models.CharField(max_length=255)
    option_4 = models.CharField(max_length=255)
    correct_option = models.IntegerField()

    def to_dict(self):
        return dict(text=self.text,
                    option_1=self.option_1,
                    option_2=self.option_2,
                    option_3=self.option_3,
                    option_4=self.option_4,
                    )
