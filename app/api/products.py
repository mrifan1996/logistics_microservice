from math import ceil

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.product import Product
from app.schemas.product import PaginatedProducts, ProductCreate, ProductResponse

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    product = Product(**payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get("", response_model=PaginatedProducts)
def list_products(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
):
    total_items = db.query(Product).count()
    total_pages = ceil(total_items / page_size)
    offset = (page - 1) * page_size

    products = db.query(Product).offset(offset).limit(page_size).all()

    return PaginatedProducts(
        total_items=total_items,
        total_pages=total_pages,
        current_page=page,
        items=[ProductResponse.model_validate(p) for p in products],
    )
