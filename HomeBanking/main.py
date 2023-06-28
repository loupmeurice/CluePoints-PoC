from fastapi import FastAPI

from routers import user, account, transaction

app = FastAPI()
app.include_router(user.router)
app.include_router(account.router)
app.include_router(transaction.router)

