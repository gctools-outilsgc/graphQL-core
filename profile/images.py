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

        tmp_name = os.path.join('temp/', str(uuid.uuid4()))
        post = False

        if 'avatar' in files:

            img = PIL.Image.open(files['avatar'])
            img = img.resize((300,300))
            img.save(tmp_name, 'JPEG')
            img.close()
            post = True

        if post:
            files = {'postimage': open(tmp_name + '.jpg', 'rb')}

            response = requests.post('http://image/backend.php', files=files)

            os.remove(tmp_name)

            if not response.status_code == requests.codes.ok:
                raise Exception('Server Access Error / ' + response.status_code)

            response = response.json()
            if 'status' in response:
                if response.get('status') == "OK":
                    return response.get('url')

        return None










