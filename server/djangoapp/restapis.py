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
    
    # try:
    # Call to NLU service includes API key
    if "apikey" in kwargs:
        params = dict()
        params["text"] = kwargs["text"]
        params["version"] = kwargs["version"]
        params["features"] = kwargs["features"]
        params["return_analyzed_text"] = kwargs["return_analyzed_text"]
        response = requests.get(url, headers={"Content-Type": "application/json"},
                                params=kwargs, auth=HTTPBasicAuth("apikey", kwargs["apikey"]))

    # Call to Cloudant DB                            
    else: 
        print(">>> try to read database")
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={"Content-Type": "application/json"},
                                params=kwargs) 
    # except:
    #     # If any error occurs
    #     print("Network exception occurred")

    
    status_code = response.status_code
    print(f"With status: {status_code}")

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
    # Call get_request with a URL parameter
    json_result = get_request(url)
    print(f">>>> json_result: '{json_result}'")
    if json_result:
        #entries list of the json_result is the list of dealerships
        dealers = json_result["entries"]

        #create a dealer object for each entry
        for dealer in dealers:
            dealer_obj = CarDealer(CDid=dealer["id"], city=dealer["city"], state=dealer["state"], st=dealer["st"],
                                        address=dealer["address"], zipAd=dealer["zip"], lat=dealer["lat"], longit=dealer["long"],
                                        short_name=dealer["short_name"], full_name=dealer["full_name"])
            results.append(dealer_obj)

    return results



# def get_dealers_by_state_from_cf(url, **kwargs):
#     return get_dealers_from_cf(url, **kwargs)


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []

    json_result = get_request(url, **kwargs)
    if json_result:
        # url will return entries for reviews for a particular dealer
        reviews = json_result["entries"]
        
        # For each dealer object
        for review in reviews:
            print("********* Inside of review:  ", review)
            # Create a CarDealer object with values in `doc` object
            review_obj = DealerReview( Rid=review["id"], name=review["name"], dealership=review["dealership"],
                review=review["review"], purchase=review["purchase"]
            )
            #Check if optional attributes were returned for this specific review
            if "purchase_date" in review:
                review_obj.purchase_date=review["purchase_date"]
            if "car_make" in review:    
                review_obj.car_make=review["car_make"], 
            if "car_model" in review:    
                review_obj.car_model=review["car_model"]
            if "car_year" in review:    
                review_obj.car_year=review["car_year"]   

            # Assign Watson NLU review sentiment result
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
                
            results.append(review_obj)
    return results    





# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(reviewText):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/77f304ca-db74-4c86-9768-18346001104e/v1/analyze"
    params = {}

    params["apikey"] = "RdggWSwS6OhURPEvnLNAynmuBJOTPDTUPmtUPBJ3t7tq"
    params["text"] = reviewText
    params["version"] = "2021-03-25"
    params["features"] = ["sentiment"]
    params["return_analyzed_text"] = False
    params["language"] = "en"

    response = get_request(url, **params)

    if "sentiment" in response:
        return response["sentiment"]["document"]["label"]
    else:
        return ""






