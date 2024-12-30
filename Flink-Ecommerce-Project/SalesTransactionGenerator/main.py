from datetime import datetime
import json
import random
from faker import Faker
from confluent_kafka import SerializingProducer
from time import sleep


fake = Faker()
def generate_sales_transactions():
    user = fake.simple_profile()

    return {
        'transactionId': fake.uuid4(),
        'productId': random.choice(['Product1', 'Product2', 'Product3', 'Product4', 'Product5', 'Product6']),
        'productName': random.choice(['Laptop', 'Mobile', 'Watch', 'Tablet', 'Headphone', 'Speaker']),
        'productCategory': random.choice(['Electronic', 'Fashion', 'Grocery', 'Home', 'Beauty', 'Sports']),
        'productPrice': round(random.uniform(10, 1000), 2),
        'productQuantity': random.randint(1, 10),
        'productBrand': random.choice(['Apple', 'Samsung', 'Oneplus', 'Xioami', 'Motorolla', 'Sony']),
        'currency': random.choice(['USD', 'GBP', 'PLN']),
        'customerId': user['username'],
        'transactionDate': datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
        'paymentMethod': random.choice(['Credit_Card', 'Debit_Card', 'Online_Transfer'])
    }

def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic} [{msg.partition()}]')

def main():
    topic = 'financial_transactions'
    producer = SerializingProducer({
        'bootstrap.servers': 'localhost:9092'
    })

    curr_time = datetime.now()
    transaction = generate_sales_transactions()

    while (datetime.now() - curr_time).seconds < 120:
        try:
            transaction = generate_sales_transactions()
            transaction['totalAmount'] = transaction['productPrice'] * transaction['productQuantity']
            print(transaction)
            sleep(3)
            producer.produce(topic,
                             key=transaction['transactionId'],
                             value=json.dumps(transaction),
                             on_delivery=delivery_report)
            producer.poll()
            sleep(5)
        except BufferError:
            print('Buffer is full! Waiting ...')
            sleep(1)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()