{\rtf1\ansi\ansicpg1252\cocoartf2867
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww28600\viewh16640\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import os\
import pandas as pd\
from mcp.server.fastmcp import FastMCP\
\
# MCP Server initialize karein\
mcp = FastMCP("SSLDataMCPServer")\
\
FILE_PATH = "Hardware Support Details.xlsx"\
SHEET_NAME = "SSL Certificates"\
\
@mcp.tool()\
def get_ssl_status() -> str:\
    """Cloud par stored Excel file se SSL certificates ka latest expiry status fetch karta hai."""\
    try:\
        if not os.path.exists(FILE_PATH):\
            return "Error: Excel file server par available nahi hai."\
        \
        # Excel file read karna[cite: 1]\
        df = pd.read_excel(FILE_PATH, sheet_name=SHEET_NAME)\
        \
        summary = "SSL Certificate Status Summary:\\n"\
        for index, row in df.iterrows():\
            domain = str(row.get('Name', '')).strip()\
            expiry = str(row.get('Expiry', '')).strip()\
            if domain and domain != 'nan':\
                summary += f"- Domain: \{domain\} | Expiry: \{expiry\}\\n"\
                \
        return summary\
    except Exception as e:\
        return f"SSL data fetch karne mein error aaya: \{str(e)\}"\
\
if __name__ == "__main__":\
    port = int(os.environ.get("PORT", 8000))\
    mcp.run(transport="sse")}