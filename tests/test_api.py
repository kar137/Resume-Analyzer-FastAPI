import pytest

def test_upload_resume(client):
    test_file = ("test_resume.pdf", open("tests/test_resume.pdf", "rb"))
    
    response = client.post(
        "/upload",
        files={"file": test_file}
    )
    
    assert response.status_code == 200
    assert "id" in response.json()
    
    analysis_id = response.json()["id"]
    
    # Test getting result
    response = client.get(f"/result/{analysis_id}")
    assert response.status_code == 200
    assert response.json()["status"] in ["processing", "completed"]