# Endpoint Validation Report: `/predict`

This document provides a comprehensive validation of the `/predict` endpoint, including the input schema, valid test cases, and error handling for invalid inputs.

## Input Schema

The `/predict` endpoint expects a JSON object with the following fields:

| Field | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `Call_Failure` | `int` | `>= 0` | Number of call failures |
| `Complains` | `int` | `0` or `1` | Customer complained (0: No, 1: Yes) |
| `Subscription_Length` | `float` | `>= 0` | Months subscribed |
| `Charge_Amount` | `int` | `0-9` | Charge category (0-9) |
| `Seconds_of_Use` | `float` | `>= 0` | Usage seconds |
| `Frequency_of_use` | `float` | `>= 0` | Usage frequency |
| `Frequency_of_SMS` | `float` | `>= 0` | SMS frequency |
| `Distinct_Called_Numbers` | `int` | `>= 0` | Unique numbers called |
| `Age_Group` | `int` | `1-5` | Age category (1-5) |
| `Tariff_Plan` | `int` | `1` or `2` | Plan type (1: Pay as you go, 2: Contractual) |
| `Status` | `int` | `1` or `2` | Account status (1: Active, 2: Non-active) |
| `Age` | `int` | `0-120` | Customer age |
| `Customer_Value` | `float` | `>= 0` | Customer value score |

### Exact JSON Schema (Pydantic)

```json
{
  "Call_Failure": 8,
  "Complains": 0,
  "Subscription_Length": 38,
  "Charge_Amount": 0,
  "Seconds_of_Use": 4370,
  "Frequency_of_use": 71,
  "Frequency_of_SMS": 5,
  "Distinct_Called_Numbers": 17,
  "Age_Group": 3,
  "Tariff_Plan": 1,
  "Status": 1,
  "Age": 30,
  "Customer_Value": 197.64
}
```

---

## Validation Results

### 1. Valid Input ✅

**Input:**
```json
{
  "Call_Failure": 8,
  "Complains": 0,
  "Subscription_Length": 38,
  "Charge_Amount": 0,
  "Seconds_of_Use": 4370,
  "Frequency_of_use": 71,
  "Frequency_of_SMS": 5,
  "Distinct_Called_Numbers": 17,
  "Age_Group": 3,
  "Tariff_Plan": 1,
  "Status": 1,
  "Age": 30,
  "Customer_Value": 197.64
}
```

**Expected Output (Status 200):**
```json
{
  "churn_prediction": 0,
  "churn_probability": 0.05,
  "risk_level": "Low",
  "confidence": 0.95,
  "top_risk_factors": [...]
}
```

**Reason:** All fields are within the specified constraints and types.

---

### 2. Invalid Input: Out of Range Age ❌

**Input:**
```json
{
  "Call_Failure": 8,
  "Complains": 0,
  "Subscription_Length": 38,
  "Charge_Amount": 0,
  "Seconds_of_Use": 4370,
  "Frequency_of_use": 71,
  "Frequency_of_SMS": 5,
  "Distinct_Called_Numbers": 17,
  "Age_Group": 3,
  "Tariff_Plan": 1,
  "Status": 1,
  "Age": 150,
  "Customer_Value": 197.64
}
```

**Expected Output (Status 422):**
```json
{
  "detail": [
    {
      "type": "less_than_equal",
      "loc": ["body", "Age"],
      "msg": "Input should be less than or equal to 120",
      "input": 150,
      "url": "https://errors.pydantic.dev/2.5/v/less_than_equal"
    }
  ]
}
```

**Reason:** The `Age` field exceeds the maximum allowed value of 120.

---

### 3. Invalid Input: Invalid Enum Value ❌

**Input:**
```json
{
  "Call_Failure": 8,
  "Complains": 2,
  "Subscription_Length": 38,
  "Charge_Amount": 0,
  "Seconds_of_Use": 4370,
  "Frequency_of_use": 71,
  "Frequency_of_SMS": 5,
  "Distinct_Called_Numbers": 17,
  "Age_Group": 3,
  "Tariff_Plan": 1,
  "Status": 1,
  "Age": 30,
  "Customer_Value": 197.64
}
```

**Expected Output (Status 422):**
```json
{
  "detail": [
    {
      "type": "enum",
      "loc": ["body", "Complains"],
      "msg": "Input should be 0 or 1",
      "input": 2,
      "url": "https://errors.pydantic.dev/2.5/v/enum"
    }
  ]
}
```

**Reason:** The `Complains` field must be either 0 or 1.

---

### 4. Invalid Input: Missing Required Field ❌

**Input:**
```json
{
  "Complains": 0,
  "Subscription_Length": 38,
  "Charge_Amount": 0,
  "Seconds_of_Use": 4370,
  "Frequency_of_use": 71,
  "Frequency_of_SMS": 5,
  "Distinct_Called_Numbers": 17,
  "Age_Group": 3,
  "Tariff_Plan": 1,
  "Status": 1,
  "Age": 30,
  "Customer_Value": 197.64
}
```

**Expected Output (Status 422):**
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "Call_Failure"],
      "msg": "Field required",
      "input": { ... },
      "url": "https://errors.pydantic.dev/2.5/v/missing"
    }
  ]
}
```

**Reason:** `Call_Failure` is a mandatory field in the schema.

---

### 5. Invalid Input: Wrong Data Type ❌

**Input:**
```json
{
  "Call_Failure": "eight",
  "Complains": 0,
  "Subscription_Length": 38,
  "Charge_Amount": 0,
  "Seconds_of_Use": 4370,
  "Frequency_of_use": 71,
  "Frequency_of_SMS": 5,
  "Distinct_Called_Numbers": 17,
  "Age_Group": 3,
  "Tariff_Plan": 1,
  "Status": 1,
  "Age": 30,
  "Customer_Value": 197.64
}
```

**Expected Output (Status 422):**
```json
{
  "detail": [
    {
      "type": "int_parsing",
      "loc": ["body", "Call_Failure"],
      "msg": "Input should be a valid integer, unable to parse string as an integer",
      "input": "eight",
      "url": "https://errors.pydantic.dev/2.5/v/int_parsing"
    }
  ]
}
```

**Reason:** `Call_Failure` expects an integer, but a string was provided.
