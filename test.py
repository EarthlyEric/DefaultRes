import asyncio
import aiohttp
import hashlib
import os

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
                print(f"SHA1 驗證失敗: {downloaded_sha1} != {sha1}")
                os.remove('/client/client_{version}.jar')  
                return False

            return True


url = 'https://piston-data.mojang.com/v1/objects/a7e5a6024bfd3cd614625aa05629adf760020304/client.jar'
sha1 = 'a7e5a6024bfd3cd614625aa05629adf760020304'
version = '1.21.3'

asyncio.run(downloadClient(url, sha1, version))
