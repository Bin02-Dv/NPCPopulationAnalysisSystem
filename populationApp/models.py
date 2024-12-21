from django.db import models

# Create your models here.


class PopulationData(models.Model):
    lga_name = models.CharField(max_length=100)
    population = models.IntegerField()
    male_population = models.IntegerField()
    female_population = models.IntegerField()
    year = models.IntegerField(default=2023)
    growth_rate = models.DecimalField(max_digits=4, decimal_places=2)
    density = models.IntegerField()
    households = models.IntegerField()

    def __str__(self):
        return self.lga_name