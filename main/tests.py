from rest_framework import status
from rest_framework.test import APITestCase
import json

class PerevalAddTests(APITestCase):
    def test_perevaladd(self):
        url = 'http://127.0.0.1:8000/submitData/'
        for i in range(10):
            data = {
       "beauty_title":f"test{i}",
       "title":f"test{i}",
       "other_titles":f"test{i}",
       "connect":f"test{i}",
       "add_time":"2021-09-22 13:18:13",

       "user":{
          "email":f"test{i}@mail.ru",
          "fam":f"test{i}",
          "name":f"test{i}",
          "otc":f"test{i}",
          "phone":f"test{i}"
       },

       "coords":{
          "latitude":f"{i}",
          "longitude":f"{i}",
          "height":f"{i}"
       },

       "level":{
          "winter":f"test{i}",
          "summer":f"test{i}",
          "autumn":f"test{i}",
          "spring":f"test{i}"
       },

       "images":[
          {
             "data":f"test{i}",
             "title":f"test{i}"
          },
          {
             "data":f"test{i}",
             "title":f"test{i}"
          }
       ]
    }
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        for i in range(11)[1:]:
            url = f'http://127.0.0.1:8000/submitData/{i}/'
            request = self.client.get(url)
            print(f'{url} {json.loads(request.content)["id"]}')
            self.assertEqual(json.loads(request.content)["id"], i)

