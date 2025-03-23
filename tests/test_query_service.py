import pytest
from fastapi import HTTPException, status

from app.clients.service.query_service import ClientQueryService


def test_get_client_success(test_db):
    client = ClientQueryService.get_client(test_db, 1)
    assert client.id == 1
    assert client.age > 0


def test_get_client_not_found(test_db):
    with pytest.raises(HTTPException) as e:
        ClientQueryService.get_client(test_db, 999)
    assert e.value.status_code == 404


def test_get_clients_success(test_db):
    result = ClientQueryService.get_clients(test_db, skip=0, limit=10)
    assert "clients" in result
    assert "total" in result
    assert isinstance(result["clients"], list)


def test_get_clients_invalid_pagination(test_db):
    with pytest.raises(HTTPException):
        ClientQueryService.get_clients(test_db, skip=-1, limit=10)


def test_get_clients_by_case_worker_success(test_db):
    clients = ClientQueryService.get_clients_by_case_worker(test_db, 2)
    assert isinstance(clients, list)


def test_get_clients_by_case_worker_not_found(test_db):
    with pytest.raises(HTTPException) as e:
        ClientQueryService.get_clients_by_case_worker(test_db, 999)
    assert e.value.status_code == 404


def test_get_clients_by_success_rate(test_db):
    result = ClientQueryService.get_clients_by_success_rate(test_db, min_rate=70)
    assert isinstance(result, list)


def test_get_clients_by_success_rate_invalid(test_db):
    with pytest.raises(HTTPException) as e:
        ClientQueryService.get_clients_by_success_rate(test_db, min_rate=150)
    assert e.value.status_code == 400
