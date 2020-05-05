from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import requests
import os, json, boto3
from botocore.client import Config
import botocore

#botocore.session.Session().set_debug_logger()

from .models import Greeting
from . import models, forms 

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")
    #return HttpResponseRedirect(reverse("submit_form"))
    #r = requests.get('http://httpbin.org/status/418')
    #print(r.text)
    #return HttpResponse('<pre>' + r.text + '</pre>')
    
    # load $TIMES, otherwise substitute 3
    #times = int(os.environ.get('TIMES',3))
    #return HttpResponse('Hello! ' * times)

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})

def sign_s3(request):
    S3_BUCKET = os.environ.get("S3_BUCKET")
    #print("AWS_ACCESS_KEY_ID: "+os.environ.get("AWS_ACCESS_KEY_ID")+\
    #    "\n AWS_SECRET_ACCESS_KEY: "+os.environ.get("AWS_SECRET_ACCESS_KEY"))
    file_name = request.GET["file_name"]
    file_type = request.GET["file_type"]

    s3 = boto3.client("s3")#, aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"), aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),)#, config = Config( signature_version = 's3v4'))

    print(S3_BUCKET)
    presigned_post = s3.generate_presigned_post(
        Bucket = S3_BUCKET,
        Key = file_name,
        
        Fields = None, #{ "acl": "public-read", "Content-Type": file_type },
        Conditions = None, #[ {"acl": "public-read"}, {"Content-Type": file_type},],
        
        ExpiresIn = 3600,
    )

    return HttpResponse( json.dumps({
        "data": presigned_post,
        "url": 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name),
        "key": file_name,
    }), content_type="text/json")

def get_image_url(request):
    filename = request.GET["file_name"]
    S3_BUCKET = os.environ.get("S3_BUCKET")
    
    params = {"Bucket": S3_BUCKET, "Key": filename}
    expire = 3600
    s3_client = boto3.client("s3")

    url = s3_client.generate_presigned_url("get_object", Params=params, ExpiresIn=expire)
    return HttpResponse(url, content_type="text/plain")


def submit_form(request):
    form2 = forms.ProfileChangeForm()
    if request.POST:
        form = forms.ProfileChangeForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            full_name = form.cleaned_data["full_name"]
            avatar_url = form.cleaned_data["avatar_url"]
            models.Account.update_account(username, full_name, avatar_url)
            return render(request, "hello/update_profile_success.html")
    
    return render(request, "hello/submit_form.html", {"form": form2} )
