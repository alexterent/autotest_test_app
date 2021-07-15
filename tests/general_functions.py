import os
import requests as r
from itertools import combinations
import yaml


def short_file_name(fixture_value):
    # TODO: this function lost utility, mb need to write split('.')[0]
    return os.path.basename(fixture_value)


def upload_file(file_name, test_dir_name):
    with open(str(os.path.join(test_dir_name, file_name)), 'rb') as f:
        r.post('http://localhost:5000/api/v1/templates',
               files={'file': (file_name, f)})


def delete_file(file_name):
    r.delete(f'http://localhost:5000/api/v1/templates/{file_name}')


def install_file(file_name):
    r.post(f'http://localhost:5000/api/v1/templates/{file_name}/install')


def combinations_yaml_files(test_dir_name) -> list:
    if not os.path.isdir(test_dir_name):
        os.mkdir(test_dir_name)

    files_name = []

    # if depends is None:
    depends = 'mock_id'

    fields = {'id': 2, 'label': 'btn_label', 'link': 'https://google.ru', 'depends': depends}
    all_comb = ['id', 'label', 'link', 'depends', None, None, None, None]

    count = 0
    for comb in set(combinations(all_comb, 4)):
        file_body = [{key: fields[key] for key in comb if key is not None}]
        files_name.append(f'test_combinations_{count}.yaml')
        with open(os.path.join(test_dir_name, files_name[-1]), 'w') as f:
            yaml.dump(file_body, f)
        count += 1
    return files_name
