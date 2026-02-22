# Agentic Backend

| Key     | Value                                   |
| ------- | --------------------------------------- |
| Project | `hackathon-java`                        |
| Region  | `us-central1`                           |
| Service | `eagle-eye-banking-app-agentic-backend` |
| Port    | `8350`                                  |

Deploy this after MCP Server.

## 1) One-time setup

```cmd
gcloud config set project hackathon-java
```

```cmd
gcloud services enable cloudbuild.googleapis.com run.googleapis.com artifactregistry.googleapis.com secretmanager.googleapis.com
```

```cmd
gcloud artifacts repositories create cloud-run-apps --repository-format=docker --location=us-central1
```

```cmd
gcloud auth configure-docker us-central1-docker.pkg.dev
```

## 2) IAM setup

```cmd
gcloud projects describe hackathon-java --format="value(projectNumber)"
```

Replace `PROJECT_NUMBER` below:

```cmd
gcloud projects add-iam-policy-binding hackathon-java --member="serviceAccount:PROJECT_NUMBER@cloudbuild.gserviceaccount.com" --role="roles/run.admin"
```

```cmd
gcloud projects add-iam-policy-binding hackathon-java --member="serviceAccount:PROJECT_NUMBER@cloudbuild.gserviceaccount.com" --role="roles/iam.serviceAccountUser"
```

```cmd
gcloud projects add-iam-policy-binding hackathon-java --member="serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com" --role="roles/secretmanager.secretAccessor"
```

## 3) Create or update secrets

Create (first time):

```cmd
echo|set /p="<your-openai-api-key>" | gcloud secrets create OPENAI_API_KEY --data-file=- --replication-policy=automatic --project=hackathon-java
```

```cmd
echo|set /p="https://eagle-eye-banking-app-mcp-server-maaw6nr6mq-uc.a.run.app" | gcloud secrets create MCP_SERVER_HOST --data-file=- --replication-policy=automatic --project=hackathon-java
```

```cmd
echo|set /p="8351" | gcloud secrets create MCP_SERVER_PORT --data-file=- --replication-policy=automatic --project=hackathon-java
```

Update (if already exists):

```cmd
echo|set /p="<your-openai-api-key>" | gcloud secrets versions add OPENAI_API_KEY --data-file=- --project=hackathon-java
```

```cmd
echo|set /p="https://eagle-eye-banking-app-mcp-server-maaw6nr6mq-uc.a.run.app" | gcloud secrets versions add MCP_SERVER_HOST --data-file=- --project=hackathon-java
```

```cmd
echo|set /p="8351" | gcloud secrets versions add MCP_SERVER_PORT --data-file=- --project=hackathon-java
```

## 4) Deploy Agentic Backend

```cmd
cd "D:\My Works\Hackathon AI\Agentic Backend" && gcloud builds submit --config=cloudbuild.yaml --project=hackathon-java .
```

Allow unauthenticated invoke (required for Postman/browser access without IAM token):

```cmd
gcloud run services add-iam-policy-binding eagle-eye-banking-app-agentic-backend --region=us-central1 --project=hackathon-java --member=allUsers --role=roles/run.invoker
```

## 5) Verify

```cmd
gcloud run services describe eagle-eye-banking-app-agentic-backend --region=us-central1 --format="value(status.url)" --project=hackathon-java
```

```cmd
gcloud run services logs read eagle-eye-banking-app-agentic-backend --region=us-central1 --limit=50 --project=hackathon-java
```

If requests fail with `403` unauthenticated:

```cmd
gcloud run services get-iam-policy eagle-eye-banking-app-agentic-backend --region=us-central1 --project=hackathon-java
```
