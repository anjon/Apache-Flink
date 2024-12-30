import os

config = {
    'key_id': os.getenv('ALPACA_KEY_ID'),
    'secret_key': os.getenv('ALPACA_SECRET_KEY'),
    'redpanda_brokers': 'localhost:9092, localhost:9093, localhost:9094',
    'base_url': 'https://data.alpaca.markets/v1beta1/',
    'trade_api_base_url': 'https://paper-api.alpaca.markets/v2'
}