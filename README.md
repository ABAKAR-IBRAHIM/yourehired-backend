# JobSpy FastAPI Application

A FastAPI application that provides a REST API for the JobSpy library to scrape job postings from multiple job boards.

## Features

- 🚀 FastAPI framework for high performance
- 🐳 Fully dockerized with Docker Compose
- �� Scrapes from LinkedIn, Indeed, Glassdoor, ZipRecruiter, Google Jobs, Bayt, and Naukri
- 🔍 Advanced search filtering options
- 📝 Automatic API documentation (Swagger/ReDoc)
- 🏥 Health checks and monitoring
- 🔒 CORS enabled for web applications
- 📈 Structured logging

## Quick Start

### Using Docker Compose (Recommended)

1. **Clone and navigate to the project:**

   ```bash
   cd jobspy-api
   ```

2. **Build and run:**

   ```bash
   docker-compose up --build
   ```

3. **Access the API:**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

### Manual Setup

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## API Endpoints

### Advanced Search

```bash
POST /search
```

Example request body:

```json
{
  "search_term": "software engineer",
  "location": "San Francisco, CA",
  "site_name": ["indeed", "linkedin"],
  "results_wanted": 20,
  "job_type": "fulltime",
  "hours_old": 24,
  "is_remote": true
}
```

### Other Endpoints

- `GET /` - Health check
- `GET /health` - Detailed health status
- `GET /sites` - List supported job sites

## Usage Examples

### 1. Advanced Search via cURL

```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{
    "search_term": "data scientist",
    "location": "Remote",
    "site_name": ["linkedin", "indeed"],
    "results_wanted": 15,
    "job_type": "fulltime",
    "is_remote": true
  }'
```

### 2. Python Client Example

```python
import requests

# Advanced search
response = requests.post(
    "http://localhost:8000/search",
    json={
        "search_term": "frontend developer",
        "location": "Austin, TX",
        "site_name": ["indeed", "glassdoor"],
        "results_wanted": 25,
        "job_type": "fulltime",
        "hours_old": 48
    }
)
jobs = response.json()
```

## Configuration

### Environment Variables

- `ENVIRONMENT`: development/production
- `LOG_LEVEL`: INFO/DEBUG/WARNING/ERROR
- `API_PORT`: Port to run the API (default: 8000)
- `API_HOST`: Host to bind (default: 0.0.0.0)

### Docker Compose Profiles

- Default: Runs only the API
- Production: `docker-compose --profile production up` (includes Nginx)

## Production Deployment

### With Nginx (Recommended)

```bash
docker-compose --profile production up --build -d
```

### Scaling

```bash
docker-compose up --scale jobspy-api=3 -d
```

## Supported Job Sites

| Site         | Code            | Global | Notes                     |
| ------------ | --------------- | ------ | ------------------------- |
| LinkedIn     | `linkedin`      | ✅     | Rate limited, use proxies |
| Indeed       | `indeed`        | ✅     | Best performance          |
| Glassdoor    | `glassdoor`     | ✅     | Requires country_indeed   |
| ZipRecruiter | `zip_recruiter` | 🇺🇸🇨🇦   | US/Canada only            |
| Google Jobs  | `google`        | ✅     | Requires specific syntax  |
| Bayt         | `bayt`          | 🌍     | Middle East focus         |
| Naukri       | `naukri`        | 🇮🇳     | India focus               |

## Troubleshooting

### Common Issues

1. **Rate Limiting (429 errors):**

   - Add delays between requests
   - Use proxy servers
   - Reduce results_wanted

2. **No results from Google:**

   - Use very specific search terms
   - Copy search syntax from Google Jobs directly

3. **LinkedIn blocking:**
   - Use proxies
   - Reduce frequency
   - Set linkedin_fetch_description=false

### Logs

```bash
docker-compose logs -f jobspy-api
```

## License

MIT License - see LICENSE file for details.
