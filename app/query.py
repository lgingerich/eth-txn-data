from google.cloud import bigquery
from google.oauth2 import service_account

def txnQuery(eth_address):    
    credentials = service_account.Credentials.from_service_account_file(
        "app\BIGQUERY-CREDENTIAL.json"
    )

    # Construct a BigQuery client object
    client = bigquery.Client(credentials=credentials)

    # Construct query
    query = """
    SELECT `hash`, nonce, block_timestamp, from_address, to_address, value/power(10, 18) as value, (gas_price/power(10, 18))*receipt_gas_used as txn_fee
    FROM bigquery-public-data.crypto_ethereum.transactions
    WHERE to_address = LOWER(@eth_address) OR from_address = LOWER(@eth_address)
    ORDER BY block_timestamp DESC
    """

    # Configure 
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("eth_address", "STRING", eth_address)
        ]
    )

    # Make API call and save as pandas dataframe
    df = (
        client.query(query, job_config=job_config)
        .result()
        .to_dataframe(
            # Optionally, explicitly request to use the BigQuery Storage API. As of
            # google-cloud-bigquery version 1.26.0 and above, the BigQuery Storage
            # API is used by default.
            create_bqstorage_client=True,
        )
    )

    # Convert dataframe to dictionary. This outputs a nested dictionary.
    txnData = df.to_dict(orient="list")
    
    return txnData