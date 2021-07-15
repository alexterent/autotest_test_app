import requests as r
import pytest
import yaml
import os
from tests.general_functions import upload_file, install_file

test_dir_name = os.path.join(os.path.dirname(__file__), 'test_file_for_delete')


@pytest.mark.parametrize('correct_file',
                         [{'testdir': test_dir_name}],
                         indirect=True)
def test_delete_upload_file(correct_file):
    file_name = correct_file
    upload_file(file_name, test_dir_name)
    resp = r.delete(f'http://localhost:5000/api/v1/templates/{file_name.split(".")[0]}')
    assert resp.status_code == 200, resp.text


def test_delete_not_existing_file():
    not_exist_file_name = 'not_exist_file'
    resp = r.delete(f'http://localhost:5000/api/v1/templates/{not_exist_file_name}')
    assert resp.status_code == 404, resp.text


def test_delete_without_id():
    resp = r.delete(f'http://localhost:5000/api/v1/templates/')
    assert resp.status_code == 404, resp.text


@pytest.mark.parametrize('correct_file',
                         [{'testdir': test_dir_name}],
                         indirect=True)
def test_delete_upload_and_install_file(correct_file):
    file_name = correct_file
    upload_file(file_name, test_dir_name)
    install_file(file_name.split('.')[0])
    resp = r.delete(f'http://localhost:5000/api/v1/templates/{file_name.split(".")[0]}')
    assert resp.status_code == 200, resp.text