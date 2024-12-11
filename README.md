# Library Management API

This is a Dockerized RESTful API for managing a collection of books in a library.  
The API supports adding, listing, searching, updating, and deleting books.  
It also includes Swagger documentation accessible through the `/api-docs` endpoint.

## Features

- **Add a new book** (`POST /books`)
- **List all books** (`GET /books`)
- **Search for books** by author, published year, or genre (`GET /books/search`)
- **Update a book** by ISBN (`PUT /books/{isbn}`)
- **Delete a book** by ISBN (`DELETE /books/{isbn}`)
- **API Documentation** at `/api-docs` (Swagger UI)

## Prerequisites

- Docker
- Flask
- flask-swagger-ui==3.36.0

## Building and Running the Docker Container

1. Clone this repository:

   git clone https://github.com/Ameen-GAMAL/library-management-api.git
   cd library-management-api
