# Start Guide: Customer Churn Prediction System

This guide provides step-by-step instructions to start the Customer Churn Prediction System. The application consists of a FastAPI backend (which also serves the interactive frontend) and an MLflow tracking server.

You can run the application using **Docker** (recommended) or **Locally** using Python.

---

## 🐳 Option 1: Running with Docker (Recommended)

This is the most straightforward method, as it sets up the entire environment, including dependencies, with a single command.

### Prerequisites
- Docker Desktop (ensure it is currently running)
- Docker Compose

### Steps
1. Open your terminal and navigate to the project directory:
   ```bash
   cd "C:\Users\Asus\Desktop\ccs preduction\customerchrunprediction"
   ```

2. Run the following command to build and start the containers in the background:
   ```bash
   docker-compose up -d --build
   ```

3. Wait a few moments for the services to initialize. Once running, you can access the system at:
   - **Frontend Application**: [http://localhost:8000](http://localhost:8000)
   - **API Documentation (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)
   - **MLflow Tracking Server**: [http://localhost:5000](http://localhost:5000)

4. To stop the application later:
   ```bash
   docker-compose down
   ```

---

## 💻 Option 2: Running Locally (Without Docker)

If you don't have Docker installed or prefer to run the services directly on your machine, follow these steps. You will need to start the MLflow server and the Backend server in two separate terminal windows.

### Prerequisites
- Python 3.9+ installed and added to PATH
- `pip` package manager

### Steps

#### 1. Install Dependencies
Open your terminal in the project directory and install the required Python packages:
```bash
pip install -r requirements.txt
```
> **Troubleshooting Tip:** If you encounter a `protobuf` import error when starting the application, you can fix it by running: `pip install protobuf==3.20.3`

#### 2. Start the MLflow Tracking Server
The backend relies on the MLflow server to track experiments and load the model. Start it in your current terminal window:
```bash
mlflow ui --host 0.0.0.0 --port 5000
```
* You can access the MLflow UI at: [http://localhost:5000](http://localhost:5000)

#### 3. Start the FastAPI Backend & Frontend
The FastAPI backend serves the API endpoints and the static frontend UI. 
Open a **new terminal window**, navigate to the project directory, and run:
```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```
*(Alternatively, you can just run `uvicorn backend.main:app --host 0.0.0.0 --port 8000`)*

* You can access the **Frontend App** at: [http://localhost:8000](http://localhost:8000)
* You can access the **API Docs** at: [http://localhost:8000/docs](http://localhost:8000/docs)
