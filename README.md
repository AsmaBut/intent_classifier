

```
# 🚀 FastAPI Intent Classifier

This project is a **FastAPI-based Intent Classification API** that classifies user queries into predefined intents (e.g., sending email, scheduling calendar events, or performing web searches).  
It uses **Machine Learning models** (TF-IDF + Logistic Regression / SVM) trained on both real and synthetic datasets.  
The project is containerized using **Docker** for easy deployment.

---

## 📂 Project Structure

```

intent_classifier/
│── main.py                     # FastAPI app entry point
│── create_dataset.py           # Script to generate synthetic noisy dataset
│── requirements.txt            # Python dependencies
│── Dockerfile                  # Docker setup for deployment
│
├── data/
│   ├── full_dataset.csv        # Complete dataset
│   ├── train_dataset.csv       # Training split
│   ├── validation_dataset.csv  # Validation split
│   └── test_dataset.csv        # Testing split
│
├── models/
│   ├── intent_model.pkl        # Trained classification model
│   ├── tfidf_vectorizer.pkl    # TF-IDF vectorizer
│   └── label_encoder.pkl       # Encodes class labels
│
└── tests/
└── test_main.py            # Unit tests for API
└── collab_notebook.py

````

---

## ⚡ Features

- Train ML model on data.  
- REST API built with **FastAPI**.  
- Predict intent from user queries.  
- Includes **unit tests** with `pytest`.  
- Ready for **Docker deployment**.  

---

## 🔧 Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/AsmaBut/intent_classifier.git
cd intent_classifier
````

### 2️⃣ Create & activate virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # On Windows
source venv/bin/activate  # On Linux/Mac
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the API Locally

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

Open your browser or use Postman at:

```
http://127.0.0.1:8000/docs
```

Here you can test the API endpoints with Swagger UI.


## 📌 API Endpoints

### 1. Health Check

**GET** `/api/health`

* **Description**: Verify that the API is running.
* **Response**:

```json
{
  "status": "ok"
}
```

---

### 2. Model Info

**GET** `/api/model/info`

* **Description**: Get details about the trained model.
* **Response**:

```json
{
  "model": "intent_classifier",
  "version": "1.0",
  "labels": ["email_send", "calendar_schedule", "web_search"]
}
```

---

### 3. Classify Single

**POST** `/api/classify`

* **Description**: Classify intent for a single text input.
* **Request Body**:

```json
{
  "text": "schedule a meeting tomorrow at 5 pm"
}
```

* **Response**:

```json
{
  "intent": "calendar_schedule",
  "confidence": 0.87
}
```

---

### 4. Classify Batch

**POST** `/api/classify/batch`

* **Description**: Classify intents for multiple texts in one request.
* **Request Body**:

```json
{
  "texts": [
    "send email to HR",
    "search for AI conferences",
    "set up a meeting on Friday"
  ]
}
```

* **Response**:

```json
[
  {"intent": "email_send", "confidence": 0.91},
  {"intent": "web_search", "confidence": 0.85},
  {"intent": "calendar_schedule", "confidence": 0.89}
]
```

---

## 🐳 Running with Docker

### 1️⃣ Build Docker image

```bash
docker build -t intent-classifier .
```

### 2️⃣ Run container

```bash
docker run -p 8000:8000 intent-classifier
```

Now the API is available at:

```
http://127.0.0.1:8000/docs
```

---

## 🧪 Running Tests

```bash
pytest tests/
```

---

## 📊 Dataset

* Synthetic dataset generated with `create_dataset.py`.
* Includes **noise injection** to ensure model accuracy remains below ~80%.
* Data splits:

  * Train
  * Validation
  * Test

---

## 🚀 Deployment

This project is ready for deployment to:

* **Railway.app**
* **Render**
* **DockerHub + VPS**

---



