# URL_shortner

# High-Performance Alphanumeric URL Shortener

A lightweight, blazing-fast URL shortener built with Python using **FastAPI**, **SQLAlchemy (SQLite)**, and **Docker**. Instead of using fragile random string hashes, this system uses an industrial-grade **Base62 Encoding Algorithm** mapped directly to auto-incrementing database primary keys, ensuring absolute zero collision risk.

---

## 🚀 Features

* **Zero-Collision Design:** Converts auto-incrementing database row IDs directly into unique Base62 strings (`0-9`, `a-z`, `A-Z`).
* **High Performance:** Designed with indexed lookups inside an asynchronous framework.
* **Modern Lifecycle Architecture:** Uses FastAPI's modern `lifespan` handler for elegant app startup and shutdown hooks.
* **Live Operational Logging:** Integrated backend trace statements print exactly how database allocations and mathematical conversions perform step-by-step.
* **Persisted Container Storage:** Docker volume mapping keeps your data safe across container lifecycles.

---

## 🛠️ System Architecture & Workflow

1. **Shorten Request (`POST /api/shorten`)**:
   * Accepts long destination URL -> Validates format via Pydantic.
   * Checks database cache to prevent duplication.
   * Inserts row to secure an auto-incremented base-10 ID.
   * Passes ID to math engine $\rightarrow$ Encodes to Base62 string string $\rightarrow$ Saves code back to row.

2. **Redirect Request (`GET /{short_code}`)**:
   * Inspects high-speed database index for target `short_code`.
   * Triggers an **HTTP 302 Temporary Redirect** to forward the browser (preserving your ability to inject analytical tracking layers later).

---

## 💾 Local Quickstart (Windows/Mac/Linux)

### 1. Prerequisites & Dependencies
Ensure you have Python 3.10+ installed. Install the core requirements:
```bash
pip install fastapi uvicorn sqlalchemy pydantic
