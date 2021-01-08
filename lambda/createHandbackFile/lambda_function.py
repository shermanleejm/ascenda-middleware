import json
import urllib.request

ENDPOINT = "http://itsa-backend-dev8.ap-southeast-1.elasticbeanstalk.com/api/loyaltyprogram/newbatchfile"

def lambda_handler(event, context):
    try:
        print (event)
        bucket = event["Records"][0]['s3']['bucket']['name']
        key = event["Records"][0]['s3']['object']['key']
        print (bucket, key)
        url_path = ENDPOINT + f"?bucket={bucket}&key={key}"
        req = urllib.request.Request(url_path)
        response = urllib.request.urlopen(req)
        contents = response.read()
        print (contents)
        return contents
    except Exception as e:
        print (f"Error is {e}")

        