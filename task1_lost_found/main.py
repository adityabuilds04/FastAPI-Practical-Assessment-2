
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select

from database import create_db_and_tables, get_session
from models import Item, ItemStatus
from schemas import ItemCreate, ItemUpdate


app = FastAPI(
    title="Campus Lost & Found API",
    description="API for managing lost and found campus items",
    version="1.0.0"
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# --------------------------------------------------
# CREATE ITEM
# --------------------------------------------------

@app.post("/items", response_model=Item, status_code=201)
def create_item(
    item_data: ItemCreate,
    session: Session = Depends(get_session)
):
    item = Item(**item_data.model_dump())

    session.add(item)
    session.commit()
    session.refresh(item)

    return item


# --------------------------------------------------
# GET ALL ITEMS
# --------------------------------------------------

@app.get("/items", response_model=list[Item])
def get_items(
    session: Session = Depends(get_session)
):
    items = session.exec(select(Item)).all()
    return items


# --------------------------------------------------
# GET ITEMS BY STATUS
# --------------------------------------------------

@app.get("/items/status/{status}", response_model=list[Item])
def get_items_by_status(
    status: ItemStatus,
    session: Session = Depends(get_session)
):
    statement = select(Item).where(Item.status == status)
    items = session.exec(statement).all()

    return items


# --------------------------------------------------
# GET ITEMS BY CATEGORY
# --------------------------------------------------

@app.get("/items/category/{category}", response_model=list[Item])
def get_items_by_category(
    category: str,
    session: Session = Depends(get_session)
):
    statement = select(Item).where(Item.category == category)
    items = session.exec(statement).all()

    return items


# --------------------------------------------------
# GET ITEM BY ID
# --------------------------------------------------

@app.get("/items/{item_id}", response_model=Item)
def get_item(
    item_id: int,
    session: Session = Depends(get_session)
):
    item = session.get(Item, item_id)

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    return item


# --------------------------------------------------
# UPDATE ITEM
# --------------------------------------------------

@app.put("/items/{item_id}", response_model=Item)
def update_item(
    item_id: int,
    item_data: ItemUpdate,
    session: Session = Depends(get_session)
):
    item = session.get(Item, item_id)

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    update_data = item_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(item, key, value)

    session.add(item)
    session.commit()
    session.refresh(item)

    return item


# --------------------------------------------------
# DELETE ITEM
# --------------------------------------------------

@app.delete("/items/{item_id}")
def delete_item(
    item_id: int,
    session: Session = Depends(get_session)
):
    item = session.get(Item, item_id)

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    session.delete(item)
    session.commit()

    return {
        "message": "Item deleted successfully"
    }


# --------------------------------------------------
# ROOT
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "Campus Lost & Found API is running"
    }