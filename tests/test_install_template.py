import requests as r
import pytest
import yaml
import os

from tests.general_functions import combinations_yaml_files, \
    upload_file, delete_file, short_file_name

test_dir_name = os.path.join(os.path.dirname(__file__), 'test_file_for_install')


@pytest.mark.parametrize('correct_file',
                         [{'testdir': test_dir_name}],
                         indirect=True)
def test_install_correct_file_without_depends(correct_file):
    file_name = correct_file
    short_file_name_val = file_name.split('.')[0]
    upload_file(file_name, test_dir_name)
    resp = r.post(f'http://localhost:5000/api/v1/templates/{short_file_name_val}/install')
    delete_file(short_file_name_val)
    assert resp.status_code == 200, resp.text



@pytest.fixture()
def correct_file_with_depends():
    if not os.path.isdir(test_dir_name):
        os.mkdir(test_dir_name)

    file_name = 'correct_file_with_depends_1.yaml'

    yf = [{'id': 1,
            'label': 'click button 1',
            'link': 'https://google.ru',
            },
            {'id': 2,
             'label': 'click button 2',
             'link': 'https://yandex.ru',
             'depends': 1
             }
    ]

    with open(os.path.join(test_dir_name, file_name), 'w') as f:
        yaml.dump(yf, f)
    upload_file(file_name, test_dir_name)
    yield file_name
    delete_file(file_name.split('.')[0])


def test_install_correct_file_with_depends(correct_file_with_depends):
    file_name = correct_file_with_depends
    resp = r.post(f'http://localhost:5000/api/v1/templates/{file_name.split(".")[0]}/install')
    assert resp.status_code == 200, resp.text

# @pytest.fixture(scope='module', params=combinations_yaml_files(test_dir_name), ids=short_file_name)
# def file_for_combinations_fields(request):
#     with open(str(request.param), 'rb') as f:
#         r.post('http://localhost:5000/api/v1/templates',
#                files={'file': (str(os.path.basename(request.param)), f)})
#     yield request.param
#     r.delete(f'http://localhost:5000/api/v1/templates/{request.param.split(".")[0]}')


@pytest.fixture(scope='module', params=combinations_yaml_files(test_dir_name), ids=short_file_name)
def file_for_combinations_fields_with_result_without_depends(request):
    result = 200
    with open(os.path.join(test_dir_name, request.param)) as f:
        yaml_file = yaml.safe_load(f)
        for content in yaml_file:  # yaml_file can be like [{}] or [{}, {} ...]
            if 'id' not in content or 'label' not in content:
                result = 400
                break
            elif 'depends' in content:
                result = 400
                break
    with open(os.path.join(test_dir_name, request.param), 'rb') as f:
        r.post('http://localhost:5000/api/v1/templates',
               files={'file': (request.param, f)})
    yield (request.param, result)
    r.delete(f'http://localhost:5000/api/v1/templates/{request.param.split(".")[0]}')


def test_install_combinations_file_for_mandatory_fields_with_incorrect_depends(file_for_combinations_fields_with_result_without_depends):
    file_name = file_for_combinations_fields_with_result_without_depends[0]
    expected_result = file_for_combinations_fields_with_result_without_depends[1]
    resp = r.post(f'http://localhost:5000/api/v1/templates/{file_name.split(".")[0]}/install')
    assert resp.status_code == expected_result, resp.text


@pytest.mark.parametrize('correct_file_without_list',
                         [{'testdir': test_dir_name}],
                         indirect=True)
def test_install_correct_file_not_in_list(correct_file_without_list):
    file_name = correct_file_without_list
    upload_file(file_name, test_dir_name)
    resp = r.post(f'http://localhost:5000/api/v1/templates/{file_name.split(".")[0]}/install')
    delete_file(file_name.split('.')[0])
    assert resp.status_code == 400, resp.text


@pytest.fixture()
def file_with_not_unique_id():
    if not os.path.isdir(test_dir_name):
        os.mkdir(test_dir_name)

    file_name = 'file_with_not_unique_id_1.yaml'

    yf = [{'id': 1,
           'label': 'click button 1',
           'link': 'https://google.ru',
           },
          {'id': 1,
           'label': 'click button 2',
           'link': 'https://yandex.ru',
           },
          {'id': 1,
           'label': 'click button 3',
           }
          ]

    with open(os.path.join(test_dir_name, file_name), 'w') as f:
        yaml.dump(yf, f)
    upload_file(file_name, test_dir_name)
    yield file_name
    delete_file(file_name.split('.')[0])


def test_install_file_with_not_unique_id(file_with_not_unique_id):
    file_name = file_with_not_unique_id
    resp = r.post(f'http://localhost:5000/api/v1/templates/{file_name.split(".")[0]}/install')
    assert resp.status_code == 400, 'Template have not unique id'


@pytest.fixture()
def file_with_equal_id_and_depends():
    if not os.path.isdir(test_dir_name):
        os.mkdir(test_dir_name)

    file_name = 'file_with_depends_like_id_1.yaml'

    yf = [
          {'id': 1,
           'label': 'click button 2',
           'link': 'https://yandex.ru',
           'depends': 1
           }
          ]

    with open(os.path.join(test_dir_name, file_name), 'w') as f:
        yaml.dump(yf, f)
    upload_file(file_name, test_dir_name)
    yield file_name
    delete_file(file_name.split('.')[0])

def test_install_file_with_equal_id_and_depends(file_with_equal_id_and_depends):
    file_name = file_with_equal_id_and_depends
    resp = r.post(f'http://localhost:5000/api/v1/templates/{file_name.split(".")[0]}/install')
    assert resp.status_code == 400, 'Template have equal id and depends id'