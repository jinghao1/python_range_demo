# python_range_demo
shoot range of leak
python version: 3.8
Django version: 3.2.2

api-1

method:
    get
url:
    http://127.0.0.1:8000/demo/get_open?name=file/data.json
response:
    {
      "name": "异享金融",
      "telephone": "0371-5505****"
    }


api-2

method:
    post
url:
    http://127.0.0.1:8007/demo/post_open
post_method:
    form-data
body:
    "name": "mysite/settings.py"
response:
    {
        "content": "###code###"
    }