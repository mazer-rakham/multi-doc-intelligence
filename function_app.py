import azure.functions as func
import logging
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import DocumentAnalysisFeature, AnalyzeResult, AnalyzeDocumentRequest
from azure.core.exceptions import HttpResponseError
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="doc_int")
def doc_int(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Load environment variables
    endpoint = os.environ["DOCUMENTINTELLIGENCE_ENDPOINT"]
    key = os.environ["DOCUMENTINTELLIGENCE_API_KEY"]
    connection_string = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
    container_name = "your-container-name"

    document_intelligence_client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    response_data = []

    try:
        # List all blobs in the container
        blobs = container_client.list_blobs()
        for blob in blobs:
            # Generate SAS URL for each blob
            sas_token = generate_blob_sas(
                account_name=blob_service_client.account_name,
                container_name=container_name,
                blob_name=blob.name,
                account_key=blob_service_client.credential.account_key,
                permission=BlobSasPermissions(read=True),
                expiry=datetime.utcnow() + timedelta(hours=1)
            )
            sas_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{blob.name}?{sas_token}"

            # Analyze each document
            poller = document_intelligence_client.begin_analyze_document(
                "prebuilt-read",
                AnalyzeDocumentRequest(url_source=sas_url),
                features=[DocumentAnalysisFeature.LANGUAGES]
            )

            result: AnalyzeResult = poller.result()

            document_data = {
                "blob_name": blob.name,
                "languages": [],
                "pages": [],
                "paragraphs": []
            }

            if result.languages is not None:
                for language in result.languages:
                    document_data["languages"].append({
                        "locale": language.locale,
                        "confidence": language.confidence
                    })

            for page in result.pages:
                page_data = {
                    "page_number": page.page_number,
                    "width": page.width,
                    "height": page.height,
                    "unit": page.unit,
                    "words": []  # Collect words directly from the page
                }
                
                # Iterate over words directly from the page
                if page.words:
                    for word in page.words:
                        word_data = {
                            "content": word.content,
                            "polygon": word.polygon,
                            "confidence": word.confidence
                        }
                        page_data["words"].append(word_data)
                
                document_data["pages"].append(page_data)

            if result.paragraphs:
                for paragraph in result.paragraphs:
                    document_data["paragraphs"].append({
                        "content": paragraph.content,
                        "bounding_regions": paragraph.bounding_regions
                    })

            response_data.append(document_data)

        return func.HttpResponse(
            body=str(response_data),
            status_code=200,
            mimetype="application/json"
        )

    except HttpResponseError as error:
        logging.error(f"Error processing document: {error}")
        return func.HttpResponse(
            "An error occurred while processing the documents.",
            status_code=500
        )