# tests/test_api.py
import pytest

def test_upload_and_get_result(client):
    # Use context manager to ensure the file is closed after the test
    test_file_path = "tests/test_resume.pdf"

    with open(test_file_path, "rb") as f:
        response = client.post(
            "/upload",
            files={"file": ("test_resume.pdf", f, "application/pdf")},
        )

    # Assert upload was successful
    assert response.status_code == 200
    data = response.json()
    assert "id" in data

    analysis_id = data["id"]

    # Now test retrieving the analysis result
    response = client.get(f"/result/{analysis_id}")
    assert response.status_code == 200

    result_data = response.json()
    assert result_data["status"] in ["processing", "completed"]
