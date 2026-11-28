def get_balance(api, api_base_url, account_id):
    response = api.get(f"{api_base_url}/accounts/{account_id}")
    response.raise_for_status()
    return response.json()["balance"]