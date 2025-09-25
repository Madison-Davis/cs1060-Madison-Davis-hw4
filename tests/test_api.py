import requests

# Code obtained from ChatGPT site, personal login

BASE_URL = "http://127.0.0.1:5000"

def test_coffee_teapot():
    resp = requests.post(f"{BASE_URL}/county_data", json={"coffee": "teapot"})
    assert resp.status_code == 418, f"Expected 418, got {resp.status_code}"
    print("PASS: coffee=teapot, returns 418")

def test_missing_zip_or_measure():
    resp = requests.post(f"{BASE_URL}/county_data", json={"measure_name": "Adult obesity"})
    assert resp.status_code == 400, f"Expected 400, got {resp.status_code}"
    print("PASS: missing ZIP from POST request, returns 400")

    resp = requests.post(f"{BASE_URL}/county_data", json={"zip": "02138"})
    assert resp.status_code == 400, f"Expected 400, got {resp.status_code}"
    print("PASS: missing measure_name from POST request, returns 400")

def test_nonexistent_data():
    resp = requests.post(
        f"{BASE_URL}/county_data", 
        json={"zip": "99999", "measure_name": "Adult obesity"}
    )
    assert resp.status_code == 404, f"Expected 404, got {resp.status_code}"
    print("PASS: requested for a nonexistent ZIP, returns 404")

    resp = requests.post(
        f"{BASE_URL}/county_data", 
        json={"zip": "02138", "measure_name": "Fake measure"}
    )
    assert resp.status_code == 404, f"Expected 404, got {resp.status_code}"
    print("PASS: requested for a nonexistent measure_name, returns 404")

def test_wrong_endpoint():
    resp = requests.post(f"{BASE_URL}/fake_endpoint", json={"zip":"02138","measure_name":"Adult obesity"})
    assert resp.status_code == 404, f"Expected 404, got {resp.status_code}"
    print("PASS: requested for endpoint other than county_data, returns 404")

if __name__ == "__main__":
    test_coffee_teapot()
    test_missing_zip_or_measure()
    test_nonexistent_data()
    test_wrong_endpoint()
    print("All tests passed!")
