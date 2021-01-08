from django.http import HttpResponse, JsonResponse
import sys
import requests
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def health(request):
    return HttpResponse("OK")


@csrf_exempt
def ci_cd_test(request):
    return HttpResponse("CI CD WORKS AS OF TODAY!!! HELLO ITSA INITAL APP ! WORKS!")

@csrf_exempt
def sticky_sessions(request):
    def get_ec2_hostname():
        if "test" in sys.argv[1]:
            return False
        try:
            ipconfig = 'http://169.254.169.254/latest/meta-data/local-ipv4'
            return requests.post(ipconfig, timeout=3).text
        except Exception:
            return "Not an ec2_instance"

    ec2_host = get_ec2_hostname()
    return HttpResponse(ec2_host)
