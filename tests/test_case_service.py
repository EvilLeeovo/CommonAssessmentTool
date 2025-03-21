import pytest
from fastapi import status
from fastapi import HTTPException
from app.models import ClientCase
from app.clients.service.case_service import CaseAssignmentService
from app.clients.schema import ServiceUpdate

def test_create_case_assignment_success(test_db):
    new_case = CaseAssignmentService.create_case_assignment(test_db, client_id=1, case_worker_id=2)
    assert isinstance(new_case, ClientCase)
    assert new_case.client_id == 1
    assert new_case.user_id == 2

def test_create_duplicate_case_assignment(test_db):
    CaseAssignmentService.create_case_assignment(test_db, 1, 2)
    with pytest.raises(HTTPException) as e:
        CaseAssignmentService.create_case_assignment(test_db, 1, 2)
    assert e.value.status_code == 400

def test_update_client_services_success(test_db):
    service_update = ServiceUpdate(employment_assistance=True, success_rate=80)
    updated = CaseAssignmentService.update_client_services(test_db, 1, 1, service_update)
    assert updated.employment_assistance is True
    assert updated.success_rate == 80

def test_update_client_services_not_found(test_db):
    service_update = ServiceUpdate(employment_assistance=True)
    with pytest.raises(HTTPException) as e:
        CaseAssignmentService.update_client_services(test_db, 999, 999, service_update)
    assert e.value.status_code == 404