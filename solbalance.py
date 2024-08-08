import requests
import time

def get_solana_balance(public_key, retries=3):
    url = "https://api.mainnet-beta.solana.com"
    headers = {"Content-Type": "application/json"}
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBalance",
        "params": [public_key]
    }
    
    for attempt in range(retries):
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            result = response.json().get("result", {})
            return result.get("value", 0) / 1e9  # Convert from lamports to SOL
        else:
            print(f"Error checking balance for {public_key}: {response.text}")
            time.sleep(2 ** attempt)  # Exponential backoff
    
    return 0

def check_balances_from_file(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            public_key = line.strip()
            if public_key:
                balance = get_solana_balance(public_key)
                if balance > 0:
                    print(f"Public Key: {public_key} has balance: {balance} SOL")
                    outfile.write(f"{public_key},{balance}\n")
                time.sleep(1)  # Delay added to avoid hitting the rate limit

if __name__ == "__main__":
    input_file = "discovered_keys.txt"  # Replace with your input file
    output_file = "public_keys_with_balance.txt"  # Replace with your output file
    check_balances_from_file(input_file, output_file)