from crewai_tools import BaseTool
import requests
from requests.structures import CaseInsensitiveDict

class HttpRequesterTool(BaseTool):
    name: str = "Execute HTTP requests"
    description: str = (
        "Execute the given HTTP request and return the response."
    )

    def _run(self, raw_request: str) -> str:
        response = execute_raw_request(raw_request)
        return response


# Parse the raw request
def parse_raw_request(raw_request):
    lines = raw_request.strip().split('\n')
    method, path, _ = lines[0].split()
    headers = CaseInsensitiveDict()
    for line in lines[1:]:
        if line.strip():
            key, value = line.split(':', 1)
            headers[key.strip()] = value.strip()
    return method, path, headers

# Execute the request
def execute_raw_request(raw_request):
    method, path, headers = parse_raw_request(raw_request)
    url = f"http://{headers['Host']}{path}"
    response = requests.request(method, url, headers=headers)
    return response