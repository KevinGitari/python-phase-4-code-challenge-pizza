from models import db, Restaurant, Pizza, RestaurantPizza
from flask import Flask, jsonify, request

def _restaurant_routes(app):

    @app.route("/restaurants", methods=["GET"])

    def get_restaurants():
        restaurants = Restaurant.query.all()
        return jsonify([restaurant.to_dict() for restaurant in restaurants]), 200
    
    @app.route("/restaurants/<int:id>", methods=["GET"])

    def get_restaurant(id):
        restaurant = Restaurant.query.get(id)

        if not restaurant:
            return jsonify({"error": "Restaurant not found"}), 404
        return jsonify(restaurant.to_dict()), 200
    
    @app.route("/restaurants/<int:id>", methods=["DELETE"])
    
    def delete_restaurant(id):
        restaurant = Restaurant.query.get(id)

        if not restaurant:
            return jsonify({"error": "Restaurant not found"}), 404
        db.session.delete(restaurant)
        db.session.commit()
        return jsonify({}), 204
    
    @app.route("/pizzas", methods=["GET"])
    def get_pizzas():
        pizzas = Pizza.query.all()
        return jsonify([pizza.to_dict() for pizza in pizzas]), 200
    
    @app.route('/restaurant_pizzas', methods=['POST'])
    def create_restaurant_pizza():
        data = request.get_json()
        try:
            restaurant_pizza = RestaurantPizza(
                price=data['price'],
                pizza_id=data['pizza_id'],
                restaurant_id=data['restaurant_id']
            )

            db.session.add(restaurant_pizza)
            db.session.commit()
            return jsonify(restaurant_pizza.to_dict()), 201
        except ValueError as e:
            return jsonify({"errors": [str(e)]}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 400
