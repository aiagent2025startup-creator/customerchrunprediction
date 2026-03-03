# 🚀 Startup Guide: Customer Churn Prediction (Tanglish Version)

Intha guide-la namma Customer Churn Prediction project-a eppadi start panrathu nu step-by-step paakalam. Namma project-la FastAPI backend (ithu thaan frontend-um serve pannuthu) and MLflow tracking server irukku.

Itha neenga **Docker** vechu easy-a run pannalam, illana **Locally** unga system-laye Python vechu run pannalam.

---

## 🐳 Option 1: Docker vechu Run Panrathu (Recommended & Easy!)

Ithu thaan romba easy-ana method. Orey command-la ellam setup aagidum.

### Thevaiyana Items (Prerequisites)
- Docker Desktop (Ithu run aagitrukkanum unga system-la)
- Docker Compose

### Enna pannanum? (Steps)
1. Unga terminal (Command Prompt / PowerShell) open panni project folder-ku pongal:
   ```bash
   cd "C:\Users\Asus\Desktop\ccs preduction\customerchrunprediction"
   ```

2. Keezha irukka command-a run pannunga. Ithu konteynargal-a build panni background-la start pannidum:
   ```bash
   docker-compose up -d --build
   ```

3. Konja neram wait pannunga. Services ellam start aanathum, keezha irukka links-a browser-la check pannalam:
   - **Frontend Application (Namma App)**: [http://localhost:8000](http://localhost:8000)
   - **API Documentation (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)
   - **MLflow Tracking Server**: [http://localhost:5000](http://localhost:5000)

4. App-a stop pannanum na, intha command-a run pannunga:
   ```bash
   docker-compose down
   ```

---

## 💻 Option 2: Locally Run Panrathu (Docker illama)

Unga kitta Docker illana, illana direct-a code-a run panni paakanum na intha steps follow pannunga. Ithu pandrathuku ungaluku rendu terminal (two terminal windows) thevapadum, onnu MLflow-ku innonu Backend-ku.

### Thevaiyana Items (Prerequisites)
- Python 3.9+ install aagirkanum, athu PATH-layum irukanum
- `pip` package manager

### Enna pannanum? (Steps)

#### 1. Dependencies Install Pannunga
Terminal-a project folder-la open panni, thevaiyana packages-a install pannunga:
```bash
pip install -r requirements.txt
```
> **Troubleshooting Tip:** Oruvela app start aagumbothu `protobuf` error vanthuchu na, intha command-a run panni fix pannikonga: `pip install protobuf==3.20.3`

#### 2. MLflow Tracking Server-a Start Pannunga
Namma model-a track panrathukum load panrathukum MLflow server thevai. Ithu mudhal terminal-la run pannanum:
```bash
mlflow ui --host 0.0.0.0 --port 5000
```
* Start aanathum, MLflow UI-a intha link-la paakalam: [http://localhost:5000](http://localhost:5000)

#### 3. FastAPI Backend & Frontend-a Start Pannunga
Ippa namma main API and Frontend-a start pannanum.
Ithuku **Pudhu Terminal window** open pannunga, project folder-ku poittu intha command-a run pannunga:
```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```
*(Illana simply `uvicorn backend.main:app --host 0.0.0.0 --port 8000` kooda run pannalam)*

* Ippa unga **Frontend App** ready! Inga poy paakalam: [http://localhost:8000](http://localhost:8000)
* **API Docs** check panna: [http://localhost:8000/docs](http://localhost:8000/docs)

All the best! 🎉
