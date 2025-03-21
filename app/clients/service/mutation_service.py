from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import Client
from app.clients.schema import ClientUpdate

class ClientMutationService:
    @staticmethod
    def update_client(db: Session, client_id: int, client_update: ClientUpdate):
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail=f"Client {client_id} not found")
        update_data = client_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(client, field, value)
        try:
            db.commit()
            db.refresh(client)
            return client
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to update client: {str(e)}")

    @staticmethod
    def delete_client(db: Session, client_id: int):
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail=f"Client {client_id} not found")
        try:
            db.query(Client.cases).filter_by(client_id=client_id).delete()
            db.delete(client)
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to delete client: {str(e)}")
