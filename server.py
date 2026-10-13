import os
import pandas as pd
from mcp.server.fastmcp import FastMCP

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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    # Render ke liye host 0.0.0.0 set karna zaroori hai
    mcp.run(transport="sse", host="0.0.0.0", port=port)
