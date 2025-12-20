# Constraint News Engine

The Constraint News Engine is a cutting-edge platform designed for aggregating, analyzing, and delivering news content. Utilizing Python, TypeScript, JavaScript, and CSS, it offers a seamless and interactive experience for retrieving and exploring the latest and most relevant news articles.

## Table of Contents

- [Architecture](#architecture)
- [Setup](#setup)
- [Environment Variables](#environment-variables)
- [API Endpoints](#api-endpoints)
- [License](#license)
- [Contributing](#contributing)

---

## Architecture

The architecture of the Constraint News Engine is divided into the following components:

1. **Front-End**: 
   Built using JavaScript and TypeScript, the front end provides an interactive user interface for news exploration. 

2. **Back-End**:
   Implemented in Python, it handles data aggregation, processing, and API endpoint management.

3. **Styling**:
   Utilizes CSS for a clean and responsive design layout.

4. **Database**:
   (Details needed for specific database technology being used - MongoDB, PostgreSQL, etc.)

5. **APIs**:
   The application integrates external APIs for fetching and aggregating news articles.

---

## Setup

To run the repository, follow these steps:

### Prerequisites
- Python 3.8+
- Node.js 14+
- Git for version control
- Package managers: `pip` for Python and `npm` for JavaScript/TypeScript dependencies.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Parth-Malik/ConstraintNewsEngine.git
   ```

2. Navigate to the project directory:
   ```bash
   cd ConstraintNewsEngine
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install Node.js dependencies:
   ```bash
   npm install
   ```

---

## Environment Variables

To configure the app, create a `.env` file in the root directory with the following variables:

```plaintext
# Application
APP_ENV=development

# API Keys
NEWS_API_KEY=your_news_api_key

# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=constraint_news
DB_USER=username
DB_PASSWORD=password

# Other configurations
DEBUG=True
SECRET_KEY=your_secret_key
```

Replace `your_news_api_key`, `username`, `password`, and other placeholders with your actual credentials.

---

## API Endpoints

Here are the key API endpoints provided by the back end:

### Base URL:
```
http://localhost:5000
```

### `GET /api/news`
- **Description**: Fetches the latest news articles.
- **Query Parameters**:
  - **`category`** *(optional)*: The category of news (e.g., sports, technology).
  - **`limit`** *(optional)*: The number of articles to fetch.
- **Response**:
```json
{
    "status": "success",
    "data": [
        {
            "title": "News Title",
            "url": "https://example.com/news",
            "source": "Example News",
            "published_at": "2025-12-18T00:00:00Z"
        }
    ]
}
```

### `POST /api/user/preferences`
- **Description**: Saves or updates user preferences for news personalization.
- **Request Body**:
```json
{
    "user_id": "1234",
    "preferences": ["tech", "sports"]
}
```
- **Response**:
```json
{
    "status": "success",
    "message": "Preferences updated!"
}
```

### `GET /api/user/preferences`
- **Description**: Retrieve user preferences.
- **Response**:
```json
{
    "user_id": "1234",
    "preferences": ["tech", "sports"]
}
```

---

## License

This repository is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contributing

We welcome contributions! To get started:
1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your message here"
   ```
4. Push the changes:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Open a pull request.
