from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table, Numeric
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy.orm.exc import NoResultFound
from typing import List, Optional
from fastapi.responses import RedirectResponse


# FastAPI app
app = FastAPI()

# Sample product data

#products = [
#    {"id": 1, "name": "Product 1", "price": 10},
#    {"id": 2, "name": "Product 2", "price": 20},
#    {"id": 3, "name": "Product 3", "price": 30}
#]

# Database connection
SQLALCHEMY_DATABASE_URL =  "postgresql://lotta:Jk9!Zt13#Qp@db:5432/postgres"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()
Base = declarative_base()

# SQLAlchemy models
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))  # Matching the VARCHAR(255) in the database
    price = Column(Numeric(10, 2))  # Matching the numeric(10,2) in the database


class CartItem(Base):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer)
    product_name = Column(String(255))
    price = Column(Numeric(10, 2))

# Initialize database schema
metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    db: Session = SessionLocal()
    try:
        products = db.query(Product).all()
    finally:
        db.close()
    return templates.TemplateResponse("index.html", {"request": request, "products": products})


@app.post("/add_to_cart/", response_class=HTMLResponse)
async def add_to_cart(request: Request, product_id: int = Form(...)):
    db: Session = SessionLocal()
    try:
        product = db.query(Product).filter(Product.id == product_id).one_or_none()
        if product:
            db.add(CartItem(
                product_id=product.id,
                product_name=product.name,
                price=product.price
            ))
            db.commit()
        else:
            raise HTTPException(status_code=404, detail="Product not found")
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Product not found")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to add item to cart: {e}")
    finally:
        db.close()

    return templates.TemplateResponse("index.html", {"request": request, "products": db.query(Product).all()})

@app.get("/cart", response_class=HTMLResponse)
async def view_cart(request: Request):
    print("Viewing cart items")
    return RedirectResponse(url="http://localhost:8082/", status_code=302)

@app.get("/back_to_product_list", response_class=HTMLResponse)
async def back_to_product_list(request: Request):
    print("Redirecting to product list)")
    return RedirectResponse(url="http://localhost:8081/", status_code=302)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081, log_level="info")
