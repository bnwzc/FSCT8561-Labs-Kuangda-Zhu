import requests
import csv

def get_home(base_url):
    try:
        r = requests.get(base_url + "/", timeout=5)
        observation = {
            "endpoint": "/",
            "HTTP method": "GET",
            "input/payload": None,
            "status_code": r.status_code,
            "response_length": len(r.content),
            "content_type": r.headers.get("Content-Type"),
            "server": r.headers.get("Server")
        }
        print(f"Requested URL: {r.url}")
        print(f"Status: {r.status_code}")
        print(f"Response Length: {len(r.content)}")
        print(f"Content-Type: {r.headers.get('Content-Type')}")
        print("-" * 40)
    except:
        print("Some errors exsist")
        observation = {
            "endpoint": "/",
            "HTTP method": "GET",
            "input/payload": "ERROR",
            "status_code": "ERROR",
            "response_length": "ERROR",
            "content_type": "ERROR",
            "server": "ERROR"
        }
    return observation

def get_search(base_url, search_words:list):
    search_url = base_url + "/rest/products/search"
    observation = []
    for word in search_words:
        try:
            r = requests.get(search_url, params={"q": word}, timeout=5)
            observation.append(
                {
                "endpoint": "/rest/products/search",
                "HTTP method": "GET",
                "input/payload": str({"q": word}),
                "status_code": r.status_code,
                "response_length": len(r.content),
                "content_type": r.headers.get("Content-Type"),
                "server": r.headers.get("Server")
            }    
            )
            print(f"Requested URL: {r.url}")
            print(f"Status: {r.status_code}")
            print(f"Response Length: {len(r.content)}")
            print(f"Content-Type: {r.headers.get('Content-Type')}")
            print("-" * 40)
        except:
            print("Some errors exsist")
            observation.append(
                {
                "endpoint": "/rest/products/search",
                "HTTP method": "GET",
                "input/payload": "ERROR",
                "status_code": "ERROR",
                "response_length": "ERROR",
                "content_type": "ERROR",
                "server": "ERROR"
            }
            )
        
    return observation

def post_home(base_url):
    try:
        r = requests.post(base_url + "/rest/products/search", timeout=5)
        observation = {
            "endpoint": "/",
            "HTTP method": "POST",
            "input/payload": None,
            "status_code": r.status_code,
            "response_length": len(r.content),
            "content_type": r.headers.get("Content-Type"),
        }
        print(f"Requested URL: {r.url}")
        print(f"Status: {r.status_code}")
        print(f"Response Length: {len(r.content)}")
        print(f"Content-Type: {r.headers.get('Content-Type')}")
        print("-" * 40)
    except:
        print("Some errors exsist")
        observation = {
            "endpoint": "/",
            "HTTP method": "POST",
            "input/payload": "ERROR",
            "status_code": "ERROR",
            "response_length": "ERROR",
            "content_type": "ERROR",
            "server": "ERROR"
        }
        
    return observation    

if __name__ == "__main__":
    
    base_url = "http://localhost:3000"
    records = []
    records.append(get_home(base_url))
    
    for i in get_search(base_url, ["apple", "banana", "chocolate"]):
        records.append(i)
    records.append(post_home(base_url))
    
    with open("http_scan_results.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)

    print("Saved http_scan_results.csv")
    
