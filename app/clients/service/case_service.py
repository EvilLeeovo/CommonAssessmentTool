from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import Client, ClientCase, User
from app.clients.schema import ServiceUpdate

class CaseAssignmentService:
    @staticmethod
    def create_case_assignment(db: Session, client_id: int, case_worker_id: int):
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail=f"Client {client_id} not found")
        case_worker = db.query(User).filter(User.id == case_worker_id).first()
        if not case_worker:
            raise HTTPException(status_code=404, detail=f"Case worker {case_worker_id} not found")

        existing = db.query(ClientCase).filter_by(client_id=client_id, user_id=case_worker_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Case already assigned")

        case = ClientCase(
            client_id=client_id,
            user_id=case_worker_id,
            employment_assistance=False,
            life_stabilization=False,
            retention_services=False,
            specialized_services=False,
            employment_related_financial_supports=False,
            employer_financial_supports=False,
            enhanced_referrals=False,
            success_rate=0
        )
        try:
            db.add(case)
            db.commit()
            db.refresh(case)
            return case
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to create case: {str(e)}")

    @staticmethod
    def update_client_services(db: Session, client_id: int, user_id: int, service_update: ServiceUpdate):
        case = db.query(ClientCase).filter_by(client_id=client_id, user_id=user_id).first()
        if not case:
            raise HTTPException(status_code=404, detail="Case not found")
        for field, value in service_update.dict(exclude_unset=True).items():
            setattr(case, field, value)
        try:
            db.commit()
            db.refresh(case)
            return case
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to update case: {str(e)}")
