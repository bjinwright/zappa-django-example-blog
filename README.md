# zappa-django-example-blog
An example app that shows how to setup an app using environment variables (envs) with Zappa


##Setup Guide

###Clone repo
```
git clone
```

###Create virtualenv

```
mkvirtualenv bjblog -a ~/yourpathto/repo
```

###Set Environment Varialbes (Required Variables Below)

```
DATABASE_ENGINE=django.db.backends.mysql
DATABASE_NAME=zappa_blog
DATABASE_USER=zappa_user
DATABASE_PASSWORD=zappa_password
DATABASE_HOST=zappa-blog.somecrud.us-east-1.rds.amazonaws.com
DATABASE_PORT=3306
SECRET_KEY=yoursecretkey
STATIC_URL=/static/
DEBUG=True
REDIS_HOST=yourhost.com:6379
STATICFILES_LOCATION=your-bucket-prod-static
MEDIAFILES_LOCATION=your-bucket-prod-media
STATIC_VERSION=1.0
AWS_STORAGE_BUCKET_NAME=your-bucket
AWS_S3_CUSTOM_DOMAIN=your-bucket.s3.amazonaws.com
```

###Install Requirements

```pip install -r requirements.txt```

###Zappa Init

Make sure you have the domain setting set in your stage in the zappa_settings.json file. 

```zappa init```


###Zappa Deploy

```zappa deploy dev```

###Migrate DB

```zappa manage migrate```

###Collectstatic

``` zappa manage prod "collectstatic --noinput"```

###Create SSL via API Gateway

Open the AWS Management Console and create a ACM certificate, validate via email 
and then use in the API Gateway console.
  