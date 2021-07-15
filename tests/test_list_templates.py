import requests as r
import pytest
import yaml
import os
from tests.general_functions import upload_file, delete_file, install_file

test_dir_name = os.path.join(os.path.dirname(__file__), 'test_file_for_list')


@pytest.mark.parametrize('json_file_name', [{'testdir': test_dir_name}], indirect=True)
def test_list_without_json(json_file_name):
    with open(os.path.join(test_dir_name, json_file_name), 'rb') as f:
        resp = r.post('http://localhost:5000/api/v1/templates',
                      files={'file': (json_file_name, f)})
    resp = r.get('http://localhost:5000/api/v1/templates')
    assert len(resp.json()['templates']) == 0, resp.text


@pytest.mark.parametrize('yaml_type_file',
                         [{'testdir': test_dir_name, 'filename': 'test_type_yaml.yaml'},
                          {'testdir': test_dir_name, 'filename': 'test_type_yml.yml'}],
                         indirect=True)
def test_list_yaml_types_file(yaml_type_file):
    file_name = yaml_type_file
    upload_file(file_name, test_dir_name)
    resp = r.get('http://localhost:5000/api/v1/templates')
    assert len(resp.json()['templates']) == 1, 'Incorrect count yaml files'
    assert resp.json()['templates'][0] == file_name.split('.')[0], 'Incorrect name of upload file'
    delete_file(file_name.split('.')[0])


@pytest.mark.parametrize('correct_file',
                         [{'testdir': test_dir_name}],
                         indirect=True)
def test_list_after_upload_and_delete_file(correct_file):
    file_name = correct_file
    upload_file(file_name, test_dir_name)
    resp = r.get('http://localhost:5000/api/v1/templates')
    assert len(resp.json()['templates']) == 1, 'Incorrect count yaml files after upload file'
    assert resp.json()['templates'][0] == file_name.split('.')[0], 'Incorrect name of upload file'
    delete_file(file_name.split('.')[0])
    resp = r.get('http://localhost:5000/api/v1/templates')
    assert len(resp.json()['templates']) == 0, 'Incorrect count yaml files after delete file'


@pytest.mark.parametrize('correct_file',
                         [{'testdir': test_dir_name}],
                         indirect=True)
def test_list_after_upload_and_install_and_delete_file(correct_file):
    file_name = correct_file
    short_file_name_val = file_name.split('.')[0]
    upload_file(file_name, test_dir_name)
    resp = r.get('http://localhost:5000/api/v1/templates')
    assert len(resp.json()['templates']) == 1, 'Incorrect count yaml files after upload file'
    assert resp.json()['templates'][0] == short_file_name_val, 'Incorrect name of upload file'
    install_file(short_file_name_val)
    delete_file(short_file_name_val)
    resp = r.get('http://localhost:5000/api/v1/templates')
    assert len(resp.json()['templates']) == 0, 'Incorrect count yaml files after delete file'


@pytest.mark.parametrize('correct_file',
                         [{'testdir': test_dir_name}],
                         indirect=True)
def test_list_not_change_after_delete_not_existing_file(correct_file):
    not_exist_file_name = 'not_exist_file'
    file_name = correct_file
    short_file_name_val = file_name.split('.')[0]
    upload_file(file_name, test_dir_name)
    resp = r.get('http://localhost:5000/api/v1/templates')
    assert len(resp.json()['templates']) == 1, 'Incorrect count yaml files after upload file'
    assert resp.json()['templates'][0] == short_file_name_val, 'Incorrect name of upload file'

    delete_file(not_exist_file_name)
    resp = r.get('http://localhost:5000/api/v1/templates')
    assert len(resp.json()['templates']) == 1, 'Incorrect count yaml files after delete not exist file'
    assert resp.json()['templates'][0] == short_file_name_val, 'Incorrect name of upload file after delete not exist file'
    delete_file(short_file_name_val)


@pytest.mark.parametrize('correct_file',
                         [{'testdir': test_dir_name}],
                         indirect=True)
def test_list_file_with_custom_id_in_list(correct_file):
    with open(str(os.path.join(test_dir_name, correct_file)), 'rb') as f:
        r.post('http://localhost:5000/api/v1/templates',
               files={'file': (correct_file, f)}, data={'tmpl_id': "test_custom_id"})
    resp = r.get('http://localhost:5000/api/v1/templates')
    assert len(resp.json()['templates']) == 1, 'Incorrect count yaml files'
    assert resp.json()['templates'][0] == "test_custom_id", 'Incorrect name of upload file with custom id'
    delete_file("test_custom_id")