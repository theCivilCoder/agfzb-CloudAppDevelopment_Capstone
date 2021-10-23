from django.db import models
from django.utils.timezone import now
from django.conf import settings

# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    country = models.CharField(max_length=50, default='Canada')

    def __str__(self):
        return "Name: " + self.name 


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealerId = models.IntegerField(null=True)
    name = models.CharField(max_length=50)
    car_type = models.CharField(max_length=10, choices = ( ("Sedan", "Sedan"), ("SUV", "SUV"), ("WAGON", "WAGON") ), default="Sedan")    
    year = models.DateField()

    def __str__(self):
        return self.name

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, state, full_name, CDid, lat, longit, short_name, st, zipAd):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = CDid
        # Location lat
        self.lat = lat
        # Location long
        self.longit = longit
        # Dealer short name
        self.short_name = short_name
        # Dealer st
        self.st = st
        # Dealer state
        self.state = state
        # Dealer Full Name
        self.full_name = full_name
        # Dealer zip
        self.zipAd = zipAd

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, name, dealership, review, purchase, Rid, purchase_date=None, car_make=None, car_model=None, car_year=None, sentiment=None):
        self.name = name
        self.dealership = dealership
        self.purchase = purchase
        self.review = review       
        self.id = Rid

        self.purchase_date = purchase_date
        self.car_make = car_make 
        self.car_model = car_model 
        self.car_year = car_year
        self.sentiment = sentiment 

    def __str__(self):
        return "Review: " + self.review


