import os
import sys
import imghdr

from swiftclient.client import put_object

from catpics.cloud.auth import CloudApi
from catpics.libs.utils import get_entry

class CloudFilesApi(CloudApi):
    def _load(self):
        endpoints =  get_entry(self.catalog, 'type', 'object-store')['endpoints']
        self.endpoint = get_entry(endpoints, 'region', self.region)['publicURL']

    def list_containers(self):
        ret = self.session.get(self.endpoint)
        return ret.text.split('\n')

    def container_exists(self, container):
        ret = self.session.get(os.path.join(self.endpoint, container))
        return ret

    def create_container(self, container):
        ret = self.session.put(os.path.join(self.endpoint, container))
        if ret:
            return Container(self, container)
        return False

    def delete_container(self, container):
        ret = self.session.delete(os.path.join(self.endpoint, container))
        if ret:
            return True
        return False

class Container(CloudFilesApi):
    def __init__(self, cloud, container):
        super(Container, self).__init__(cloud)
        self.container = container

    def list_files(self):
        ret = self.session.get(os.path.join(self.endpoint, self.container))
        if ret:
            return ret.text.strip().split('\n')
        return []

    def add_file(self, filename, content):
        #ret = put_object(self.endpoint, self.token, self.container, filename, content, content_type='image/jpeg')
        image = content.read()
        imagetype = imghdr.what(filename, image)
        ret = self.session.put(
            os.path.join(self.endpoint, self.container, filename),
            files={'file': (filename, image)},
            headers={'Content-Type': 'image/{0}'.format(imagetype)},
        )
        return ret
