import os
import base64
from glob import glob

class FileInterface:
    def __init__(self):
        self.base_dir = os.path.join(os.getcwd(), 'files')
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    def list(self):
        try:
            return dict(status='OK', data=os.listdir(self.base_dir))
        except Exception as e:
            return dict(status='ERROR', data=str(e))

    def get(self, filename):
        try:
            filepath = os.path.join(self.base_dir, filename)
            with open(filepath, 'rb') as f:
                content = base64.b64encode(f.read()).decode()
            return dict(status='OK', data_namafile=filename, data_file=content)
        except Exception as e:
            return dict(status='ERROR', data=str(e))

    def upload(self, filename, content_base64):
        try:
            filepath = os.path.join(self.base_dir, filename)
            with open(filepath, 'wb') as f:
                f.write(base64.b64decode(content_base64))
            return dict(status='OK', data=f'{filename} berhasil diupload')
        except Exception as e:
            return dict(status='ERROR', data=str(e))

    def delete(self, filename):
        try:
            filepath = os.path.join(self.base_dir, filename)
            if os.path.exists(filepath):
                os.remove(filepath)
                return dict(status='OK', data=f'{filename} berhasil dihapus')
            else:
                return dict(status='ERROR', data=f'{filename} tidak ditemukan')
        except Exception as e:
            return dict(status='ERROR', data=str(e))
