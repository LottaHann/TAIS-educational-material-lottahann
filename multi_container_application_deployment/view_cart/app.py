from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.orm import sessionmaker
from typing import List

# FastAPI app
app = FastAPI()

# Database connection
SQLALCHEMY_DATABASE_URL = "postgresql://username:password@localhost/mydatabase"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()

# SQLAlchemy models
cart_items = Table(
    "cart_items",
    metadata,
    autoload=True,
    autoload_with=engine
)

templates = Jinja2Templates(directory="templates")

@app.get("/cart", response_class=HTMLResponse)
async def view_cart(request: Request):
    db = SessionLocal()
    try:
        stmt = select([cart_items])
        results = db.execute(stmt).fetchall()
        cart = [
            {"product_id": row.product_id, "product_name": row.product_name, "price": row.price}
            for row in results
        ]
        total = sum(item['price'] for item in cart)
        return templates.TemplateResponse("cart.html", {"request": request, "cart": cart, "total": total})
    finally:
        db.close()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081, log_level="info")
