from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .models import CarModel
# from .restapis import related methods
# from .restapis import get_dealers_from_cf, get_dealers_by_state_from_cf, get_dealer_reviews_from_cf, post_request, get_request
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request, get_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

from datetime import datetime

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)

# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    if request.method == "POST":
        username = request.POST['usernameInput']
        password = request.POST['passwordInput']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        
        return redirect("djangoapp:index")
        
# Create a `logout_request` view to handle sign out request
def logout_request(request):
    if request.method == "GET":
        logout(request)
        return redirect("djangoapp:index")

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}

    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)

    # If it is a POST request, then create the user and return to the main page
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))

        # If it is a new user
        if (user_exist == False):
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, 
                            last_name=last_name, password=password)
            # Login the user and redirect to course list page
            login(request, user)
            return redirect("djangoapp/index.html")
        else:
            # context = {"ErrorMessage":"Username already exists in the system. Please register a different username."}
            return render(request, 'djangoapp/registration.html', context)
    
# ...

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        # return render(request, 'djangoapp/index.html', context)
        url = "https://d480556a.us-south.apigw.appdomain.cloud/api/dealership"
        #get dealers from the URL
        
        #if state was given as a parameter then get the entries related to that 'state'
        if "state" in request.GET:
            print(">>>> state was found in GET request")
            dealerships = get_dealer_by_state(url, state=request.GET["state"])
        
        #else, get all dealerships
        else:
            print(">>> getting all dealerships")
            dealerships = get_dealers_from_cf(url)
            print(">>> SUCCESS, got all dealerships")

        # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # # Return a list of dealer short name
        # return HttpResponse(dealer_names)

        context['dealerships'] = dealerships
        return render(request, 'djangoapp/index.html', context)    



# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://d480556a.us-south.apigw.appdomain.cloud/api/reviews"
        reviews = get_dealer_reviews_from_cf(url, dealerId=dealer_id)
        
    # If response does not have error message
    if "msg" not in reviews:
        # review_text = " ".join([review.review + ": " + " \n" for review in reviews])
        review_text = " ".join([review.review + ": " + review.sentiment + " | " for review in reviews])
        return HttpResponse(review_text)
    else:
        # Return response error
        return HttpResponse(str(reviews))

    # return render(request, 'djangoapp/dealer_details.html', context)

    


# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    url = "https://d480556a.us-south.apigw.appdomain.cloud/api/review"
    # if request.method == "GET":
    #     context = {
    #         "cars": CarModel.objects.all(),
    #         "dealer": get_dealers_from_cf(url, dealerId=dealer_id)[0],
    #     }
    #     return render(request, 'djangoapp/add_review.html', context)

    if request.user.is_authenticated and request.method == "POST":
        url = "https://d480556a.us-south.apigw.appdomain.cloud/api/review"
        review = dict()
        review["id"] = request.POST("id")
        review["time"] = request.POST("time")
        review["dealership"] = dealer_id
        review["review"] = request.POST("review")
        review["purchase"] = request.POST("purchase")
        review["purchase_date"] = request.POST("purchase_date")
        review["car_make"] = request.POST("car_make")
        review["car_model"] = request.POST("car_model")
        review["car_year"] = request.POST("car_year")
        
        json_payload = {review:review}
        response = post_request(url, json_payload)
        return HttpResponse(str(response))

    else:
        return HttpResponse("Only authenticated users can submit reviews")
    # return redirect("djangoapp:dealer_details", dealerId=dealer_id)    
