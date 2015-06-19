from catpics.cloud.auth import CloudApi
from catpics.libs.utils import get_entry

class CloudFilesApi(CloudApi):
    def _load(self):
        endpoints =  get_entry(self.catalog, 'type', 'object-store')['endpoints']
        self.endpoint = get_entry(endpoints, 'region', self.region)['publicURL']
