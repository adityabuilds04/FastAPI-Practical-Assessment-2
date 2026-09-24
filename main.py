
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select

from database import create_db_and_tables, get_session
from models import Event, EventStatus, Reservation
from schemas import EventCreate, EventUpdate, ReservationCreate


app = FastAPI(
    title="Campus Event Seat Reservation API",
    description="API for managing college events and student seat reservations",
    version="1.0.0"
)


# ==========================================================
# DATABASE STARTUP
# ==========================================================

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# ==========================================================
# EVENT APIs
# ==========================================================


# ----------------------------------------------------------
# 1. CREATE EVENT
# ----------------------------------------------------------

@app.post("/events", response_model=Event, status_code=201)
def create_event(
    event_data: EventCreate,
    session: Session = Depends(get_session)
):
    event = Event(**event_data.model_dump())

    session.add(event)
    session.commit()
    session.refresh(event)

    return event


# ----------------------------------------------------------
# 2. GET ALL EVENTS
# ----------------------------------------------------------

@app.get("/events", response_model=list[Event])
def get_events(
    session: Session = Depends(get_session)
):
    events = session.exec(select(Event)).all()

    return events


# ----------------------------------------------------------
# 3. GET EVENT BY ID
# ----------------------------------------------------------

@app.get("/events/{event_id}", response_model=Event)
def get_event(
    event_id: int,
    session: Session = Depends(get_session)
):
    event = session.get(Event, event_id)

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    return event


# ----------------------------------------------------------
# 4. UPDATE EVENT
# ----------------------------------------------------------

@app.put("/events/{event_id}", response_model=Event)
def update_event(
    event_id: int,
    event_data: EventUpdate,
    session: Session = Depends(get_session)
):
    event = session.get(Event, event_id)

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    update_data = event_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(event, key, value)

    session.add(event)
    session.commit()
    session.refresh(event)

    return event


# ----------------------------------------------------------
# 5. DELETE EVENT
# ----------------------------------------------------------

@app.delete("/events/{event_id}")
def delete_event(
    event_id: int,
    session: Session = Depends(get_session)
):
    event = session.get(Event, event_id)

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    # Delete reservations belonging to this event first
    reservations = session.exec(
        select(Reservation).where(
            Reservation.event_id == event_id
        )
    ).all()

    for reservation in reservations:
        session.delete(reservation)

    session.delete(event)
    session.commit()

    return {
        "message": "Event deleted successfully"
    }


# ==========================================================
# RESERVATION APIs
# ==========================================================


# ----------------------------------------------------------
# 6. CREATE RESERVATION
# ----------------------------------------------------------

@app.post(
    "/events/{event_id}/reserve",
    response_model=Reservation,
    status_code=201
)
def create_reservation(
    event_id: int,
    reservation_data: ReservationCreate,
    session: Session = Depends(get_session)
):
    # Step 1: Check event exists
    event = session.get(Event, event_id)

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    # Step 2: Check event status
    if event.status == EventStatus.Closed:
        raise HTTPException(
            status_code=400,
            detail="Reservations are closed for this event"
        )

    # Step 3: Count existing reservations
    statement = select(Reservation).where(
        Reservation.event_id == event_id
    )

    reservations = session.exec(statement).all()

    booked = len(reservations)

    # Step 4: Check capacity
    if booked >= event.capacity:
        raise HTTPException(
            status_code=400,
            detail="Event is full. No seats available."
        )

    # Step 5: Create reservation
    reservation = Reservation(
        event_id=event_id,
        **reservation_data.model_dump()
    )

    session.add(reservation)
    session.commit()
    session.refresh(reservation)

    return reservation


# ----------------------------------------------------------
# 7. GET EVENT RESERVATIONS
# ----------------------------------------------------------

@app.get(
    "/events/{event_id}/reservations",
    response_model=list[Reservation]
)
def get_event_reservations(
    event_id: int,
    session: Session = Depends(get_session)
):
    # Check event exists
    event = session.get(Event, event_id)

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    statement = select(Reservation).where(
        Reservation.event_id == event_id
    )

    reservations = session.exec(statement).all()

    return reservations


# ----------------------------------------------------------
# 8. DELETE / CANCEL RESERVATION
# ----------------------------------------------------------

@app.delete("/reservations/{reservation_id}")
def delete_reservation(
    reservation_id: int,
    session: Session = Depends(get_session)
):
    reservation = session.get(
        Reservation,
        reservation_id
    )

    if not reservation:
        raise HTTPException(
            status_code=404,
            detail="Reservation not found"
        )

    session.delete(reservation)
    session.commit()

    return {
        "message": "Reservation cancelled successfully"
    }


# ----------------------------------------------------------
# 9. EVENT AVAILABILITY
# ----------------------------------------------------------

@app.get("/events/{event_id}/availability")
def get_availability(
    event_id: int,
    session: Session = Depends(get_session)
):
    # Check event exists
    event = session.get(Event, event_id)

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    # Count booked seats
    statement = select(Reservation).where(
        Reservation.event_id == event_id
    )

    reservations = session.exec(statement).all()

    booked = len(reservations)

    remaining = event.capacity - booked

    return {
        "capacity": event.capacity,
        "booked": booked,
        "remaining": remaining
    }


# ==========================================================
# ROOT
# ==========================================================

@app.get("/")
def root():
    return {
        "message": "Campus Event Seat Reservation API is running"
    }
