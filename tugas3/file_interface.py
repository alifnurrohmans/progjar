import os
import json
import base64
from glob import glob


class FileInterface:
    def __init__(self):
        if not os.path.exists('files'):
            os.makedirs('files')
        os.chdir('files/')

    def list(self, params=[]):
        try:
            filelist = glob('*.*')
            return dict(status='OK', data=filelist)
        except Exception as e:
            return dict(status='ERROR', data=str(e))

    def get(self, params=[]):
        try:
            filename = params[0]
            if filename == '':
                return None
            with open(filename, 'rb') as fp:
                isifile = base64.b64encode(fp.read()).decode()
            return dict(status='OK', data_namafile=filename, data_file=isifile)
        except Exception as e:
            return dict(status='ERROR', data=str(e))

    def upload(self, params=[]):
        try:
            filename = params[0]
            content_base64 = params[1]
            content_bytes = base64.b64decode(content_base64)
            with open(filename, 'wb') as f:
                f.write(content_bytes)
            return dict(status='OK', data=f'{filename} berhasil diupload')
        except Exception as e:
            return dict(status='ERROR', data=str(e))

    def delete(self, params=[]):
        try:
            filename = params[0]
            if os.path.exists(filename):
                os.remove(filename)
                return dict(status='OK', data=f'{filename} berhasil dihapus')
            else:
                return dict(status='ERROR', data=f'{filename} tidak ditemukan')
        except Exception as e:
            return dict(status='ERROR', data=str(e))


if __name__ == '__main__':
    f = FileInterface()
    print(f.list())
    print(f.get(['contoh.jpg']))
    # Test upload & delete
    # print(f.upload(['baru.txt', base64.b64encode(b"ini isi file baru").decode()]))
    # print(f.delete(['baru.txt']))
