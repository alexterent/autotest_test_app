import requests as r
import pytest
import yaml
import json
import os

from tests.general_functions import combinations_yaml_files, \
    delete_file, short_file_name

test_dir_name = os.path.join(os.path.dirname(__file__), 'test_file_for_upload')


@pytest.fixture(scope='module', params=combinations_yaml_files(test_dir_name), ids=short_file_name)
def file_for_combinations_fields(request):
    yield request.param
    # clear uploads
    r.delete(f'http://localhost:5000/api/v1/templates/{request.param.split(".")[0]}')


def test_upload_combinations_file(file_for_combinations_fields):
    with open(os.path.join(test_dir_name, file_for_combinations_fields), 'rb') as f:
        resp = r.post('http://localhost:5000/api/v1/templates',
                      files={'file': (file_for_combinations_fields, f)})
    assert resp.status_code == 201, resp.text


def test_upload_without_formdata_files():
    resp = r.post('http://localhost:5000/api/v1/templates')
    assert resp.status_code == 400, resp.text


def test_upload_without_field_file():
    resp = r.post('http://localhost:5000/api/v1/templates', files={})
    assert resp.status_code == 400, resp.text


@pytest.mark.parametrize('json_file_name', [{'testdir': test_dir_name}], indirect=True)
def test_upload_json_file(json_file_name):
    with open(os.path.join(test_dir_name, json_file_name), 'rb') as f:
        resp = r.post('http://localhost:5000/api/v1/templates', files={'file': (json_file_name, f)})
    assert resp.status_code == 400, resp.text


@pytest.mark.parametrize('yaml_type_file',
                         [{'testdir': test_dir_name, 'filename': 'test_type_yaml.yaml'},
                          {'testdir': test_dir_name, 'filename': 'test_type_yml.yml'}],
                         indirect=True)
def test_upload_yaml_types_file(yaml_type_file):
    with open(str(os.path.join(test_dir_name, yaml_type_file)), 'rb') as f:
        resp = r.post('http://localhost:5000/api/v1/templates',
                      files={'file': (yaml_type_file, f)})
    delete_file(yaml_type_file.split('.')[0])
    assert resp.status_code == 201, resp.text



@pytest.mark.parametrize('correct_file',
                         [{'testdir': test_dir_name}],
                         indirect=True)
def test_uplpoad_with_empty_file_name(correct_file):
    with open(str(os.path.join(test_dir_name, correct_file)), 'rb') as f:
        resp = r.post('http://localhost:5000/api/v1/templates',
                      files={'file': ("", f)})
    assert resp.status_code == 400, resp.text


@pytest.mark.parametrize('correct_file',
                         [{'testdir': test_dir_name}],
                         indirect=True)
def test_uplpoad_correct_file(correct_file):
    with open(str(os.path.join(test_dir_name, correct_file)), 'rb') as f:
        resp = r.post('http://localhost:5000/api/v1/templates',
                      files={'file': (correct_file, f)})
    delete_file(correct_file.split('.')[0])
    assert resp.status_code == 201, resp.text



@pytest.mark.parametrize('correct_file',
                         [{'testdir': test_dir_name}],
                         indirect=True)
def test_uplpoad_correct_file_with_tmpl_id(correct_file):
    with open(str(os.path.join(test_dir_name, correct_file)), 'rb') as f:
        resp = r.post('http://localhost:5000/api/v1/templates',
                      files={'file': (correct_file, f)}, data={'tmpl_id': "test_custom_id"})
    delete_file(correct_file.split('.')[0])
    assert resp.status_code == 201, resp.text





@pytest.mark.parametrize('correct_file_without_list',
                         [{'testdir': test_dir_name}],
                         indirect=True)
def test_uplpoad_correct_file_not_in_list(correct_file_without_list):
    file_name = correct_file_without_list
    with open(str(os.path.join(test_dir_name, file_name)), 'rb') as f:
        resp = r.post('http://localhost:5000/api/v1/templates',
                      files={'file': (file_name, f)})
    delete_file(file_name.split('.')[0])
    assert resp.status_code == 201, resp.text




@pytest.fixture(scope="module")
def create_file_without_label():
    if not os.path.isdir(test_dir_name):
        os.mkdir(test_dir_name)

    file_name = 'test_file_without_label_1.yaml'

    yf = [{'id': 1,
           'link': 'https://google.ru',
           }
          ]
    with open(os.path.join(test_dir_name, file_name), 'w') as f:
        yaml.dump(yf, f)
    return file_name

@pytest.mark.xfail()
def test_uplpoad_check_error_message_for_file_without_label(create_file_without_label):
    file_name = create_file_without_label
    with open(str(os.path.join(test_dir_name, file_name)), 'rb') as f:
        resp = r.post('http://localhost:5000/api/v1/templates',
                      files={'file': (file_name, f)})

    delete_file(file_name.split('.')[0])

    assert resp.status_code == 400
    assert resp.text != "No label defined for one or more buttons!"
    #TODO: не нашла текст ошибки для label, но суть ошибки
    # в том, что, если исправить label в коде и отправить таком тесте,
    # то код ошибки, что "нет ссылки без названия", хотя ошибка про то, что нет label в шаблоне
