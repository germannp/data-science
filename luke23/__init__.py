"Luke, I am your parser!"
import os


def _read(text_file):
    print('Reading ' + text_file.split('/')[-1])
    with open(text_file, 'r') as txt:
        return txt.read()


module_path = os.path.dirname(__file__)
if module_path == '':
    module_path = '.'

texts = {f.split('.')[0]: _read(os.path.join(module_path, f))
    for f in os.listdir(module_path) if f.endswith('.txt')}
