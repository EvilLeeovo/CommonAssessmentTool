from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Client, ClientCase  # Import ClientCase which represents the cases table

class ClientQueryService:
    @staticmethod
    def get_client(db: Session, client_id: int):
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail=f"Client {client_id} not found")
        return client

    @staticmethod
    def get_clients(db: Session, skip: int = 0, limit: int = 50):
        if skip < 0 or limit < 1:
            raise HTTPException(status_code=400, detail="Invalid pagination")
        total = db.query(Client).count()
        clients = db.query(Client).offset(skip).limit(limit).all()
        return {"clients": clients, "total": total}

    @staticmethod
    def get_clients_by_case_worker(db: Session, case_worker_id: int):
        # unchanged from your current implementation
        case_worker = db.query(Client).filter(Client.id == case_worker_id).first()
        if not case_worker:
            raise HTTPException(
                status_code=404, detail=f"Case worker {case_worker_id} not found"
            )
        return (
            db.query(Client)
            .join(Client.cases)
            .filter_by(user_id=case_worker_id)
            .all()
        )

    @staticmethod
    def get_clients_by_success_rate(db: Session, min_rate: int = 70):
        if not (0 <= min_rate <= 100):
            raise HTTPException(
                status_code=400, detail="Success rate must be between 0 and 100"
            )
        # Updated query:
        # Join the ClientCase table via the relationship Client.cases,
        # then filter on ClientCase.success_rate instead of Client.cases.success_rate.
        return (
            db.query(Client)
            .join(ClientCase, Client.cases)
            .filter(ClientCase.success_rate >= min_rate)
            .all()
        )
