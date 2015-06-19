from catpics.cloud.auth import CloudApi

class CloudFilesApi(CloudApi):
    def _load(self):
        endpoints =  get_entry(self.catalog, 'type', 'object-store')['endpoints']
        self.endpoint = get_entry(endpoints, 'region', self.region)['publicURL']
