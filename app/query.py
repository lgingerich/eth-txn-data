from google.cloud import bigquery
from google.oauth2 import service_account

def txnQuery():    
    credentials = service_account.Credentials.from_service_account_file(
        "app\BIGQUERY-CREDENTIAL.json"
    )

    bqclient = bigquery.Client(credentials=credentials)

    QUERY = """
    SELECT nonce, FORMAT_DATE("%b %d %Y", block_timestamp) AS block_timestamp, from_address, to_address, value/power(10, 18) as value, gas_price/power(10, 18) as gas_price, receipt_gas_used as gas_used
    FROM bigquery-public-data.crypto_ethereum.transactions
    WHERE to_address = LOWER('0xDd8994fcA8593fE233d1a447E654efB814d69a23') OR from_address = LOWER('0xDd8994fcA8593fE233d1a447E654efB814d69a23')
    ORDER BY block_timestamp DESC
    LIMIT 5
    """

    # Save query results as pandas dataframe
    df = (
        bqclient.query(QUERY)
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

    # Convert address to MetaMask display format (i.e. 0x12ab...34bc)
    # for i in txnData:
    #     txnData["from_address"][i] = txnData["from_address"][i][0:6] + "..." + txnData["from_address"][i][-4:]    
    
    return txnData