# Architecture

This repository is organized as a modular knowledge management system. Each module can be used independently, but the verified workflow focuses on the backend API and the supporting utilities.

## Backend Service

The backend service is a Flask API providing CRUD operations for knowledge entries. The API uses SQLite by default and can be configured via environment variables. It exposes a health endpoint, search, and pagination.

### Key responsibilities

- Validate incoming payloads
- Persist entries in SQLite
- Provide filtered queries and pagination
- Return structured JSON responses

## Core OS Module

The core OS module is a small C program used to demonstrate secure operations and system monitoring. The module supports two operations:

- `secure`: writes an encrypted file (XOR demo)
- `monitor`: prints system health for a bounded number of iterations

## AI/ML Utilities

The AI/ML module ships with a deterministic naive Bayes classifier that can be trained on a small CSV dataset. It includes scripts to preprocess data, train the classifier, and run inference.

## Security and SRE Utilities

Security tools provide PBKDF2 password hashing and verification. SRE tools output a lightweight system health report or a bounded monitoring loop.

## Web App

The web app is intentionally static. It can be served with a local HTTP server and uses the backend API for CRUD operations.
