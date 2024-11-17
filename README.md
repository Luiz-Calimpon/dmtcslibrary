# DMT Law Case Management System

## Description

The DMT Law Case Management System is a sophisticated web-based application designed to streamline case management for law firms. It offers robust features for case storage, retrieval, and semantic search using advanced natural language processing techniques.

## Features

- Comprehensive case management (Create, Read, Update, Delete)
- Secure file upload and storage
- Advanced semantic search powered by SBERT (Sentence-BERT)
- Automatic model retraining for continuously improving search results
- Responsive and intuitive web interface
- PostgreSQL database for reliable data storage
- Railway integration for easy deployment and scalability

## Technologies Used

- Backend: Python 3.8+, Flask 2.1.0
- Database: PostgreSQL
- ORM: SQLAlchemy 3.0.2
- Frontend: HTML5, CSS3, JavaScript (ES6+)
- NLP: Sentence-BERT (SBERT) 2.2.2
- Task Scheduling: APScheduler 3.9.1
- Deployment: Railway

## Prerequisites

- Python 3.8 or higher
- PostgreSQL 13 or higher
- Railway account (for deployment)
- Git (for version control and deployment)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/dmt-law-case-management.git
   cd dmt-law-case-management
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the project root and add the following:
   ```
   DATABASE_URL=postgresql://username:password@localhost/dmt_law_cases
   SECRET_KEY=your_secret_key_here
   UPLOAD_FOLDER=case_files
   ```

5. Initialize the database:
   ```
   flask db upgrade
   ```

## Usage

To run the application locally:

```
python run.py
```

The application will be available at `http://localhost:5000`.

## Deployment to Railway

1. Create a new project on Railway (https://railway.app/).
2. Add a PostgreSQL database to your Railway project.
3. Connect your GitHub repository to the Railway project.
4. Set the following environment variables in your Railway project settings:
   - `DATABASE_URL`: Use the PostgreSQL connection URL provided by Railway
   - `SECRET_KEY`: A secure random string for Flask sessions
   - `RAILWAY_VOLUME_MOUNT_PATH`: The path where Railway will mount the persistent storage

5. Deploy your application on Railway.

## Project Structure

```
dmt-law-case-management/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   └── utils.py
├── static/
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   └── main.js
│   └── images/
│       └── dmt_logo1.png
├── templates/
│   ├── base.html
│   ├── index.html
│   └── view_case.html
├── .gitignore
├── config.py
├── requirements.txt
├── run.py
└── README.md
```

## Contributing

Contributions to the DMT Law Case Management System are welcome! Please follow these steps to contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
5. Push to the branch (`git push origin feature/AmazingFeature`)
6. Open a Pull Request

Please ensure your code adheres to the project's coding standards and includes appropriate tests.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

Your Name - your.email@example.com

Project Link: [https://github.com/yourusername/dmt-law-case-management](https://github.com/yourusername/dmt-law-case-management)

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Sentence-BERT](https://www.sbert.net/)
- [Railway](https://railway.app/)"# dmtcslibrary" 
