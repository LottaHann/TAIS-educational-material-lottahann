from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.orm import sessionmaker
from typing import List
from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from fastapi import HTTPException
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse



# FastAPI app
app = FastAPI()

# Database connection
SQLALCHEMY_DATABASE_URL = "postgresql://lotta:Jk9!Zt13#Qp@db:5432/postgres"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()
Base = declarative_base()

# SQLAlchemy models
class CartItem(Base):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer)
    product_name = Column(String(255))
    price = Column(Numeric(10, 2))


templates = Jinja2Templates(directory="templates")
cart_items = None

@app.get("/", response_class=HTMLResponse)
async def view_cart(request: Request):
    db: Session = SessionLocal()
    try:
        cart_items = db.query(CartItem).all()
        print(cart_items)
        total = sum(item.price for item in cart_items)
        print(total)
        return templates.TemplateResponse("cart.html", {"request": request, "cart_items": cart_items, "total": total})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching cart items: {e}")
    finally:
        db.close()

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

@app.get("/back_to_product_list", response_class=HTMLResponse)
async def back_to_product_list(request: Request):
    print("Redirecting to product list")
    return RedirectResponse(url="http://localhost:8081/", status_code=302)



if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8082, log_level="info")
