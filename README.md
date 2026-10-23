# Sales Data Analysis Using SQL and Python

An end-to-end sales data analysis web application built using **Python, Flask, PostgreSQL, SQLAlchemy, Pandas, and Matplotlib**. The application combines SQL-based data analysis with Python data processing and interactive web-based visualization.

## 🌐 Live Application

**Live Demo:** https://brazil-ecommerce.onrender.com/

The application is deployed on Render and uses PostgreSQL for database operations.

## 📌 Project Overview

This project demonstrates how SQL and Python can be integrated to analyze e-commerce sales data, extract meaningful business insights, and present the results through a web-based dashboard.

The project covers:

- Connecting Python applications to PostgreSQL.
- Writing SQL queries to retrieve and analyze sales data.
- Data cleaning and transformation using Pandas.
- Filtering, sorting, grouping, and aggregating sales records.
- SQL joins, subqueries, and Common Table Expressions (CTEs).
- Window functions for advanced analytical queries.
- Generating business insights from sales data.
- Visualizing analytical results through a Flask web application.
- Deploying a Python web application using Render and Neon PostgreSQL.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Flask | Web application framework |
| PostgreSQL | Relational database |
| SQLAlchemy | Database connectivity and SQL toolkit |
| Pandas | Data cleaning, manipulation, and analysis |
| Matplotlib | Data visualization |
| Psycopg | PostgreSQL database driver |
| python-dotenv | Loading environment variables from `.env` |
| Gunicorn | Production WSGI server |
| Neon | Cloud PostgreSQL database hosting |
| Render | Web application hosting |

## 📂 Project Structure

A typical project structure is shown below. Adjust the filenames to match your actual repository.

```text
SALES_DATA_ANALYSIS_SQL_PYTHON/
│
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── .env                   # Local environment variables
├── .gitignore             # Files excluded from Git
├── README.md              # Project documentation
│
├── templates/             # HTML templates
│   ├── index.html
│   └── ...
│
├── static/                # CSS, JavaScript, images
│   ├── css/
│   ├── js/
│   └── ...
│
└── ...
```

## ⚙️ Prerequisites

Before running the project locally, install:

- Python 3.10 or a compatible version supported by your dependencies.
- Git.
- A PostgreSQL database, local PostgreSQL 
- A code editor such as Visual Studio Code.

Check your Python and Git installations:

```bash
python --version
git --version
```

## 🚀 1. Run the Project Locally

### Step 1: Clone the repository

Replace `<YOUR_GITHUB_REPOSITORY_URL>` with your actual repository URL.

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Navigate into the project directory:

```bash
cd SALES_DATA_ANALYSIS_SQL_PYTHON
```

### Step 2: Create a virtual environment

On Linux or macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

The `requirements.txt` file should contain:

```text
Flask
SQLAlchemy
pandas
psycopg[binary]
python-dotenv
gunicorn
```

### Step 4: Configure the database

You can use either a local PostgreSQL database or a Neon cloud database.

#### Option A: Use local PostgreSQL

Create a PostgreSQL database for the project.

run the python migrate.py- automatically convert the xls files to database table.

#### Option B: Use Neon PostgreSQL

1. Create an account on [Neon](https://neon.tech/).
2. Create a Neon project.
3. Open the project dashboard.
4. Select **Connect**.
5. Choose the appropriate database, branch, and role.
6. Copy the PostgreSQL connection string.

Keep the connection string private because it contains database credentials.

### Step 5: Create the `.env` file if it connected with Neon postgres database

Create a file named `.env` in the project root directory.

For local PostgreSQL:

```env
DATABASE_URL=postgresql+psycopg://postgres:your_password@localhost:5432/brazil_ecommerce
```

For Neon PostgreSQL, use your actual Neon connection details:

```env
DATABASE_URL=postgresql+psycopg://YOUR_USERNAME:YOUR_PASSWORD@YOUR_NEON_HOST/YOUR_DATABASE?sslmode=require
```

Replace the placeholder values with the credentials and hostname provided by Neon.



### Step 6: Running the code locally
After the database connection succeed, migration run completed. check your database is filled with the tables.
pip install -r requirements.txt
Then type python main.py or app.py (main file)
Automatically localhost url link will be generated then we can see the website

