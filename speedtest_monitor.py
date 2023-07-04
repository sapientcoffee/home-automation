#!/usr/bin python3

import sys
import json
import requests

def ubi_upload():
    data = json.load(sys.stdin)
    # apiKey = os.environ["ubidotsApi"]

    type = data['type']

    if type == 'log':
        # some error use print below to see response, alternatively run $ speedtest -f json
        pass
    elif type == 'result':
        # success, upload to ubidots
        upload_to_ubi(data)
    else:
        # uncaught error use print below to see response, alternatively run $ speedtest -f json
        pass

def upload_to_ubi(data):
    try:
        payload = {
            'download': round(data["download"]["bandwidth"] / (1024*1024) / 0.125, 2),
            'upload': round(data["upload"]["bandwidth"] / (1024*1024) / 0.125, 2),
            'ping': round(data["ping"]["latency"], 2), # 0ms to 20ms is considered good 
            'jitter': round(data["ping"]["jitter"], 2),
            'packet-loss': round(data["packetLoss"], 2),
            'bytes_used': round((data["download"]["bytes"] + data["upload"]["bytes"] ) / (1024*1024), 2),
        }

        r = requests.post('http://industrial.api.ubidots.com/api/v1.6/devices/raspberry-pi/?token='os.environ["ubiapi"]'', data=payload)
        r.raise_for_status()

        # Print the server's response Uncomment the next line for debugging purposes
        print(r.content)

    except Exception as identifier:

        print(identifier)

if __name__ == '__main__':
    ubi_upload()