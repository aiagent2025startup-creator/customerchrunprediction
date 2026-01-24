# Customer Churn Prediction - Viva Guide (Tanglish)

Indha guide unga project viva-ku romba useful-ah irukkum. Simple-ah, student style-la answers irukku.

---

## Project Explanation (Simple Overview)

Indha project-oda main goal **Customer Churn** predict pannradhu. Churn-na oru customer namma service-ai (like telecom or bank) vittu poidrathu. 

Namma **Iranian Churn Dataset** (UCI Repository) use pannirukkom. Idhula 13 features irukku (Call Failure, Subscription Length, etc.). Indha data-vai use panni, oru **LightGBM** model-ai train pannirukkom. Indha model, oru pudhu customer data-vai kudutha, avaru churn aaguvaara illaiya-nu predict pannum.

Project-la **FastAPI** use panni backend build pannirukkom, **MLflow** use panni model-ai track pannrom, and **Docker** use panni deploy pannirukkom.

---

## 25 Viva Questions & Answers

**Q1: Customer Churn na enna?**
A1: Customer service use pannama company vittu poidrathu thaan churn.

**Q2: Indha project main aim enna?**
A2: Customer churn pannuvaana illa-na nu future-la predict pannradhu.

**Q3: Dataset edhirundhu eduthadhu?**
A3: UCI Machine Learning Repository-la irukkura **Iranian Churn Dataset**.

**Q4: Output label enna?**
A4: Churn. 0 = customer stay, 1 = customer leave.

**Q5: Indha dataset-la evlo features irukku?**
A5: Total 13 input features irukku.

**Q6: Most important feature edhu?**
A6: **Complains**, **Call Failure**, and **Status**.

**Q7: Complains churn-ku yen important?**
A7: Complaint pannina customer dissatisfaction irukkum, so churn chance adhigam.

**Q8: Call Failure enna kaatuthu?**
A8: Call connect aagama fail aana count. Network problem indicate pannum.

**Q9: Subscription Length yen important?**
A9: Long-term customer loyal-ah iruppaaru, pudhu customer easy-ah churn pannuvaan.

**Q10: Idhu supervised learning-aa?**
A10: Yes. Input features irukku, output label (Churn) irukku.

**Q11: Idhu classification problem-aa?**
A11: Yes. Output binary (0 or 1).

**Q12: Endha ML algorithms use pannalaam?**
A12: Logistic Regression, Random Forest, LightGBM, XGBoost.

**Q13: Indha project-la best model edhu?**
A13: **LightGBM**, because high accuracy and fast training.

**Q14: LightGBM yen use panrom?**
A14: Large data handle pannum, overfitting kammi, performance nalla irukkum.

**Q15: Train-test split enna?**
A15: Data train panna 80% and test panna 20% split pannirukkom.

**Q16: Feature scaling thevaiyaa?**
A16: Yes. Numerical features-ai correct-aa learn panna help pannum.

**Q17: Model evaluation metrics edhu?**
A17: Accuracy, Precision, Recall, F1-score.

**Q18: Accuracy mattum pothumaa?**
A18: Illa. Churn case-la **Recall** romba important.

**Q19: Recall yen important?**
A19: Churn aagura customers-ai miss pannakoodaadhu, adhaan recall important.

**Q20: Overfitting na enna?**
A20: Model training data-la nalla work pannum, aana new data-la fail aagum.

**Q21: Overfitting eppadi avoid pannuva?**
A21: Cross-validation, regularization, and proper features use pannuvom.

**Q22: Real-time-la indha model eppadi use pannuva?**
A22: Customer data-vai **FastAPI** endpoint-ku anuppi churn probability predict pannuvom.

**Q23: Company indha output-ai eppadi use pannum?**
A23: High-risk customers-ku offers kuduthu retain pannuvaanga.

**Q24: MLOps-ku enna tool use pannirukka?**
A24: **MLflow** use panni model versioning and tracking pannirukkom.

**Q25: Indha project future enhancement enna?**
A25: More data add pannalaam, deep learning try pannalaam, real-time dashboard build pannalaam.
