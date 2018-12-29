import requests
from time import sleep
from bs4 import BeautifulSoup
from kafka import KafkaProducer

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6)'
    + ' AppleWebKit/537.36 (KHTML, like Gecko)'
    + ' Chrome/66.0.3359.181 Safari/537.36',
    'Pragma': 'no-cache'
}


def fetch_raw(recipe_url):
    html = None
    print('Processing..{}'.format(recipe_url))
    try:
        r = requests.get(recipe_url, headers=headers)
        if r.status_code == 200:
            html = r.text
    except Exception as e:
        print('Exception while accessing raw html')
        print(str(e))
    finally:
        return html.strip()


def get_recipes():
    recipies = []
    url = 'https://www.allrecipes.com/recipes/96/salad/'
    print('Accessing list')
    r = None
    try:
        r = requests.get(url, headers=headers)
    except Exception as e:
        print('Exception in get_recipes')
        print(str(e))
    else:
        if r and r.status_code == 200:
            html = r.text
            soup = BeautifulSoup(html, 'lxml')
            links = soup.select('.fixed-recipe-card__h3 a')
            for link in links:
                sleep(2)
                recipe = fetch_raw(link['href'])
                yield recipe


def publish_message(producer_instance, topic_name, key, value):
    try:
        key_bytes = bytes(key, encoding='utf-8')
        value_bytes = bytes(value, encoding='utf-8')
        producer_instance.send(topic_name, key=key_bytes, value=value_bytes)
        producer_instance.flush()
        print('Message published successfully.')
    except Exception as e:
        print('Exception in publishing message')
        print(str(e))


def connect_kafka_producer():
    _producer = None
    try:
        _producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
    except Exception as e:
        print('Exception while connecting Kafka')
        print(str(e))
    finally:
        return _producer


if __name__ == '__main__':
    # all_recipes = get_recipes()
    # if all_recipes:
    kafka_producer = connect_kafka_producer()
    if kafka_producer:
        for recipe in get_recipes():
            publish_message(
                kafka_producer,
                'raw_recipes',
                'raw',
                recipe.strip()
            )
        kafka_producer.close()
