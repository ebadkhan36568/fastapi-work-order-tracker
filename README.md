# FastAPI Work-Order Tracker

A REST API built with **FastAPI** for managing work orders. The project uses **Pydantic** for data validation, **JSON** for data persistence, and the **Groq API** to generate AI-powered summaries of work-order descriptions.

## Features

- Create work orders
- View all work orders
- View a single work order by ID
- Update work-order status
- Delete work orders
- Validate request data using Pydantic
- Store work orders in a JSON file
- Generate AI summaries using Groq
- Use environment variables to securely store the API key

## Technologies Used

- Python
- FastAPI
- Pydantic
- Uvicorn
- Groq API
- python-dotenv
- JSON

## Project Structure

```text
fastapi-project/
│
├── main.py
├── README.md
└── .gitignore
```

## Installation

Clone the repository and move into the project directory:

```bash
git clone <repository-url>
cd fastapi-work-order-tracker
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project directory:

```env
GROQ_API_KEY=your_groq_api_key
```

The `.env` file should **not** be committed to GitHub.

## Running the Application

Start the FastAPI development server:

```bash
python -m uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Home endpoint |
| GET | `/work-orders` | Get all work orders |
| POST | `/work-orders` | Create a work order |
| PUT | `/work-orders` | Update work-order status |
| GET | `/work-orders/{id}` | Get a specific work order |
| GET | `/work-orders/summarize/{id}` | Generate an AI summary |
| DELETE | `/work-orders/{id}` | Delete a work order |

## Security

The Groq API key is loaded from an environment variable rather than being hardcoded in the source code.

The `.env` file is excluded from Git using `.gitignore`.