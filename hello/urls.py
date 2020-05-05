from django.urls import path

from hello import views

urlpatterns = [
    path("", views.index, name="index"),
    path("sign_s3", views.sign_s3, name="sign_s3"),
    #path("submit_form", views.submit_form, name="submit_form"),
    path("get_image_url", views.get_image_url, name="get_image_url"),
]