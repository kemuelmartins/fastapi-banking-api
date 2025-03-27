from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import Account, Transaction

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("/{account_id}")
async def create_transaction(account_id: int, transaction_type: str, amount: float, db: AsyncSession = Depends(get_db)):
    account = await db.get(Account, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Conta não encontrada")

    if transaction_type == "withdrawal" and account.balance < amount:
        raise HTTPException(status_code=400, detail="Saldo insuficiente")

    new_transaction = Transaction(account_id=account_id, type=transaction_type, amount=amount)
    db.add(new_transaction)

    if transaction_type == "deposit":
        account.balance += amount
    elif transaction_type == "withdrawal":
        account.balance -= amount

    await db.commit()
    await db.refresh(account)

    return {"message": "Transação realizada com sucesso!"}
