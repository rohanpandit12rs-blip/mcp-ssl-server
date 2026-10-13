import os
import pandas as pd
import uvicorn
from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP

# FastMCP instance
mcp = FastMCP("SSLDataMCPServer")

FILE_PATH = "Hardware Support Details.xlsx"
SHEET_NAME = "SSL Certificates"

@mcp.tool()
def get_ssl_status() -> str:
    """Cloud par stored Excel file se SSL certificates ka latest expiry status fetch karta hai."""
    try:
        if not os.path.exists(FILE_PATH):
            return "Error: Excel file server par available nahi hai."
        
        df = pd.read_excel(FILE_PATH, sheet_name=SHEET_NAME)
        
        summary = "SSL Certificate Status Summary:\n"
        for index, row in df.iterrows():
            domain = str(row.get('Name', '')).strip()
            expiry = str(row.get('Expiry', '')).strip()
            if domain and domain != 'nan':
                summary += f"- Domain: {domain} | Expiry: {expiry}\n"
                
        return summary
    except Exception as e:
        return f"SSL data fetch karne mein error aaya: {str(e)}"

# FastAPI app get karte hain MCP se
app = mcp.sse_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    # Direct uvicorn run jo 0.0.0.0 par bind karega
    uvicorn.run(app, host="0.0.0.0", port=port)
