
import requests 
import json
def verify_file(filename, filelocation):
    API_KEY = "5d875868c7f0f46245d39c18b56510124efd59babb14e3d18654d06fb125922c"
    url = "https://www.virustotal.com/api/v3/files/upload_url"
    headers = {
        "accept": "application/json",
        "x-apikey": API_KEY
    }
    response = json.loads(requests.get(url, headers=headers).text)
    upload_url = response['data']
    files = {
        "file": (
            filename,
            open(filelocation, "rb")
        )
    }
    response = requests.post(upload_url, files=files, headers=headers)
    upload_response = json.loads(response.text)
    analysis_id = upload_response['data']['id']
    analysis_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
    response = requests.get(analysis_url, headers=headers)
    analysis_report = json.loads(response.text)
    if 'data' in analysis_report and 'stats' in analysis_report['data']['attributes']:
        malicious_count = analysis_report['data']['attributes']['stats']['malicious']
        if malicious_count > 0:
            print("Malicious File")
            return True
        else:
            print("Normal File")
            return False
    else:
        print("Error retrieving analysis results.")
        return False
    return False
