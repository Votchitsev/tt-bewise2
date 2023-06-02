import os
import aiofiles
from .db import Files


class FileStorage:
    def __init__(self, storage_path):
        self.storage_path = storage_path
        self.tmp_dir = self.storage_path + '/tmp/'

    async def collect_file(self, name, file):
        wav = await self._collect_wav(file, name)
        mp3 = self._create_mp3(name, wav)

        if not mp3:
            return False
        
        model = await Files.objects.create(
            id=name,
            path=mp3,
        )

        return model

    async def _collect_wav(self, file, name):
        path = self.tmp_dir + f"{name}.wav"

        async with aiofiles.open(
            path, 'wb'    
        ) as output:
            content = await file.read()
            await output.write(content)

        return path

    def _create_mp3(self, filename, wav):
        try:
            mp3 = f"{self.storage_path}/{filename}.mp3"

            os.system(f"lame {wav} {mp3}")

            os.remove(wav)

            return mp3
        except:
            return False
