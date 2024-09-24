from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests  
from django.conf import settings


class CompanyInfoView(APIView):
    def post(self, request, *args, **kwargs):
        # Retrieve company_name from the JSON body
        company_name = request.data.get('company_name', None)
        
        if not company_name:
            return self.generate_response(success=False, message="Company name is required", data=None, status_code=status.HTTP_400_BAD_REQUEST)
        try:
            # Fetch company financial information
            financial_info = self.get_financial_info(company_name)
            # Fetch company legal information
            legal_info = self.get_legal_info(company_name)
            # Fetch recent news
            news_info = self.get_news_info(company_name)

            # Consolidated response
            response_data = {
                "company_name": company_name,
                "financial_info": financial_info,
                "legal_info": legal_info,
                "news_info": news_info,
            }

            return self.generate_response(success=True, message="Company information retrieved successfully", data=response_data, status_code=status.HTTP_200_OK)

        except Exception as e:
            return self.generate_response(success=False, message=str(e), data=None, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get_financial_info(self, company_name):
        # Placeholder for financial data fetch (replace with actual API calls)
        return {
            "revenue": "1B",
            "market_share": "5%"
        }

    def get_legal_info(self, company_name):
        # Placeholder for legal data fetch (replace with actual API calls)
        return {
            "frauds": 0,
            "default_cases": 1
        }

    def get_news_info(self, company_name):
        api_key = settings.NEWS_API_KEY  # Access the API key from settings

        if not api_key:
            return {"error": "API key not found"}

        # Reliable Indian news domains
        reliable_domains = "thehindu.com,indiatimes.com,ndtv.com,indianexpress.com,hindustantimes.com,livemint.com,business-standard.com,economictimes.indiatimes.com,news18.com,scroll.in"

        url = f'https://newsapi.org/v2/everything?q={company_name}&domains={reliable_domains}&apiKey={api_key}'
        response = requests.get(url)

        if response.status_code == 200:
            articles = response.json().get('articles', [])
            # Filter by recent news (sorted by published date)
            recent_news = sorted(articles, key=lambda x: x['publishedAt'], reverse=True)[:5]  # Get top 5 recent news
            return recent_news
        else:
            return {"error": "News data not available"}

    def generate_response(self, success, message, data, status_code):
        """
        Helper function to standardize API response structure.
        """
        response = {
            "success": success,
            "message": message,
            "data": data
        }
        return Response(response, status=status_code)
