# Python Django Client-Side File Upload Sample

## related documents

* [Direct to S3 File Uploads in Python](https://devcenter.heroku.com/articles/s3-upload-python)
* [Getting Started on Heroku with Python](https://devcenter.heroku.com/articles/getting-started-with-python)

## URLs

| url | returns | format |
|-----|---------|--------|
| /submit_form | demo main page | HTML |
| /sign_s3 | presigned POST url, etc. | JSON |
| /get_image_url | presigned GET url | text |

## requirements

* `heroku` environment
* `boto3` library
* `AWS account`

## Usage

* create S3 IAM, Backet
  * IAM needs permission to `s3:PutObject`, `s3:GetObject` for the Backet.
  * probably, creating Backet in `us-east-1` protect you from bugs.
* Fill up `.env` accords with `.env-sample`

and

```sh
pip install boto3
python manage.py migrate
heroku local
```

Then access to `localhost:5000/submit_form`, you can try S3 uploading via presigned-post and S3 downloading via presigned-url.