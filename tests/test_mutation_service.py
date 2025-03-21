import pytest
from fastapi import status
from fastapi import HTTPException
from app.clients.service.mutation_service import ClientMutationService
from app.clients.schema import ClientUpdate

def test_update_client_success(test_db):
    update = ClientUpdate(age=40, currently_employed=True)
    updated = ClientMutationService.update_client(test_db, 1, update)
    assert updated.age == 40
    assert updated.currently_employed is True

def test_update_client_not_found(test_db):
    update = ClientUpdate(age=30)
    with pytest.raises(HTTPException) as e:
        ClientMutationService.update_client(test_db, 999, update)
    assert e.value.status_code == 404

def test_delete_client_success(test_db):
    ClientMutationService.delete_client(test_db, 2)
    with pytest.raises(HTTPException):
        ClientMutationService.delete_client(test_db, 2)

def test_delete_client_not_found(test_db):
    with pytest.raises(HTTPException) as e:
        ClientMutationService.delete_client(test_db, 999)
    assert e.value.status_code == 404