def get_balance(api, api_base_url, account_id):
    response = api.get(f"{api_base_url}/accounts/{account_id}")
    response.raise_for_status()
    return response.json()["balance"]

def find_transactions(api, api_base_url, account_id, description):
    response = api.get(f"{api_base_url}/accounts/{account_id}/transactions")
    assert response.status_code == 200
    transactions = response.json()
    mine = [t for t in transactions if t["description"] == description]
    return mine

#descriptions: "Funds Transfer Recieved", "Funds Transfer Sent", "Bill Payment to {name}"