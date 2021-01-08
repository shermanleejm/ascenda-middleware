import json
import boto3
import urllib
from urllib import request, parse
from datetime import datetime

ENDPOINT = "http://itsa-backend-dev8.ap-southeast-1.elasticbeanstalk.com/api/loyaltyprogram/generatebatchfile"
BEST_DATE = 20200801

def lambda_handler(event, context):
    date = datetime.now().strftime("%Y%m%d")
    ## TODO: Change for production
    # if int(date) > BEST_DATE:
    #     date = str(BEST_DATE)
    data = parse.urlencode({"date": date}).encode("utf-8")
    # data = json.dumps(data).encode("utf-8")
    req = request.Request(ENDPOINT, data=data)
    resp = request.urlopen(req)
    print (resp.read())
    return "Hello World, Sherman was here"
