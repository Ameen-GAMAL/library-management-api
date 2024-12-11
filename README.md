# Library Management API

This is a Dockerized RESTful API for managing a collection of books in a library.  
The API supports adding, listing, searching, updating, and deleting books.  
It also includes Swagger/OpenAPI documentation accessible through the `/api-docs` endpoint.

## Features

- **Add a new book** (`POST /books`)
- **List all books** (`GET /books`)
- **Search for books** by author, published year, or genre (`GET /books/search`)
- **Update a book** by ISBN (`PUT /books/{isbn}`)
- **Delete a book** by ISBN (`DELETE /books/{isbn}`)
- **API Documentation** at `/api-docs` (Swagger UI)

## Prerequisites

- Docker installed on your machine.

## Building and Running the Docker Container

1. Clone this repository:
   ```bash
   git clone <repository_url>
   cd library-management-api
