# Student Viva Presentation: Customer Churn Prediction System

## 1. Project Title & Domain
**Title:** Customer Churn Prediction using Machine Learning and MLOps
**Domain:** Data Science and Machine Learning (Predictive Analytics)

---

## 2. Problem Statement
**What is Customer Churn?**
Customer churn occurs when customers stop doing business with a company. In the telecom industry, it means a subscriber cancels their service. It is much more expensive to acquire a new customer than to retain an existing one.

---

## 3. Objective of the Project
The goal is to build an end-to-end system that can:
1. Predict which customers are likely to churn based on their usage patterns.
2. Provide a user-friendly interface for managers to check churn risk.
3. Use MLOps tools like MLflow to track experiments and manage model versions.

---

## 4. Why this problem is important
Churn directly affects a company's revenue. By predicting churn early, companies can offer discounts or better services to "at-risk" customers, thereby increasing customer retention and long-term profitability.

---

## 5. Dataset Explanation
I used the **Iranian Churn Dataset** from the UCI Machine Learning Repository.
- **Size:** 3,150 records.
- **Features:** 13 features including Call Failure, Subscription Length, Charge Amount, Seconds of Use, and Customer Value.
- **Target:** A binary label (1 for Churn, 0 for Non-Churn).

---

## 6. Machine Learning Model Used
I chose **LightGBM (Light Gradient Boosting Machine)**.
- **Why?** It is highly efficient, handles large datasets well, and provides high accuracy for tabular data. It uses a leaf-wise growth strategy which often results in better performance compared to other boosting algorithms.

---

## 7. System Architecture
The project consists of three main components:
1. **Frontend:** A clean web interface built with HTML/CSS and Vanilla JavaScript.
2. **Backend:** A high-performance API built using **FastAPI**.
3. **MLOps Layer:** **MLflow** for tracking training runs and serving as a Model Registry.
4. **Deployment:** The entire system is containerized using **Docker**.

---

## 8. ML Workflow
1. **Data Preprocessing:** Handling missing values and feature engineering.
2. **Training:** Training the LightGBM model.
3. **Evaluation:** Checking metrics like Accuracy and F1-Score.
4. **Versioning:** Registering the best model in the MLflow Model Registry.
5. **Deployment:** The FastAPI backend loads the "Production" model from MLflow to make real-time predictions.

---

## 9. Tools & Technologies Used
- **Language:** Python
- **ML Library:** LightGBM, Scikit-learn, Pandas
- **API Framework:** FastAPI
- **MLOps:** MLflow
- **Containerization:** Docker & Docker Compose
- **Frontend:** HTML, CSS, JavaScript

---

## 10. How MLflow is used
MLflow acts as the backbone for our model management:
- **Tracking:** It logs hyperparameters (like learning rate) and metrics (like accuracy) for every training run.
- **Model Registry:** It allows us to tag specific models as "Staging" or "Production," making it easy to roll back or update models without changing the code.

---

## 11. How predictions are made
1. The user enters customer data in the frontend.
2. The frontend sends a JSON request to the FastAPI backend.
3. The backend preprocesses the data and passes it to the loaded LightGBM model.
4. The model returns a churn probability, which the backend converts into a Risk Level (Low, Medium, High).

---

## 12. Real-world applications
- **Telecom:** Identifying subscribers likely to switch providers.
- **Banking:** Predicting which customers might close their accounts.
- **SaaS:** Identifying users who might cancel their monthly subscriptions.

---

## 13. Conclusion
This project demonstrates how a machine learning model can be moved from a notebook into a production-ready application. By integrating MLflow and Docker, we ensure that the model is scalable, trackable, and easy to deploy in a real business environment.

---

## 14. Common Viva Questions & Answers

**Q1: Why did you use FastAPI instead of Flask?**
*A: FastAPI is much faster, has built-in data validation using Pydantic, and automatically generates interactive API documentation (Swagger UI).*

**Q2: What is the benefit of using Docker here?**
*A: Docker ensures that the application runs the same way on any machine by packaging all dependencies together. It solves the "it works on my machine" problem.*

**Q3: How do you handle imbalanced data in churn prediction?**
*A: Churn datasets are often imbalanced. We can handle this using techniques like SMOTE, adjusting class weights in LightGBM, or focusing on metrics like Precision-Recall instead of just Accuracy.*

**Q4: What does the 'Model Registry' in MLflow do?**
*A: It provides a centralized store to manage the full lifecycle of an ML model, including versioning and stage transitions (e.g., from Staging to Production).*
