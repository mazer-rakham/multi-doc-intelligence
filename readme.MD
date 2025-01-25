# Document Intelligence Azure Function

This repository contains an Azure Function app that processes documents stored in an Azure Blob Storage container using Azure's Document Intelligence service. The function analyzes each document to extract language information, page details, and paragraphs.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Environment Variables](#environment-variables)
- [Functionality](#functionality)
- [Error Handling](#error-handling)
- [Contributing](#contributing)

## Overview

The function is triggered via an HTTP request and performs the following tasks:

1. Lists all blobs in a specified Azure Blob Storage container.
2. Generates a SAS URL for each blob.
3. Analyzes each document using Azure's Document Intelligence service.
4. Extracts and returns language information, page details, and paragraphs for each document.

## Prerequisites

- Azure account with access to Azure Blob Storage and Azure Document Intelligence.
- Python 3.8 or later.
- Azure Functions Core Tools for local development and testing.

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/mazer-rakham/multi-doc-intelligence
   cd document-intelligence-function
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables as described below.

## Environment Variables

The function requires the following environment variables to be set:

- `DOCUMENTINTELLIGENCE_ENDPOINT`: The endpoint URL for the Azure Document Intelligence service.
- `DOCUMENTINTELLIGENCE_API_KEY`: The API key for authenticating with the Document Intelligence service.
- `AZURE_STORAGE_CONNECTION_STRING`: The connection string for accessing Azure Blob Storage.
- `CONTAINER`: The name of the Azure Blob Storage container containing the documents to be processed.

## Functionality

The function is defined in `function_app.py` and is triggered by an HTTP request to the `/doc_int` route. It performs the following steps:

- Loads the necessary environment variables.
- Initializes clients for Azure Document Intelligence and Azure Blob Storage.
- Lists all blobs in the specified container.
- Generates a SAS URL for each blob to securely access it.
- Analyzes each document using the Document Intelligence service.
- Extracts language information, page details, and paragraphs from the analysis result.
- Returns the extracted data as a JSON response.

## Error Handling

The function includes error handling for HTTP response errors that may occur during document processing. If an error occurs, it logs the error and returns a 500 HTTP status code with an error message.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.



