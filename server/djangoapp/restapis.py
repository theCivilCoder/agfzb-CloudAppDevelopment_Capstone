import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth
from .models import CarDealer, DealerReview


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print(f"GET from url: {url}")
    
    print(">>> try to read database")
    response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'})


    # try:
    #     print(">>> try to read database")
    #     response = requests.get(url, param=kwargs, headers={'Content-Type': 'application/json'})
    # except: 
    #     #if any errors occurs
    #     print("Network Exception Occurred, GET request did not succeed.")
    
    status_code = response.status_code
    print(f"Status: {status_code}")

    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, payload, **kwargs):
    print(kwargs)
    print(f"POST from url: {url}")

    try:
        response = requests.post(url, params=kwargs, json=payload)
    except:
        #If any error occurs
        print("Network Exception Occurred, POST request did not succeed.")

    status_code = response.status_code
    print(f"Status: {status_code}")

    json_data = json.loads(response.text)
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url)
    print(f">>>> json_result: '{json_result}'")
    if json_result:
        #entries list of the json_result is the list of dealerships
        dealers = json_result["entries"]

        #create a dealer object for each entry
        for dealer in dealers:
            dealer_obj = CarDealer(CDid=dealer["id"], city=dealer["city"], state=dealer["state"], st=dealer["st"],
                                        address=dealer["address"], zipAd=dealer["zip"], lat=dealer["lat"], longit=dealer["long"],
                                        full_name=dealer["full_name"])
            results.append(dealer_obj)

    return results



def get_dealers_by_state_from_cf(url, **kwargs):
    return get_dealers_from_cf(url, **kwargs)


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []

    json_result = get_request(url)
    if json_result:
        # url will return entries for reviews for a particular dealer
        reviews = json_result["entries"]
        # For each dealer object
        for review in reviews:
            # Create a CarDealer object with values in `doc` object
            review_obj = DealerReview( id=review_doc["id"], name=review["name"], dealership=review["dealership"],
                review=review["review"], purchase=review["purchase"]
            )
            #Check if optional attributes were returned for this specific review
            if "purchase_date" in review:
                review_obj.purchase_date=review["purchase_date"]
            if "car_make" in review:    
                review_obj.car_make=review["car_make"], 
            if "car_model" in review:    
                car_model=review["car_model"]
            if "car_year" in review:    
                car_year=review["car_year"],   
            
            results.append(review_obj)
    return results    





# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative







