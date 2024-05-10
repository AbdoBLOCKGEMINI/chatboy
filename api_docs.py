import json

scoopsie_api_docs = {
    "base_url": "http://127.0.0.1:5000/",
    "endpoints": {
        "/avaliable_cars": {
            "method": "GET",
            "description": "Retrieve the menu of flavors and customizations.",
            "parameters": None,
            "response": {
                "description": "A JSON object containing available flavors and toppings along with their counts.",
                "content_type": "application/json"
            }
        },
        "/drivers_confirmation": {
            "method": "GET",
            "description": "Retrieve current special offers and discounts.",
            "parameters": None,
            "response": {
                "description": "A JSON object listing the current special offers and discounts.",
                "content_type": "application/json"
            }
        },
        "/customer-reviews": {
            "method": "GET",
            "description": "Retrieve customer reviews for the ice cream store.",
            "parameters": None,
            "response": {
                "description": "A JSON object containing customer reviews, ratings, and comments.",
                "content_type": "application/json"
            }
        },

    }
}

scoopsie_api_docs = json.dumps(scoopsie_api_docs, indent=2)
