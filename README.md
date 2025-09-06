# Career Advisor

A one-stop personalized career and education advisor platform, featuring a FastAPI backend with Retrieval-Augmented Generation (RAG) and a Next.js frontend.

---

## Project Structure

```
Career_Advisor/
  backend/
    data/
      courses.md
      jobs.md
      scholarships.md
    main.py
    requirements.txt
    .env
  frontend/
    package.json
    README.md
    ...
backend/
  data/
    courses.md
    jobs.md
    scholarships.md
  main.py
  requirements.txt
  .env
frontend/
  package.json
  README.md
  ...
```

---

## Backend

- **Framework:** FastAPI
- **Features:** Loads career data from markdown files, uses RAG pipeline with Google Gemini LLM, exposes endpoints for querying.
- **Key files:**
  - [`main.py`](Career_Advisor/backend/main.py): FastAPI app, RAG pipeline, API endpoints.
  - [`data/`](Career_Advisor/backend/data/): Markdown files with courses, jobs, and scholarships.

### Running the Backend

1. Create a `.env` file in `backend/` with your `GOOGLE_API_KEY`.
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Start the server:
   ```sh
   uvicorn main:app --reload
   ```
4. API will be available at `http://localhost:8000/`.

---

## Frontend

- **Framework:** Next.js (React)
- **Key files:** `src/`, `package.json`, etc.
- **Usage:** Interacts with backend API to provide a user interface for career guidance.

### Running the Frontend

1. Install dependencies:
   ```sh
   npm install
   ```
2. Start the development server:
   ```sh
   npm run dev
   ```
3. App will be available at `http://localhost:3000/`.

---

## Data

- All career, course, and scholarship data is stored in markdown files in the `backend/data/` directory.
- Example: [`scholarships.md`](Career_Advisor/backend/data/scholarships.md)

---

## License
