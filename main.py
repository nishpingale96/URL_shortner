import string
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session

from database import init_db, get_db, URLMapping

# --- Task 1: Engine with Step-by-Step Mathematical Logging ---
class Base62Converter:
    ALPHABET = string.digits + string.ascii_lowercase + string.ascii_uppercase
    BASE = len(ALPHABET)

    @classmethod
    def encode(cls, num: int) -> str:
        print(f"  [MATH ENGINE] Starting encoding for Database ID: {num}")
        if num == 0:
            return cls.ALPHABET[0]
        
        original_num = num
        arr = []
        while num > 0:
            num, rem = divmod(num, cls.BASE)
            print(f"    [MATH STEP] {original_num} divided by 62 -> Remainder: {rem} (Character: '{cls.ALPHABET[rem]}')")
            arr.append(cls.ALPHABET[rem])
        
        final_code = "".join(reversed(arr))
        print(f"  [MATH ENGINE] Completed! ID {original_num} translates into Short Code: '{final_code}'")
        return final_code


# --- Lifespan Manager ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("\n========== SERVER LIFECYCLE: STARTUP ==========")
    init_db()
    yield  
    print("\n========== SERVER LIFECYCLE: SHUTDOWN ==========")


app = FastAPI(
    title="Logged URL Shortener",
    lifespan=lifespan
)


class URLShortenRequest(BaseModel):
    long_url: HttpUrl

class URLShortenResponse(BaseModel):
    short_code: str
    short_url: str


# --- Monitored Endpoints ---

@app.post("/api/shorten", response_model=URLShortenResponse, status_code=status.HTTP_201_CREATED)
def shorten_url(payload: URLShortenRequest, db: Session = Depends(get_db)):
    long_url_str = str(payload.long_url)
    print(f"\n[POST /api/shorten] Received request to shorten: {long_url_str}")
    
    # 1. Check Cache/Existence
    print("  [API STEP 1] Checking if URL already exists in database...")
    existing_mapping = db.query(URLMapping).filter(URLMapping.long_url == long_url_str).first()
    if existing_mapping:
        print(f"  [API CACHE HIT] Found existing code '{existing_mapping.short_code}' for this URL. Bypassing creation.")
        return URLShortenResponse(
            short_code=existing_mapping.short_code,
            short_url=f"http://localhost:8000/{existing_mapping.short_code}"
        )

    print("  [API CACHE MISS] URL is new. Inserting row into the database...")

    # 2. Insert to get auto-increment ID
    new_mapping = URLMapping(long_url=long_url_str)
    db.add(new_mapping)
    db.commit()
    db.refresh(new_mapping) 
    print(f"  [API STEP 2] Database committed. Assigned Auto-Increment ID is: {new_mapping.id}")

    # 3. Calculate code based on ID
    print("  [API STEP 3] Handing ID over to the math engine...")
    calculated_code = Base62Converter.encode(new_mapping.id)

    # 4. Save short code back
    print(f"  [API STEP 4] Updating database row {new_mapping.id} with short_code: '{calculated_code}'")
    new_mapping.short_code = calculated_code
    db.commit()

    print("[POST /api/shorten] Request complete. Returning values to client.\n")
    return URLShortenResponse(
        short_code=calculated_code,
        short_url=f"http://localhost:8000/{calculated_code}"
    )


@app.get("/{short_code}", response_class=RedirectResponse)
def redirect_to_long_url(short_code: str, db: Session = Depends(get_db)):
    print(f"\n[GET /{short_code}] Received redirection lookup request...")
    
    print(f"  [API STEP 1] Searching database index for short_code: '{short_code}'")
    db_mapping = db.query(URLMapping).filter(URLMapping.short_code == short_code).first()
    
    if not db_mapping:
        print(f"  [API ERROR] Look up failed. Code '{short_code}' does not exist in the system.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="The requested short URL link code does not exist."
        )
        
    print(f"  [API SUCCESS] Code found! Mapping target is: {db_mapping.long_url}")
    print(f"  [API STEP 2] Sending HTTP 302 Redirect header back to browser.\n")
    return RedirectResponse(url=db_mapping.long_url, status_code=status.HTTP_302_FOUND)