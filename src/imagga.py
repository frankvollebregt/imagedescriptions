import requests

api_key = 'acc_68324598082a188'
api_secret = 'bb9180ada44fdfff3bf054ded4644003'
image_path = 'images/bikes.jpg'

response = requests.post(
    'https://api.imagga.com/v2/tags',
    auth=(api_key, api_secret),
    files={'image': open(image_path, 'rb')})
res = response.json()

for tag in res['result']['tags']:
    print('{}% {}'.format(round(tag['confidence']), tag['tag']['en']))

# import requests
#
# api_key = 'acc_68324598082a188'
# api_secret = 'bb9180ada44fdfff3bf054ded4644003'
# image_url = 'https://docs.imagga.com/static/images/docs/sample/japan-605234_1280.jpg'
#
# response = requests.get(
#     'https://api.imagga.com/v2/tags?image_url=%s' % image_url,
#     auth=(api_key, api_secret))
#
# print(response.json())