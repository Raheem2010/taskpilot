BACKEND_BASE_URL = "http://localhost:8000"
API_PREFIX = "/api/v1"


def get_full_url(path: str) -> str:
    path = path.lstrip("/")

    # Health is a root-level endpoint: GET /health
    if path == "health":
        return f"{BACKEND_BASE_URL}/health"

    prefix = API_PREFIX.strip("/")
    if prefix:
        return f"{BACKEND_BASE_URL}/{prefix}/{path}"

    return f"{BACKEND_BASE_URL}/{path}"
