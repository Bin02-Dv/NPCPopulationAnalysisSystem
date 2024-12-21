import csv
from django.core.management.base import BaseCommand
from .models import PopulationData

class Command(BaseCommand):
    help = 'Load population data from CSV'

    def handle(self, *args, **kwargs):
        with open('path/to/katsina_population_all_lgas.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                PopulationData.objects.create(
                    lga_name=row['Name of Area'],
                    population=row['Population'],
                    male_population=row['Male Population'],
                    female_population=row['Female Population'],
                    year=row['Year'],
                    growth_rate=float(row['Growth Rate'].strip('%')),
                    density=row['Density (per sq. km)'],
                    households=row['Households']
                )
        self.stdout.write(self.style.SUCCESS('Data successfully loaded!'))