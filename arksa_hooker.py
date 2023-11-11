import requests
import json
import time

def get_server_status(api_token, server_id):
    """ Function to get the status of the ARK server. """
    url = f"https://api.battlemetrics.com/servers/{server_id}"
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = json.loads(response.text)['data']['attributes']
        return data['status'], data.get('players'), data.get('maxPlayers')
    else:
        return None, None, None

def send_to_discord(webhook_url, message):
    """ Function to send message to a Discord channel via webhook. """
    data = {
        "content": message,
        "username": "5450-Tracker"
    }
    response = requests.post(webhook_url, json=data)
    if response.status_code != 204:
        print(f"Failed to send message to Discord. Status Code: {response.status_code}, Response: {response.text}")

def main():
    api_token = "<battlemetrics-api-token>"
    server_id = "<server-id-from-metrics-page-url>"
    webhook_url = "<discord-channel-webhook-url>"

    print("5450-Tracker online...")
    send_to_discord(webhook_url, "5450-Tracker online...")

    last_status = None  # Placeholder for storing the last status

    while True:
        current_status, player_count, max_players = get_server_status(api_token, server_id)
        
        if current_status is None:
            print("Failed to retrieve server status.")
        else:
            # Print the current status and player count to the terminal
            print(f"Server Status: {current_status}")
            if current_status == "online":
                print(f"Player Count: {player_count}/{max_players}")

            # Check if the status is different than the last check and send to Discord if it has changed
            if current_status != last_status:
                emoji = "<:SERVERISBACK:1170863426092941473>" if current_status == "online" else "<:RIPSERVER:1170863355112730694>"
                send_to_discord(webhook_url, emoji)

            # Update the last known status
            last_status = current_status
        
        time.sleep(10)  # Check the server status every 10 seconds

if __name__ == "__main__":
    main()
