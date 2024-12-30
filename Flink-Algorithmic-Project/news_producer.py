import json
from typing import List
from confluent_kafka import SerializingProducer
from alpaca_config.keys import config
from alpaca_trade_api import REST
from alpaca.common import Sort
from alpaca_trade_api.common import URL

def get_producer(brokers: List[str]):
    producer = SerializingProducer({
        'bootstrap.servers': brokers,
        'key.serializer': str.encode,
        'value.serializer': lambda v: json.dumps(v).encode('utf-8')
    })
    return producer


def produce_historical_news(
        redpanda_client: SerializingProducer,
        start_date: str,
        end_date: str,
        symbols: List[str],
        topic: str
    ):
    key_id = config['key_id']
    secret_key = config['secret_key']
    base_url = config['base_url']

    api = REST(key_id=key_id,
               secret_key=secret_key,
               base_url=URL(base_url))
    
    for symbol in symbols:
        news = api.get_news(
            symbol=symbol,
            start=start_date,
            end=end_date,
            limit=5,
            sort=Sort.ASC,
            include_content=False
        )
        print(news)

if __name__ == "__main__":
    produce_historical_news(
        get_producer(config['redpanda_brokers']),
        topic='market-news',
        start_date='2024-01-01',
        end_date='2024-12-31',
        symbols=['AAPL', 'Apple']
    )