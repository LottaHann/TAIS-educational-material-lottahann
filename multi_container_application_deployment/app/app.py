from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import sessionmaker
from typing import List, Optional

# FastAPI app
app = FastAPI()

# Sample product data
products = [
    {"id": 1, "name": "Product 1", "price": 10},
    {"id": 2, "name": "Product 2", "price": 20},
    {"id": 3, "name": "Product 3", "price": 30}
]

# Database connection
SQLALCHEMY_DATABASE_URL = "postgresql://username:password@localhost/mydatabase"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()

# SQLAlchemy models
cart_items = Table(
    "cart_items",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("product_id", Integer),
    Column("product_name", String),
    Column("price", Integer)
)

# Initialize database schema
metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "products": products})

@app.post("/add_to_cart/", response_class=HTMLResponse)
async def add_to_cart(request: Request, product_id: int = Form(...)):
    product = next((p for p in products if p["id"] == product_id), None)
    if product:
        # Save to database
        db = SessionLocal()
        try:
            db.execute(
                cart_items.insert().values(
                    product_id=product["id"],
                    product_name=product["name"],
                    price=product["price"]
                )
            )
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail="Failed to add item to cart")
        finally:
            db.close()
        
        return templates.TemplateResponse(request, "index.html", {"products": products})
    else:
        raise HTTPException(status_code=404, detail="Product not found")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")
