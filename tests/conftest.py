import pytest
import os
import json
import yaml


@pytest.fixture(scope='module')
def correct_file(request):
    test_dir_name = request.param['testdir']

    if not os.path.isdir(test_dir_name):
        os.mkdir(test_dir_name)

    yf = [
        {'id': 1,
         'label': 'click button',
         'link': 'https://google.ru'
         }
    ]

    #file_name = request.param['filename']
    file_name = 'correct_file_1.yaml'
    with open(os.path.join(test_dir_name, file_name), 'w') as f:
        yaml.dump(yf, f)
    return file_name


@pytest.fixture(scope='module')
def correct_file_without_list(request):
    test_dir_name = request.param['testdir']

    if not os.path.isdir(test_dir_name):
        os.mkdir(test_dir_name)

    yf = {'id': 1,
         'label': 'click button',
         'link': 'https://google.ru'
         }


    #file_name = request.param['filename']
    file_name = 'correct_file_1.yaml'
    with open(os.path.join(test_dir_name, file_name), 'w') as f:
        yaml.dump(yf, f)
    return file_name



@pytest.fixture(scope='module')
def yaml_type_file(request):
    test_dir_name = request.param['testdir']

    if not os.path.isdir(test_dir_name):
        os.mkdir(test_dir_name)

    file_name = request.param['filename']
    file_body = [{'id': 1, 'label': 'test label'}]

    with open(os.path.join(test_dir_name, file_name), 'w') as f:
        yaml.dump(file_body, f)
    yield file_name


@pytest.fixture(scope='module')
def json_file_name(request):
    test_dir_name = request.param['testdir']

    if not os.path.isdir(test_dir_name):
        os.mkdir(test_dir_name)

    json_file_body = {
        'id': 1,
        'label': 'test label'
    }
    #file_name = request.param['filename']
    file_name = 'test_json.json'
    with open(os.path.join(test_dir_name, file_name), 'w') as f:
        json.dump(json_file_body, f)
    return file_name