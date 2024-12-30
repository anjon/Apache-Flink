import json
from typing import List
from confluent_kafka import Producer
from alpaca_config.keys import config
from alpaca_trade_api import REST

def get_producer(brokers: List[str]):
    producer = Producer({
        'bootstrap.servers': brokers,
        'key.serializer': str.encode,
        'value.serializer': lambda v: json.dumps(v).encode('utf-8')
    })
    return producer


def produce_historical_news(
        redpanda_client: Producer,
        start_date: str,
        end_date: str,
        symbols: List[str],
        topic: str
    ):
    key_id = config['key_id'],
    secret_key = config['secret_key'],
    base_url = config['base_url']

    api = REST()

if __name__ == "__main__":
    produce_historical_news()