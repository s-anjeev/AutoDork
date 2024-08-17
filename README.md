# Dorking King

Dorking King is a Python script designed to automate the process of using Google dorks to find specific information on the web. It leverages the Google Custom Search API to perform searches and returns results in a user-friendly format.

## Features

- **Automated Google Dorking**: Specify a domain and a dork query or a file containing multiple dorks, and the script will retrieve relevant links using Google Custom Search API.
- **Error Handling**: Manages API rate limits and errors gracefully by switching API keys or pausing as needed.
- **Output Management**: Saves the results of your dorks to an output file, appending new data to existing content.
- **Threading**: (Not yet implemented) Planned support for multithreading to improve performance with large sets of dorks.

## Configuration
The script requires Google API keys and Custom Search Engine (CSE) IDs to function. These should be placed in a config.py file structured like this:

```API_Key = ["YOUR_GOOGLE_API_KEY1", "YOUR_GOOGLE_API_KEY2", ...]```
```CSE_Id = ["YOUR_CSE_ID1", "YOUR_CSE_ID1", ...]```

## usage
Run the script with the following command-line arguments:

1. Perform a single dork search:
```python dorking_king.py -D example.com -Q inurl:login```

2. Perform multiple dork searches from a file:
```python dorking_king.py -D example.com -F dorks.txt```