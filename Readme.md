# Company Information API

## Overview

The Company Information API is a Django-based web service designed to retrieve consolidated information about Nifty 50 companies. By accepting a company name as input, the API provides financial data, legal information, and recent news updates from reliable sources. This project leverages various external APIs, including Yahoo Finance, NewsAPI, and others, to gather comprehensive data dynamically.

## Features

- **Fetch Financial Data**: Retrieve detailed financial information for Nifty 50 companies using their stock symbols.
- **Legal Information**: Get insights into any legal issues related to the company.
- **Recent News**: Access the latest news articles about the company from reliable Indian news sources.
- **Company Symbol Mapping**: The stock symbol for a company is fetched from a predefined JSON object containing mappings of Nifty 50 companies to their stock symbols.
- **Rate Limiting**: Rate limiting is implemented to prevent abuse and ensure fair usage of the API.

## Technologies Used

- **Backend Framework**: Django REST Framework
- **Data Fetching Libraries**: `requests`
- **Environment Management**: `dotenv` for managing API keys and environment variables
- **APIs Used**: 
  - Yahoo Finance API (via yfinance)
  - NewsAPI for fetching recent news articles

## Installation

### Prerequisites

- Python 3.x
- Django
- pip

### Steps

1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd <project_directory>
   ```

2. **Install Dependencies**:
   Create a virtual environment and install the required packages:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:
   Create a `.env` file in the project root and add your API keys:
   ```env
   NEWS_API_KEY=<your_news_api_key>
   ```

4. **Run Migrations** (if any):
   ```bash
   python manage.py migrate
   ```

5. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Retrieve Nifty 50 Company Information

- **Endpoint**: `/api/company-info/`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "company_name": "Tata Power"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "message": "Company information retrieved successfully",
    "data": {
      "company_name": "Tata Power",
      "financial_info": { /* financial data */ },
      "legal_info": { /* legal data */ },
      "news_info": [ /* array of news articles */ ]
    }
  }
  ```

## Key Considerations

- **Static Company Symbol Mapping**: The stock symbols for Nifty 50 companies are predefined and stored in a JSON object for direct lookup. Symbols are not fetched dynamically from external sources, ensuring quick retrieval but limiting the API to only Nifty 50 companies.
- **Rate Limiting**: Rate limiting has been applied to prevent overuse and ensure fair usage across different users. This ensures that the service remains responsive and available under high traffic.

## Error Handling

The API handles various errors, including:

- Invalid company name provided.
- Failure to fetch data from external APIs.
- No available financial or news data.

## Future Enhancements

- Implement caching for improved performance.
- Add more data sources for enhanced information retrieval.
- User authentication and authorization for access control.
