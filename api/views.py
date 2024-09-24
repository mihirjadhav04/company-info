from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests  
import yfinance as yf
import json
import os
from django.conf import settings

class CompanyInfoView(APIView):

    def load_company_symbols(self):
        with open(os.path.join(settings.BASE_DIR, 'company_symbols.json')) as f:
            return json.load(f).get("COMPANY_SYMBOLS", {})

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
        # Resolve company symbol from company name
        company_symbol = self.get_company_symbol(company_name)
        
        if not company_symbol:
            return {
                "success": False,
                "message": f"Could not find stock symbol for {company_name}",
                "data": {}
            }

        try:
            stock = yf.Ticker(company_symbol)
            financial_data = stock.info

            if financial_data:
                # Extracting required fields for the response
                data =  {
                    "symbol": financial_data.get("symbol"),
                    "shortName": financial_data.get("shortName"),
                    "longName": financial_data.get("longName"),
                    "sector": financial_data.get("sector"),
                    "industry": financial_data.get("industry"),
                    "currency": financial_data.get("currency"),
                    "marketCap": financial_data.get("marketCap"),
                    "regularMarketPrice": financial_data.get("regularMarketPrice"),
                    "revenue": financial_data.get("totalRevenue"),  # Annual Revenue
                    "netIncome": financial_data.get("netIncomeToCommon"),  # Net income
                    "trailingPE": financial_data.get("trailingPE"),
                    "priceToBook": financial_data.get("priceToBook"),
                    "dividendYield": financial_data.get("dividendYield")
                }

                return {
                    "success": True,
                    "message": f"Financial information for {company_name} retrieved successfully",
                    "data": data
                }
            else:
                return {
                    "success": False,
                    "message": f"No financial data found for {company_name}",
                    "data": {}
                }

        except Exception as e:
            return {"success": False, "message": str(e), "data": {}}

    def get_company_symbol(self, company_name):
        company_symbols = self.load_company_symbols()
        return company_symbols.get(company_name)

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
