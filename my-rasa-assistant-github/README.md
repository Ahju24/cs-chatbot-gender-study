# How to Replicate the Rasa Chatbot 

This repository contains the source code and Docker configurations to replicate the Rasa mentoring assistant. This chatbot was created with Rasa Developer Edition and is able to interact with users under specific experimental conditions.

---

## Table of Contents

1. [Prerequisites](#-prerequisites)
2. [Project Structure](#-project-structure)
3. [Quick Start (Local Deployment)](#-quick-start-local-deployment)
4. [Production Deployment (GitHub Pages + GCP)](#-production-deployment-github-pages-gcp) 

---

## Prerequisites

To run this assistant, you need to have the following installed:

* [Docker](https://www.docker.com/get-started) (Desktop or Engine)
* [Docker Compose](https://docs.docker.com/compose/)
* [Rasa](https://rasa.com/docs/pro/installation/python/?utm_campaign=2024-01-Personal-Edition-License-Key-Request&utm_medium=email&_hsenc=p2ANqtz-88adczHb-fAkmp6EGBh23CJwoQKSSz-K0DpHaWIkTIMHX6Z1i1TPr6_YvAGRS7JVHY_Xk6nVxedbwOK-Q7Udlak8FTcA&_hsmi=292413219&utm_content=292413219&utm_source=hs_automation)

*Note: Because this project uses the Rasa Developer Edition, you will need a free Developer Edition License key (request it [here](https://rasa.com/rasa-pro-developer-edition-license-key-request)). Make sure to add it in your .env file!*

---

## Project Structure

```text
├── actions/                  
│   ├── __init__.py          
│   └── actions.py           # Custom Python actions
├── data/                    
│   ├── flows.yml            # Structured sequence of steps for conversation
│   └── patterns.yml         # Defines patterns how to handle “meta” conversational situations
├── config.yml               # Assistant configurations (language, pipeline, policies)
├── domain.yml               # Defines slots, actions and response templates
├── endpoints.yml            # Action server endpoint & tracker configuration 
├── credentials.yml          # External channel settings (REST)
├── docker-compose.yml       # Docker-compose file (Assistant + Action Server)
└── README.md                

```

---

## Quick Start (Local Deployment)

Follow these steps to run the assistant and custom action server on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/Ahju24/cs-chatbot-gender-study.git
cd cs-chatbot-gender-study/my-rasa-assistant-github

```

### 2. Train the Rasa Model

Train the initial model using:

```bash
rasa train

```

### 3. Launch the Chatbot Stack
Build your Docker image:
```bash
docker compose build

```

Start both the Rasa assistant and the custom Python Action Server:

```bash
docker compose up -d

```

### 4. Testing the Chatbot

When you visit http://localhost:5005, you should see a "Hello from Rasa: 3.15.10".

To chat with the chatbot, simply open the [index.html](index.html) file in a browser.

---

## Production Deployment (GitHub Pages + GCP)
First, upload [index.html](index.html) to a GitHub repository and use this repository for creating a website with GitHub Pages (click [here](https://docs.github.com/en/pages/quickstart#creating-your-website) for more details).

For online deployment, the assistant can be deployed via Google Cloud Platform (GCP).

1. Create a new GCP project (click [here](https://developers.google.com/workspace/guides/create-project) for more details)
2. Tag & Push your Action Server Docker Image to your GCP Artifact Registry (click [here](https://docs.cloud.google.com/artifact-registry/docs/docker/store-docker-container-images#add-image) for more details).
3. Deploy both services using GCP Cloud Run.
* Select "Deploy one revision from an existing container image"
* Select container image from Artifact Registry
* Choose your Service name and Region
* Authentication: Allow public access
* Billing: Request-based
* Service scaling: Auto scaling with 0 min. instances for lower costs, 1 if you want quicker starts; set max. to 2 or 3
* Ingress: All
* Container port: 5055 (Action Server); 5005 (Assistant)
* Container arguments: run actions --port 5055 --actions actions (Action Server); run --enable-api --endpoints endpoints.yml --credentials credentials.yml --port 5005 --cors ["https://your-github-repository-with-index-html"] (Assistant)
* Resources: Memory 1 GiB & 1 CPU (Action Server); 4 GiB & 1 CPU (Assistant)
* Requests: Request timeout 500, Max. concurrent requests per instance 80
* Execution environment: Default
* Select Startup CPU boost
* Add Environment variables: RASA_LICENSE, DB_PASSWORD, HF_TOKEN, MONGO_URL, MONDO_USER, MONGO_PASS (Action Server); RASA_USER_APP, HF_TOKEN, DB_PASSWORD, RASA_LICENSE, MONGO_URL, MONGO_USER, RASA_TELEMETRY_ENABLED=false, CORS_ORIGINS=* (Assistant)
* Networking: Select nothing (Action Server); Select Session affinity (Assistant)
* Security: Use default settings