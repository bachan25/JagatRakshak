import json
import asyncio
import websockets
from fastapi import APIRouter, Query,APIRouter
import requests
import os

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
MCP_URL = f"wss://mcp.tavily.com/mcp/?tavilyApiKey={TAVILY_API_KEY}"

router = APIRouter()


@router.get("/search", summary='''Search using Tavily MCP server.
The Tavily MCP server provides:search, extract, map, crawl tools. 
Real-time web search capabilities through the tavily-search tool. 
Intelligent data extraction from web pages via the tavily-extract tool. 
Powerful web mapping tool that creates a structured map of website.
Web crawler that systematically explores websites.''')
async def search_by_tavily(
    query: str = Query(..., description="Search query, e.g., 'nearest hospital in Mumbai'")
):
    try:
        url = "https://api.tavily.com/search"
        payload = {
            "api_key": TAVILY_API_KEY,
            "query": query,
            "search_depth": "basic"
        }
        response = requests.post(url, json=payload)
        print(response.json())
        return response.json()
    except Exception as e:
        return {"error": str(e)}
