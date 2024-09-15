import pytest
from unittest.mock import Mock, MagicMock

import requests
from Workers.FinanceWorker import FinanceWorker


@pytest.fixture()
def finance_worker_instance_mmm(mocker):
    finance_worker_instance = FinanceWorker('mmm')
    with open('TestMMMYahooHTML.txt', 'r', encoding='utf-8') as file:
        test_html = file.read()
    mock_response = MagicMock(spec=requests, autospec=True)
    mock_response.status_code = 200
    mock_response.text = test_html
    mock_get = Mock(return_value=mock_response)
    mocker.patch('requests.get', mock_get)
    return finance_worker_instance


@pytest.fixture()
def finance_worker_instance_aos(mocker):
    finance_worker_instance = FinanceWorker('aos')
    with open('TestAOSYahooHTML.txt', 'r', encoding='utf-8') as file:
        test_html = file.read()
    mock_response = MagicMock(spec=requests, autospec=True)
    mock_response.status_code = 200
    mock_response.text = test_html
    mock_get = Mock(return_value=mock_response)
    mocker.patch('requests.get', mock_get)
    return finance_worker_instance


def test_real_connection_respond():
    finance_worker_instance = FinanceWorker('aos')
    response = requests.get(finance_worker_instance.url)
    assert response.status_code == 200


# Good
def test_extract_price_mmm(finance_worker_instance_mmm):
    assert finance_worker_instance_mmm.extract_price() == 131.4


def test_extract_price_aos(finance_worker_instance_aos):
    assert finance_worker_instance_aos.extract_price() == 83.72
