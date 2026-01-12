# ITC CodeAI - IT Creative Academy Project

Welcome to **ITC CodeAI**, a modern Full Stack AI Chatbot application developed by **IT Creative Academy**. This project integrates a powerful Django backend with a sleek, responsive React frontend.

## 🌟 Features

### 🤖 AI Chatbot
-   **Multimodal Intelligence**: Capable of understanding and processing both **Text** and **Images** using Google Gemini AI.
-   **Context Board**: Maintains chat history for seamless conversations.
-   **Image Analysis**: Upload images for the AI to describe, analyze, or extract code from.

### 🔐 Authentication & Users
-   **Secure Auth**: JWT-based Authentication (Login/Register/Refresh).
-   **Premium System**: Special "Premium" status for users, managed by Admins.
-   **Custom Profiles**: Extensible user model.

### 🎨 Modern UI/UX (Frontend)
-   **Tech Stack**: Built with **React (Vite)**, **TailwindCSS**, and **Framer Motion**.
-   **Themes**: Fully supported **Dark Mode** and Light Mode with a glassmorphic aesthetic.
-   **Responsive**: Optimized for Desktop and Mobile devices.
-   **Animations**: Smooth transitions and interactive elements.

### 🛠 Backend
-   **Framework**: Django 5 + Django Rest Framework (DRF).
-   **Admin Panel**: Custom Admin interface to manage Chat Sessions and Users.
-   **API**: Well-structured RESTful endpoints.

---

## 🚀 Installation & Setup

### Prerequisites
-   Python 3.10+
-   Node.js 18+
-   Git

### 1. Clone the Repository
```bash
git clone https://github.com/xusanbek0039/itc_code_ai.git
cd itc_code_ai
```

### 2. Backend Setup (Django)
Navigate to the root directory.

1.  **Create Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\Activate
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment**:
    Create a `.env` file in the root directory:
    ```ini
    SECRET_KEY=your_secret_key
    DEBUG=True
    GEMINI_API_KEY=your_google_gemini_api_key
    ```

4.  **Run Migrations**:
    ```bash
    python manage.py migrate
    ```

5.  **Create Superuser** (for Admin Panel):
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run Server**:
    ```bash
    python manage.py runserver
    ```
    Backend will be available at `http://127.0.0.1:8000`.

### 3. Frontend Setup (React)
Open a new terminal and navigate to the `frontend` folder.

1.  **Navigate**:
    ```bash
    cd frontend
    ```

2.  **Install Dependencies**:
    ```bash
    npm install
    ```

3.  **Run Development Server**:
    ```bash
    npm run dev
    ```
    Frontend will be available at `http://localhost:5173`.

---

## 📖 Usage Guide

1.  **Register/Login**: Open the frontend and create a new account.
2.  **Chat**:
    -   Type a message to start chatting.
    -   Click the **Image Icon** to upload a picture for the AI to analyze.
3.  **Settings**:
    -   Click the **Moon/Sun** icon in the navbar to toggle themes.
    -   Use the **Logout** button to end your session.
4.  **Admin**:
    -   Go to `http://127.0.0.1:8000/admin/` to view all chat logs and manage users (e.g., grant Premium status).

## 🏗 Tech Stack overview

| Component | Technology |
| :--- | :--- |
| **Backend** | Django, DRF, SimpleJWT, Python |
| **Frontend** | React, Vite, TailwindCSS, Axios |
| **AI Model** | Google Gemini (via `google-generativeai`) |
| **Database** | SQLite (Dev) / PostgreSQL (Prod ready) |
| **Styling** | TailwindCSS, Lucide Icons, Framer Motion |

---

Developed with ❤️ by **IT Creative Academy**.
