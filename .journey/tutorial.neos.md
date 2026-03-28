<!--markdownlint-disable MD024 MD033 MD036 MD041 -->

<walkthrough-metadata>
  <meta name="title" content="How to deploy Travel MCP to Cloud Run and use with Gemini CLI" />
  <meta name="description" content="Learn how to deploy the Travel MCP server to Google Cloud Run and connect it to Gemini CLI" />
  <meta name="keywords" content="Gemini CLI, Gemini, Google Cloud Platform, GCP, Cloud Run, MCP" />
</walkthrough-metadata>

# Build and Deploy an MCP Server on Google Cloud

## Let's get started

![Tutorial header image](https://raw.githubusercontent.com/NucleusEngineering/serverless/main/.images/run.jpg)

In this tutorial, we will learn how to deploy a Travel MCP (Model Context Protocol) server to Google Cloud Run and integrate it with Gemini CLI.

<walkthrough-tutorial-difficulty difficulty="3"></walkthrough-tutorial-difficulty>

Estimated time:
<walkthrough-tutorial-duration duration="45"></walkthrough-tutorial-duration>

To get started, click **Start**.

## Project Setup

First, make sure you have the correct project selected.

<walkthrough-project-setup billing="true"></walkthrough-project-setup>

Next, enable the required Google APIs for this tutorial. We need the Cloud Run API and Cloud Build API.

<walkthrough-enable-apis apis="run.googleapis.com,cloudbuild.googleapis.com"></walkthrough-enable-apis>

## Clone the Repository

We need to clone the repository containing the Travel MCP server code.

Run the following command in your Cloud Shell to clone the repository and navigate into the project directory:

```bash
git clone https://github.com/mariyamsalim/bwai-2.git
cd bwai-2/travel-mcp
```

## Deploy to Cloud Run

Now, let's deploy the application directly to Cloud Run from the source code. Google Cloud Run will automatically build the container and deploy it.

Run the following deployment command:

```bash
gcloud run deploy travel-mcp \
  --source . \
  --allow-unauthenticated \
  --region europe-west1
```

Once the deployment completes, the output will display a **Service URL**. Copy this URL, as you'll need it in the next step. It will look something like `https://travel-mcp-XXXXXXXXXX.europe-west1.run.app`.

## Configure Gemini CLI

Now we need to connect the newly deployed Travel MCP server to Gemini CLI. We'll do this by updating the Gemini CLI settings.

Open your Gemini CLI settings file located at `~/.gemini/settings.json`.

```bash
cd
nano .gemini/settings.json
```

Add your deployed Cloud Run service URL to the configuration. **Make sure to append `/mcp` to the end of your Service URL.**

Your configuration should include the following block (replace the URL with your actual Service URL):

```json
{
  "mcpServers": {
    "travel-mcp": {
      "url": "https://travel-mcp-XXXXXXXXXX.europe-west1.run.app/mcp"
    }
  }
}
```

## Test the Initial Integration

Everything is set up! Let's test if Gemini CLI can communicate with your new Travel MCP server.

Run Gemini CLI:

```bash
gemini
```

Once inside the Gemini CLI prompt, try asking the following prompt to test the weather capability for Dubai:

```bash
What is the current weather in Dubai?
```

The CLI will route the request to your deployed Cloud Run service, fetch the information using your MCP server, and provide you with the current weather.

## Add a New MCP Tool

Now, let's extend our Travel MCP server by adding a new tool to fetch tourist attractions.

Don't forget to exit Gemini CLI via double CTRL+C shortcut.

Then you need to navigate travel-mcp directory

```bash
cd
cd cloudshell_open/bwai-2/travel-mcp
```

Open the `main.py` file in your repository and append the following tool function at the appropriate location you can use the open editor button to edit easily using code editor mode.

```python
@mcp.tool()
def get_city_attractions(city: str) -> list:
    """
    Get top tourist attractions for a given city using Wikipedia.
    """
    safe_city = quote(city)
    search_url = (
        f"https://en.wikipedia.org/w/api.php?action=query&list=search"
        f"&srsearch={safe_city}%20tourist%20attractions&format=json"
    )

    headers = {
        'User-Agent': 'TravelMCP'
    }

    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status() 
        data = response.json()

        if "query" in data and "search" in data["query"]:
            results = data["query"]["search"]
            if not results:
                return [f"No attractions found for {city}."]
          
            return [r["title"] for r in results[:5]]
      
        return ["Could not parse attractions data."]

    except requests.exceptions.RequestException as e:
        return [f"Error fetching attractions: {str(e)}"]
```

## Redeploy the Updated Server

Now that we have added the new tool, we need to deploy the updated server.

Run the following command to redeploy to Cloud Run. Notice the addition of the `--clear-base-image` flag:

```bash
gcloud run deploy travel-mcp \
  --source . \
  --allow-unauthenticated \
  --region europe-west1 \
  --clear-base-image
```

## Final Test

Once the deployment is complete, your updated MCP server will automatically be available to Gemini CLI.

Run Gemini CLI again:

```bash
gemini
```

This time, try asking for both the weather and the new tourist attractions functionality:

```bash
Can you give me the top tourist attractions and the current weather in Dubai?
```

Gemini CLI will use both tools provided by your MCP server and deliver a comprehensive response!

## Congratulations!

<walkthrough-conclusion-trophy></walkthrough-conclusion-trophy>

You have successfully deployed an MCP server to Google Cloud Run and connected it to Gemini CLI!

### **What we've covered**

* Cloning a repository in Cloud Shell.
* Deploying a source-based application to Cloud Run.
* Configuring Gemini CLI to use a remote MCP server.

<walkthrough-inline-feedback></walkthrough-inline-feedback>

## Clean up

To avoid incurring charges, you can delete the Cloud Run service we just created.

Go to the Cloud Run Console at [https://console.cloud.google.com/run](https://console.cloud.google.com/run) and delete the `travel-mcp` service.
