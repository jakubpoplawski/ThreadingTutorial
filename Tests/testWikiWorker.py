import pytest
from unittest.mock import Mock, MagicMock, patch

import requests
from Workers.WikiWorker import WikiWorker


@pytest.fixture()
def wiki_worker_instance():
    wiki_worker_instance = WikiWorker()
    return wiki_worker_instance


def test_real_connection_respond(wiki_worker_instance):
    response = requests.get(wiki_worker_instance.url)
    assert response.status_code == 200


# Good
def test_get_companies_good_retrival_scenario(wiki_worker_instance, mocker):
    test_data = [(1, 'MMM'), (2, 'AOS'), (3, 'ABT')]
    mock_response = MagicMock(spec=requests, autospec=True)
    mock_response.status_code = 200
    mock_response.text = 'blah'
    mock_get = Mock(return_value=mock_response)
    mocker.patch('requests.get', mock_get)
    with patch.object(wiki_worker_instance, 'extract_companies',
                      return_value=iter(test_data)) as mock_method:
        result = len(list(wiki_worker_instance.get_companies()))
        mock_method.assert_called_once()
    assert result == 3


# Interesting
def test_real_connection_result_magicmock_full_data_mock(
        wiki_worker_instance, mocker):
    with open('TestWikiHTML.txt', 'r', encoding='utf-8') as file:
        test_html = file.read()
    mock_response = MagicMock(spec=requests, autospec=True)
    mock_response.status_code = 200
    mock_response.text = test_html
    mock_get = Mock(return_value=mock_response)
    mocker.patch('requests.get', mock_get)
    result = len(list(wiki_worker_instance.get_companies()))
    assert result == 503


def test_real_connection_result_conf_iter(wiki_worker_instance, mocker):
    test_data = [(1, 'MMM'), (2, 'AOS'), (3, 'ABT')]
    test_extract = MagicMock()
    test_extract.iter.return_value = iter(test_data)
    mock_response = Mock(spec=requests, autospec=True)
    mock_response.status_code = 200
    mock_get = Mock(return_value=mock_response)
    mocker.patch('requests.get', mock_get)
    result = len(list(wiki_worker_instance.get_companies()))
    mock_response.status_code.assert_called_once_with(200)
    assert result != 0


# Good
def test_get_companies_bad_retrival_scenario(wiki_worker_instance, mocker):
    mock_response = Mock(spec=requests, autospec=True)
    mock_response.status_code = 500
    mock_get = Mock(return_value=mock_response)
    mocker.patch('requests.get', mock_get)
    result = wiki_worker_instance.get_companies()
    assert result == []


# Good
def test_extract_companies(wiki_worker_instance):
    with open('TestWikiHTML.txt', 'r', encoding='utf-8') as file:
        test_html = file.read()
    assert len(list(wiki_worker_instance.extract_companies(test_html))) == 503


def test_extract_companies_cut_html(wiki_worker_instance):
    with open('TestHTML501Companies.txt', 'r', encoding='utf-8') as file:
        test_html = file.read()
    assert len(list(wiki_worker_instance.extract_companies(test_html))) == 501
