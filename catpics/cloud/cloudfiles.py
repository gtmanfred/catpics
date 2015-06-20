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
        endpoints =  get_entry(self.catalog, 'type', 'rax:object-cdn')['endpoints']
        self.cdnendpoint = get_entry(endpoints, 'region', self.region)['publicURL']

    def list_containers(self):
        ret = self.session.get(self.endpoint)
        return ret.text.split('\n')

    def container_exists(self, container):
        ret = self.session.get(os.path.join(self.endpoint, container))
        return ret

    def create_container(self, container):
        ret = self.session.put(
            os.path.join(self.endpoint, container)
        )
        if ret:
            return Container(self, container)
        return False

    def disable_cdn(self, container):
        ret = self.session.put(
            os.path.join(self.cdnendpoint, container),
            headers={'X-Cdn-Enabled': 'False'}
        )
        if ret:
            return Container(self, container)
        return False

    def enable_cdn(self, container):
        ret = self.session.put(
            os.path.join(self.cdnendpoint, container),
            headers={'X-Cdn-Enabled': 'True'}
        )
        if ret:
            self.links = ret.headers
            return Container(self, container)
        return False

    def get_cdn(self, container):
        ret = self.session.head(
            os.path.join(self.cdnendpoint, container),
        )
        if ret:
            self.links = ret.headers
            return self.links
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
            tmp = ret.text.strip().split('\n')
            if tmp[0]:
                return tmp
        return []

    def add_file(self, filename, content):
        image = content.read()
        imagetype = imghdr.what(filename, image)
        ret = self.session.put(
            os.path.join(self.endpoint, self.container, filename),
            files={'file': (filename, image)},
            headers={'Content-Type': 'image/{0}'.format(imagetype)},
        )
        return ret

    def delete_file(self, filename):
        ret = self.session.delete(
            os.path.join(self.endpoint, self.container, filename),
        )
        return ret

    def create_container(self):
        super(Container, self).create_container(self.container)

    def enable_cdn(self):
        super(Container, self).enable_cdn(self.container)

    def disable_cdn(self):
        super(Container, self).disable_cdn(self.container)

    def get_cdn(self):
        super(Container, self).get_cdn(self.container)
