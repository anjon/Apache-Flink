kafka-topics --bootstrap-server broker:29092 --list
kafka-topics --bootstrap-server broker:29092 --list --topic financial_transactions
kafka-console-consumer --bootstrap-server broker:29092 --topic financial_transactions --from-beginning

'''
GET transactions/_search

POST _reindex
{
    "source": {
        "index": "transactions"
    },
    "dest": {
        "index": "transactions_part1"
    },
    "script": {
        "source": """
            ctx._source.transactionDate = new Date(ctx._source.transactionDate).toString();
            """
    }
}

GET transactions_part1/_search
'''

'''
POST _reindex
{
    "source": {
        "index": "transactions"
    },
    "dest": {
        "index": "transactions_part2"
    },
    "script": {
        "source": """
        SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss");
        formatter.setTimeZone(TimeZone.getTimeZone('UTC'));
        ctx._source.transactionDate = formatter.format(new Date(ctx._source.transactionDate));
        """
    }
'''