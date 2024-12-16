import asyncio
import os
import requests
import hashlib
import aiohttp
from staticInfo import StaticInfo

class clientDownloader:
    def __init__(self):
        self.url = StaticInfo.versionManifestUrl

    async def downloadClient(url, sha1, version):
        if not os.path.exists('client'):
            os.mkdir('client')
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    return False
                if not os.path.exists(os.path.join('client',version)):
                    os.mkdir(os.path.join('client',version))
                with open(os.path.join('client',f'{version}',f'client_{version}.jar'), 'wb') as f:
                    hasher = hashlib.sha1()
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            break
                        f.write(chunk)
                        hasher.update(chunk)
                    
                downloaded_sha1 = hasher.hexdigest()
                if downloaded_sha1 != sha1:
                    os.remove('/client/client_{version}.jar')  
                    return False

                return True
                        
    def solveClient(self):
        versionManifestJson = requests.get(self.url).json()
        for version in versionManifestJson['versions']:
            versionJson = requests.get(version['url']).json()
            downloadUrl = versionJson['downloads']['client']['url']
            sha1 = versionJson['downloads']['client']['sha1']
            asyncio.run(self.downloadClient(downloadUrl, sha1))
    
                        

