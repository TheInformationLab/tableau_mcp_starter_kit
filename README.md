# Tableau MCP Starter Kit

A powerful integration that brings AI functionality to Tableau Server or Tableau Cloud using MCP and LangChain, enabling natural language interactions with the data you trust in Tableau.

This repo is an implementation of [tableau-mcp](https://github.com/tableau/tableau-mcp) using the MCP tools with LangChain, building on the [tableau_langchain_starter_kit](https://github.com/TheInformationLab/tableau_langchain_starter_kit).

## 🚀 Features

- Natural language querying of Tableau data
- Available via Web interface or Dashboard extension
- Support for both Tableau Server and Tableau Cloud

## 📋 Prerequisites

Before you begin, ensure you have the following:

- **Tableau Server Version 2025.1** or later OR **Tableau Cloud**, a free Tableau Cloud trial is available via the [Tableau Developer Program](https://www.tableau.com/en-gb/developer)
- **Python 3.12+** - [Download Python](https://python.org/downloads/)
- **Git** - [Download Git](https://git-scm.com/downloads/)
- **API credentials** for your chosen AI model (OpenAI, etc.)

## ⚠️ Warning

When using this code, data from Tableau will be sent to an external AI model (by default, OpenAI). For learning and testing, it is strongly recommended to use the Superstore dataset included with Tableau.

If you need to process sensitive or proprietary information, consider configuring the tool to use a local AI model instead of an external service. This approach ensures your data remains within your organisation’s infrastructure and reduces the risk of data exposure.

## 📺 Quickstart Tableau MCP Guides

If you haven't tried Tableau MCP yet I recommend testing it out using desktop applications like Claude Desktop and VSCode. You can find links to my quickstart tutorials below.

<div align="center">

<a href="https://www.youtube.com/watch?v=hmdzDlMBraw">
    <img src="https://img.youtube.com/vi/hmdzDlMBraw/maxresdefault.jpg" width ="48%">
</a>
<a href="https://www.youtube.com/watch?v=opbXLGZDKdU">
    <img src="https://img.youtube.com/vi/opbXLGZDKdU/maxresdefault.jpg" width ="48%">
</a>

</div>

## 📺 Step Up Guide 

<a href="https://www.youtube.com/watch?v=juD1rQxhiqA">
    <img src="https://img.youtube.com/vi/juD1rQxhiqA/maxresdefault.jpg" width ="80%">
</a>

## 🛠️ Installation

### 1. Install Tableau MCP

```bash
git clone https://github.com/tableau/tableau-mcp.git
cd tableau-mcp
```

From the [Install Guide](https://github.com/tableau/tableau-mcp?tab=readme-ov-file#install-prerequisites)

Install Node.js (tested with 22.15.0 LTS)
```bash
npm install
npm run build
```

### 2. Clone the Starter Kit Repository

```bash
git clone https://github.com/TheInformationLab/tableau_mcp_starter_kit.git
cd tableau_mcp_starter_kit
```

### 3. Create Virtual Environment

Creating a virtual environment helps isolate project dependencies:

```bash
python -m venv .venv
```

### 4. Activate Virtual Environment

**Windows:**
```bash
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

💡 **Tip:** You should see `(.venv)` at the beginning of your command prompt when the virtual environment is active.

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

If you encounter any installation issues, try upgrading pip first:
```bash
pip install --upgrade pip
```

## ⚙️ Configuration

### Environment Variables Setup

1. Copy the template environment file:
```bash
cp .env_template .env
```

2. Open the `.env` file in your preferred text editor and configure the following variables:

```
# Tableau MCP Server Config
TRANSPORT='stdio'
SERVER='https://my-tableau-server.com'
SITE_NAME='TableauSiteName'
PAT_NAME='Tableau Personal Access Token (PAT) Name'
PAT_VALUE='Tableau Personal Access Token (PAT) Secret Key'

# Tableau MCP Server Optional Configs
DATASOURCE_CREDENTIALS=''
DEFAULT_LOG_LEVEL='debug'
INCLUDE_TOOLS=''
EXCLUDE_TOOLS=''
MAX_RESULT_LIMIT=''
DISABLE_QUERY_DATASOURCE_FILTER_VALIDATION=''

# Local Filepath Config
TABLEAU_MCP_FILEPATH='your/local/filepath/to/tableau-mcp/build/index.js'

# Model Providers
OPENAI_API_KEY='from OpenAI developer portal'

# Langfuse 
LANGFUSE_PUBLIC_KEY = 'Public key from https://langfuse.com/'
LANGFUSE_SECRET_KEY = 'Secret key from https://langfuse.com/'
LANGFUSE_HOST = 'https://cloud.langfuse.com'

# Custom MCP Tool Extra Configs
# from: https://github.com/wjsutton/tableau-mcp-experimental
FIXED_DATASOURCE_LUID='unique identifier for a data source found via the graphql metadata API'
```

⚠️ **Security Note:** Never commit your `.env` file to version control. It's already included in `.gitignore`.

## 🏃‍♂️ Running the Application

### Web Interface Mode

Launch the full web application with dashboard extension support:

```bash
python web_app.py
```

Once running, open your browser and navigate to:
- **Local development:** `http://localhost:8000`
- The application will display the correct URL in the terminal

You will now be able to ask questions in natural language:
   - "What are the trends in customer satisfaction?"
   - "Compare revenue between Q1 and Q2"
   - "Show me outliers in the sales data"

You can also run this web application with dashboard extension support.

Once running, open your Tableau workbook, or the [Superstore Dashboard](dashboard_extension\Superstore.twbx)

On a dashboard page, in the bottom left menu, drag a dashboard extension, local extension, and select [tableau_langchain.trex](dashboard_extension\tableau_langchain.trex) from the dashboard_extension folder. 

### Custom Dashboard Extension

The script `dashboard_app.py` is configured to use only a single datasource, using custom tools from [https://github.com/wjsutton/tableau-mcp-experimental](https://github.com/wjsutton/tableau-mcp-experimental). 

To do

1. Install the custom tools:
```bash
git clone https://github.com/wjsutton/tableau-mcp-experimental.git
cd tableau-mcp-experimental
```

2. With Node.js (tested with 22.15.0 LTS) execute:
```bash
npm install
npm run build
```

3. Return to the Tableau MCP Starter Kit:
```
cd ..
cd tableau_mcp_starter_kit
```

4. In dashboard_app.py, update: `Line 36: mcp_location` to the local file path of tableau-mcp-experimental

5. Find your datasource luid, you can use the [utilities/find_datasource_luid.gql](utilities/find_datasource_luid.gql) to query your Tableau Server / Cloud's Metadata API. 

6. In .env add your datasource luid to the FIXED_DATASOURCE_LUID environment variable.  

7. Run the dashboard_app script
```bash
python dashboard_app.py
```

Verify the app is running, open your browser and navigate to:
- **Local development:** `http://localhost:8000`
- The application will display the correct URL in the terminal

Once running, open your Tableau workbook, or the [Superstore Dashboard](dashboard_extension\Superstore.twbx)

On a dashboard page, in the bottom left menu, drag a dashboard extension, local extension, and select [tableau_langchain.trex](dashboard_extension\tableau_langchain.trex) from the dashboard_extension folder. 


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Get Involved

- Check out the [Tableau MCP](https://github.com/tableau/tableau-mcp) repo for further developments
- Join the [#tableau-ai-solutions](https://tableau-datadev.slack.com/archives/C07LMAVG4N6) conversation on Slack. Sign up to the [DataDev Slack channel here.](https://tabsoft.co/JoinTableauDev)

## 🙏 Acknowledgments

- [Tableau MCP](https://github.com/tableau/tableau-mcp) the team developing the tools
- [The Tableau LangChain Starter Kit](https://github.com/TheInformationLab/tableau_langchain_starter_kit) the prequel to this project 
- [LangChain](https://langchain.com/) for the AI framework
- [Tableau](https://tableau.com/) for the visualisation platform
- All contributors who have helped improve this project

---

**⭐ If you find this project helpful, please consider giving it a star!**
