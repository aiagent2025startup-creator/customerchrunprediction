# 📊 Dataset Explanation: Iranian Churn Dataset

This project uses the **Iranian Churn Dataset** (UCI Machine Learning Repository ID: 563) to train its machine learning model.

## 🌍 Source
- **Origin**: UCI Machine Learning Repository
- **Dataset Name**: Iranian Churn Dataset
- **Link**: [https://archive.ics.uci.edu/dataset/563/iranian+churn+dataset](https://archive.ics.uci.edu/dataset/563/iranian+churn+dataset)
- **Context**: Data collected from a telecommunications company in Iran.

## 📉 Target Variable
The goal of the dataset is to predict **Churn**.
- **`Churn` (Label)**:
    - `0`: **Non-Churn** (Customer stayed)
    - `1`: **Churn** (Customer left)

## 📝 Features (Inputs)
The dataset contains **13 features** that describe customer behavior and demographics.

| Feature Name | Type | Description |
| :--- | :--- | :--- |
| **Call Failure** | Numeric | Number of times a call failed to connect. |
| **Complains** | Binary | `0`: No complaint, `1`: Customer complained. |
| **Subscription Length** | Numeric | Total months the customer has been with the company. |
| **Charge Amount** | Ordinal | A category (0-9) representing the amount charged. |
| **Seconds of Use** | Numeric | Total seconds of calls made. |
| **Frequency of use** | Numeric | Total number of calls made. |
| **Frequency of SMS** | Numeric | Total number of text messages sent. |
| **Distinct Called Numbers** | Numeric | Total number of unique people called. |
| **Age Group** | Ordinal | Age category (1-5). |
| **Tariff Plan** | Binary | `1`: Pay as you go, `2`: Contractual. |
| **Status** | Binary | `1`: Active, `2`: Non-active. |
| **Age** | Numeric | The age of the customer. |
| **Customer Value** | Numeric | A calculated metric representing the value of the customer to the company. |

## 🧠 Why this data matters
This dataset is valuable because it combines **usage metrics** (seconds of use, SMS frequency) with **customer experience signals** (complaints, call failures). This allows the model to find patterns like:
> *"Customers with high call failures and low usage are 80% more likely to churn."*
