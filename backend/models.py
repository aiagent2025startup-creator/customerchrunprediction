from pydantic import BaseModel, Field, validator
from typing import List, Optional
from enum import IntEnum

class ComplainsEnum(IntEnum):
    NO = 0
    YES = 1

class AgeGroupEnum(IntEnum):
    GROUP_1 = 1
    GROUP_2 = 2
    GROUP_3 = 3
    GROUP_4 = 4
    GROUP_5 = 5

class TariffPlanEnum(IntEnum):
    PLAN_1 = 1
    PLAN_2 = 2

class StatusEnum(IntEnum):
    ACTIVE = 1
    NON_ACTIVE = 2

class CustomerData(BaseModel):
    Call_Failure: int = Field(..., ge=0, description="Number of call failures")
    Complains: ComplainsEnum = Field(..., description="Customer complained (0: No, 1: Yes)")
    Subscription_Length: float = Field(..., ge=0, description="Months subscribed")
    Charge_Amount: int = Field(..., ge=0, le=9, description="Charge category (0-9)")
    Seconds_of_Use: float = Field(..., ge=0, description="Usage seconds")
    Frequency_of_use: float = Field(..., ge=0, description="Usage frequency")
    Frequency_of_SMS: float = Field(..., ge=0, description="SMS frequency")
    Distinct_Called_Numbers: int = Field(..., ge=0, description="Unique numbers called")
    Age_Group: AgeGroupEnum = Field(..., description="Age category (1-5)")
    Tariff_Plan: TariffPlanEnum = Field(..., description="Plan type (1: Pay as you go, 2: Contractual)")
    Status: StatusEnum = Field(..., description="Account status (1: Active, 2: Non-active)")
    Age: int = Field(..., ge=0, le=120, description="Customer age")
    Customer_Value: float = Field(..., ge=0, description="Customer value score")

    class Config:
        json_schema_extra = {
            "example": {
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
        }

class PredictionResponse(BaseModel):
    churn_prediction: int = Field(..., description="0: Non-churn, 1: Churn")
    churn_probability: float = Field(..., ge=0.0, le=1.0, description="Probability of churn")
    risk_level: str = Field(..., description="Risk level: Low, Medium, High")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Model confidence")
    top_risk_factors: List[dict] = Field(default=[], description="Top contributing features to churn risk")

class BatchPredictionRequest(BaseModel):
    customers: List[CustomerData] = Field(..., min_items=1, max_items=100, description="List of customer data (1-100 items)")

class BatchPredictionResponse(BaseModel):
    predictions: List[PredictionResponse]
    total_customers: int
    high_risk_count: int
    processing_time_ms: float

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    model_accuracy: float
    features: int
    version: str
