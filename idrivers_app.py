from flask import Flask, jsonify
from data_store import avaliable_cars, drivers_confirmation, customer_reviews
app = Flask(__name__)


@app.route('/avaliable_cars', methods=['GET'])
def get_menu():
    """
    Retrieves the menu data.

    Returns:
        A tuple containing the menu data as JSON and the HTTP status code.
    """
    return jsonify(avaliable_cars), 200


@app.route('/drivers_confirmation', methods=['GET'])
def get_special_offers():
    """
    Retrieves the special offers data.

    Returns:
        A tuple containing the special offers data as JSON and the HTTP status code.
    """
    return jsonify(drivers_confirmation), 200


@app.route('/customer-reviews', methods=['GET'])
def get_customer_reviews():
    """
    Retrieves customer reviews data.

    Returns:
        A tuple containing the customer reviews data as JSON and the HTTP status code.
    """
    return jsonify(customer_reviews), 200



if __name__ == '__main__':
    app.run(debug=True)
