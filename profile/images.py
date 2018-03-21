from django.conf import settings
import PIL.Image
import uuid
import requests
import os

class AvatarImage:

    def setimage(self, info, **kwargs):

        files = info.context.FILES
        if files is None:
            return None
        if 'avatar' in files:
            tmp_name = os.path.join('temp/', str(uuid.uuid4()))
            img = PIL.Image.open(files['avatar'])
            img = img.resize((300,300))
            img.save(tmp_name, 'JPEG')
            img.close()

        url = "http://127.0.0.1/backend.php"
        files = {'postimage': open(tmp_name, 'rb')}

        response = requests.post(url, files=files)

        os.remove(tmp_name)

        if not response.status_code == requests.codes.ok:
            raise Exception('Server Access Error')

        response = response.json()
        if 'status' in response:
            if response.get('status') == "OK":
                return response.get(url)










