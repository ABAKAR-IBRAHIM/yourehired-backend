from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
import pandas as pd
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="JobSpy API",
    description="Production-ready API for scraping jobs using JobSpy library",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models
class JobSearchRequest(BaseModel):
    site_name: Optional[List[str]] = Field(
        default=["indeed", "linkedin", "glassdoor"],
        description="Job sites to search: linkedin, indeed, glassdoor, zip_recruiter, google, bayt, naukri",
    )
    search_term: Optional[str] = Field(default=None, description="Job search term")
    google_search_term: Optional[str] = Field(
        default=None,
        description="Specific search term for Google Jobs (required for Google)",
    )
    location: Optional[str] = Field(default=None, description="Job location")
    results_wanted: Optional[int] = Field(
        default=20, ge=1, le=1000, description="Number of results per site (max 1000)"
    )
    hours_old: Optional[int] = Field(
        default=None, description="Filter jobs by hours since posted"
    )
    job_type: Optional[str] = Field(
        default=None, description="fulltime, parttime, internship, contract"
    )
    is_remote: Optional[bool] = Field(
        default=None, description="Filter for remote jobs"
    )
    distance: Optional[int] = Field(default=50, description="Search distance in miles")
    country_indeed: Optional[str] = Field(
        default="USA",
        description="Country for Indeed/Glassdoor (see supported countries)",
    )
    easy_apply: Optional[bool] = Field(
        default=None, description="Filter for easy apply jobs"
    )
    description_format: Optional[str] = Field(
        default="markdown", description="markdown or html"
    )
    linkedin_fetch_description: Optional[bool] = Field(
        default=False, description="Fetch full LinkedIn descriptions (slower)"
    )
    linkedin_company_ids: Optional[List[int]] = Field(
        default=None, description="Search specific LinkedIn company IDs"
    )
    offset: Optional[int] = Field(
        default=None,
        description="Start search from offset (e.g. 25 starts from 25th result)",
    )
    enforce_annual_salary: Optional[bool] = Field(
        default=None, description="Convert wages to annual salary"
    )
    proxies: Optional[List[str]] = Field(
        default=None,
        description="List of proxies in format ['user:pass@host:port', 'localhost']",
    )
    ca_cert: Optional[str] = Field(
        default=None, description="Path to CA Certificate file for proxies"
    )
    verbose: Optional[int] = Field(default=1, ge=0, le=2, description="Verbosity level")


class JobSearchResponse(BaseModel):
    success: bool
    total_jobs: int
    jobs: List[Dict[str, Any]]
    search_params: Dict[str, Any]
    execution_time: float
    message: str


class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: str


# Utility functions
def convert_dataframe_to_dict(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Convert pandas DataFrame to list of dictionaries"""
    df = df.where(pd.notnull(df), None)
    return df.to_dict("records")


def clean_search_params(params: Dict[str, Any]) -> Dict[str, Any]:
    """Remove None values and clean parameters"""
    return {k: v for k, v in params.items() if v is not None}


# Routes
@app.get("/", response_model=HealthResponse)
async def root():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy", version="1.0.0", timestamp=datetime.now().isoformat()
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Detailed health check"""
    return HealthResponse(
        status="healthy", version="1.0.0", timestamp=datetime.now().isoformat()
    )


@app.post("/search", response_model=JobSearchResponse)
async def search_jobs(request: JobSearchRequest):
    """Search for jobs using JobSpy library"""
    try:
        from jobspy import scrape_jobs

        start_time = time.time()
        search_params = clean_search_params(request.model_dump())

        logger.info(f"Starting job search: {search_params}")

        # Perform job search
        jobs_df = scrape_jobs(**search_params)
        jobs_list = convert_dataframe_to_dict(jobs_df)

        execution_time = time.time() - start_time

        logger.info(f"Found {len(jobs_list)} jobs in {execution_time:.2f} seconds")

        return JobSearchResponse(
            success=True,
            total_jobs=len(jobs_list),
            jobs=jobs_list,
            search_params=search_params,
            execution_time=execution_time,
            message=f"Successfully found {len(jobs_list)} jobs",
        )

    except ImportError as e:
        logger.error(f"JobSpy import error: {e}")
        raise HTTPException(status_code=500, detail="JobSpy library not available")
    except Exception as e:
        logger.error(f"Job search error: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@app.get("/sites")
async def get_supported_sites():
    """Get comprehensive information about supported job sites and parameters"""
    return {
        "supported_sites": [
            "linkedin",
            "indeed",
            "glassdoor",
            "zip_recruiter",
            "google",
            "bayt",
            "naukri",
        ],
        "job_types": ["fulltime", "parttime", "internship", "contract"],
        "description_formats": ["markdown", "html"],
        "supported_countries": {
            "indeed_glassdoor": [
                "Argentina",
                "Australia",
                "Austria",
                "Bahrain",
                "Belgium",
                "Brazil",
                "Canada",
                "Chile",
                "China",
                "Colombia",
                "Costa Rica",
                "Czech Republic",
                "Denmark",
                "Ecuador",
                "Egypt",
                "Finland",
                "France",
                "Germany",
                "Greece",
                "Hong Kong",
                "Hungary",
                "India",
                "Indonesia",
                "Ireland",
                "Israel",
                "Italy",
                "Japan",
                "Kuwait",
                "Luxembourg",
                "Malaysia",
                "Mexico",
                "Morocco",
                "Netherlands",
                "New Zealand",
                "Nigeria",
                "Norway",
                "Oman",
                "Pakistan",
                "Panama",
                "Peru",
                "Philippines",
                "Poland",
                "Portugal",
                "Qatar",
                "Romania",
                "Saudi Arabia",
                "Singapore",
                "South Africa",
                "South Korea",
                "Spain",
                "Sweden",
                "Switzerland",
                "Taiwan",
                "Thailand",
                "Turkey",
                "Ukraine",
                "United Arab Emirates",
                "UK",
                "USA",
                "Uruguay",
                "Venezuela",
                "Vietnam",
            ],
            "linkedin": "Global (uses location parameter)",
            "zip_recruiter": "US/Canada only",
            "bayt": "International",
            "google": "Global (requires google_search_term)",
            "naukri": "India focused",
        },
        "limitations": {
            "indeed": "Only one of: hours_old, (job_type & is_remote), easy_apply",
            "linkedin": "Only one of: hours_old, easy_apply. Rate limited ~10 pages per IP",
            "google": "Requires specific google_search_term syntax",
            "general": "All sites capped at ~1000 jobs per search",
        },
        "tips": {
            "indeed_search": "Use quotes for exact match, - to exclude, OR for alternatives. Example: '\"engineering intern\" software summer (java OR python OR c++) 2025 -tax -marketing'",
            "google_search": "Copy exact search from Google Jobs browser after applying filters",
            "rate_limiting": "Use proxies for LinkedIn, wait between scrapes, Indeed has no rate limiting",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
