Submitted by Shakthi Dharshini - AIML DIET PLANNER PROJECT

# AI/ML-Based Personalized Diet Planner

A full end-to-end AI/ML system that generates personalized weekly diet plans from medical reports.

## 🔍 Problem Statement
Patients receive medical prescriptions but lack clear, personalized dietary guidance.  
This project converts medical reports into structured health insights and generates a 7-day diet plan.

## ✨ Features
- Accepts **Text**, **PDF**, and **Image** medical inputs
- OCR for scanned prescriptions
- NLP-based medical intent extraction
- ML risk prediction using **XGBoost**
- Condition-aware diet generation
- Vegetarian / Non-Vegetarian preference
- Weekly meal plan (Breakfast, Lunch, Snack, Dinner)
- Export results as **PDF** and **JSON**
- Deployed using **Streamlit Cloud**

## 🧠 Tech Stack
- Python
- Streamlit
- Scikit-learn
- XGBoost
- EasyOCR
- PDFPlumber
- ReportLab

## 🗂 Project Structure
# AI/ML-Based Personalized Diet Planner

A full end-to-end AI/ML system that generates personalized weekly diet plans from medical reports.

## 🔍 Problem Statement
Patients receive medical prescriptions but lack clear, personalized dietary guidance.  
This project converts medical reports into structured health insights and generates a 7-day diet plan.

## ✨ Features
- Accepts **Text**, **PDF**, and **Image** medical inputs
- OCR for scanned prescriptions
- NLP-based medical intent extraction
- ML risk prediction using **XGBoost**
- Condition-aware diet generation
- Vegetarian / Non-Vegetarian preference
- Weekly meal plan (Breakfast, Lunch, Snack, Dinner)
- Export results as **PDF** and **JSON**
- Deployed using **Streamlit Cloud**

## 🧠 Tech Stack
- Python
- Streamlit
- Scikit-learn
- XGBoost
- EasyOCR
- PDFPlumber
- ReportLab

## 🗂 Project Structure
diet_backend/
├── app.py
├── diet_rules.py
├── export_utils.py
├── ml_model.py
├── pdf_utils.py
├── image_utils.py
├── requirements.txt
├── assets/
│ └── image/
│ ├── logo.png
│ └── favicon.png
├── xgboost_diet_model.pkl


## 🚀 How to Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
