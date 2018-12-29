# Recipes-Alert-System-In-Kafka
Kafka producer consumer sample

This is a modified version of programs based on an article ["Getting started with Apache Kafka in Python"](https://towardsdatascience.com/getting-started-with-apache-kafka-in-python-604b3250aa05)

In `producer-raw-recipies.py`, it uses `requests` to get recipes from [allrecipes.com](https://www.allrecipes.com) and stores to topic `raw_recipes`.

In `producer_consumer_parse_recipes.py`, it consume the message from `raw_recipes` and parse the recipes then stores into another topic `parsed_recipes`.

In `consumer-notification.py`, it consume the parsed recipes and print out an alerts if the calories of a recipe is greater than 200.

To run the program you need a stand alone Zookeeper and Kafka. Please refer to the article ["Getting started with Apache Kafka in Python"](https://towardsdatascience.com/getting-started-with-apache-kafka-in-python-604b3250aa05) for more info.
