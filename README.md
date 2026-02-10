# Chemical Equipment Visualizer

This is a hybrid application that works as both a **Web Application** and a
**Desktop Application**, using a single backend.

The project visualizes chemical equipment data uploaded via CSV files.

---

## Project Components

- Backend: Django + Django REST Framework
- Web Frontend: React (Create React App)
- Desktop Frontend: Python (PyQt5)

---

## Project Structure

chemical-visualizer/
├── backend/
│ ├── backend/
│ ├── equipment/
│ ├── manage.py
│ └── db.sqlite3
│
├── desktop/
│ └── desktop_app.py
│
├── frontend/
│ ├── src/
│ ├── public/
│ ├── package.json
│ └── package-lock.json
│
├── README.md
└── .gitignore


---

## Tech Stack

- Backend: Django, Django REST Framework
- Web Frontend: React (Create React App)
- Desktop Frontend: Python (PyQt5)
- Database: SQLite
- Data Processing: Pandas
- Visualization: Matplotlib

---

## Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/SiripuramVarshitha/chemical-visualizer.git
cd chemical-visualizer
2️⃣ Backend Setup
Create virtual environment:

python -m venv venv
Activate it (Windows):

venv\Scripts\activate
Install dependencies:

pip install -r requirements.txt
Run backend server:

cd backend
python manage.py runserver
3️⃣ Run Desktop Application
Open a new terminal:

cd desktop
python desktop_app.py
4️⃣ Run Web Application
Open another terminal:

cd frontend
npm install
npm start

##Author 
VarshithaSiripuram