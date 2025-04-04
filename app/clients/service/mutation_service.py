from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.clients.schema import ClientUpdate
from app.models import Client, ClientCase  # Make sure ClientCase is defined in your models

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
            raise HTTPException(
                status_code=500, detail=f"Failed to update client: {str(e)}"
            )

    @staticmethod
    def delete_client(db: Session, client_id: int):
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail=f"Client {client_id} not found")
        try:
            # Delete associated cases using the actual model (ClientCase)
            db.query(ClientCase).filter(ClientCase.client_id == client_id).delete()
            # Delete the client record
            db.delete(client)
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=500, detail=f"Failed to delete client: {str(e)}"
            )
