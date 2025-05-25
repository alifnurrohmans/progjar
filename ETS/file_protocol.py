import json
import shlex
from file_interface import FileInterface

class FileProtocol:
    def __init__(self):
        self.file = FileInterface()

    def proses_string(self, string_datamasuk=''):
        try:
            c = shlex.split(string_datamasuk)
            if not c:
                return json.dumps(dict(status='ERROR', data='Perintah kosong'))
            command = c[0].upper()
            args = c[1:]

            if command == 'LIST':
                return json.dumps(self.file.list())
            elif command == 'GET' and len(args) == 1:
                return json.dumps(self.file.get(args[0]))
            elif command == 'UPLOAD' and len(args) == 2:
                return json.dumps(self.file.upload(args[0], args[1]))
            elif command == 'DELETE' and len(args) == 1:
                return json.dumps(self.file.delete(args[0]))
            else:
                return json.dumps(dict(status='ERROR', data='Perintah tidak dikenali atau argumen tidak lengkap'))
        except Exception as e:
            return json.dumps(dict(status='ERROR', data=str(e)))
