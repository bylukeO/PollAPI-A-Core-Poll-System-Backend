# Poll API Documentation

## Overview
A RESTful API for creating and managing polls, built with Django REST Framework.

## Base URL
```
http://127.0.0.1:8000/api/
```

## Endpoints

### Polls

#### List All Polls / Create Poll
- **URL:** `/polls/`
- **Methods:** `GET`, `POST`

**GET Response:**
```json
[
  {
    "id": 1,
    "question_text": "What is your favorite color?",
    "pub_date": "2025-08-30T22:00:00Z",
    "options": [
      {
        "id": 1,
        "option_text": "Red"
      },
      {
        "id": 2,
        "option_text": "Blue"
      }
    ]
  }
]
```

**POST Request:**
```json
{
  "question_text": "What is your favorite color?",
  "pub_date": "2025-08-30T22:00:00Z"
}
```

#### Get Poll Details
- **URL:** `/polls/{id}/`
- **Method:** `GET`

**Response:**
```json
{
  "id": 1,
  "question_text": "What is your favorite color?",
  "pub_date": "2025-08-30T22:00:00Z",
  "options": [
    {
      "id": 1,
      "option_text": "Red"
    },
    {
      "id": 2,
      "option_text": "Blue"
    }
  ]
}
```

### Voting

#### Submit Vote
- **URL:** `/polls/{poll_id}/vote/`
- **Method:** `POST`

**Request:**
```json
{
  "option_id": 1
}
```

**Response:**
```json
{
  "poll": 1,
  "option_id": 1
}
```

#### List All Votes
- **URL:** `/votes/`
- **Method:** `GET`

**Response:**
```json
[
  {
    "poll": 1,
    "option_id": 1
  },
  {
    "poll": 1,
    "option_id": 2
  }
]
```

## Status Codes

- `200 OK` - Successful GET request
- `201 Created` - Successful POST request
- `400 Bad Request` - Invalid request data
- `404 Not Found` - Resource not found
- `405 Method Not Allowed` - HTTP method not supported

## Example Usage

### Create a Poll
```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"question_text": "What is your favorite color?", "pub_date": "2025-08-30T22:00:00Z"}' \
http://127.0.0.1:8000/api/polls/
```

### Get All Polls
```bash
curl http://127.0.0.1:8000/api/polls/
```

### Submit a Vote
```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"option_id": 1}' \
http://127.0.0.1:8000/api/polls/1/vote/
```

### View All Votes
```bash
curl http://127.0.0.1:8000/api/votes/
```

## Data Models

### Poll
- `id` - Integer (Primary Key)
- `question_text` - String (max 200 characters)
- `pub_date` - DateTime

### Option
- `id` - Integer (Primary Key)
- `poll` - ForeignKey to Poll
- `option_text` - String (max 200 characters)

### Vote
- `id` - Integer (Primary Key)
- `poll` - ForeignKey to Poll
- `option` - ForeignKey to Option