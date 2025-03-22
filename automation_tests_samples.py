# automation_tests_samples.py

import logging
from typing import Dict

import pytest
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
LOGGER = logging.getLogger()

BASE_URL = "https://jsonplaceholder.typicode.com"


@pytest.fixture(scope="module")
def test_data() -> Dict[str, str]:
    """
    Fixture to provide test data for the tests.

    :return: A dictionary containing test data for creating a post.
    """
    return {"title": "foo", "body": "bar", "userId": "1"}


def test_get_posts() -> None:
    """
    Test to validate fetching posts.

    Sends a GET request to the /posts endpoint and checks if the response status code is 200.
    Also verifies that the response is a list and logs the number of items returned.
    """
    response = requests.get(f"{BASE_URL}/posts")
    assert response.status_code == 200, "Failed to fetch posts"
    assert isinstance(response.json(), list), "Response is not a list"
    LOGGER.info("GET /posts returned %d items", len(response.json()))


def test_create_post(test_data: dict) -> None:
    """
    Test to validate creating a post.

    Sends a POST request to the /posts endpoint with the provided test data and
    checks if the response status code is 201. Also verifies that the title in
    the response matches the title in the test data and logs the ID of the created post.

    :param test_data: A dictionary containing the data for the new post.
    """
    response = requests.post(f"{BASE_URL}/posts", json=test_data)
    assert response.status_code == 201, "Failed to create post"
    assert response.json().get("title") == test_data["title"], "Title mismatch"
    LOGGER.info("POST /posts created a post with ID %s", response.json().get("id"))


def test_update_post() -> None:
    """
    Test to validate updating a post.

    Sends a PATCH request to the /posts/1 endpoint with the update data and
    checks if the response status code is 200. Also verifies that the title
    in the response matches the updated title and logs the update.
    """
    update_data = {"title": "updated title"}
    response = requests.patch(f"{BASE_URL}/posts/1", json=update_data)
    assert response.status_code == 200, "Failed to update post"
    assert response.json().get("title") == update_data["title"], "Update failed"
    LOGGER.info("PATCH /posts/1 updated the title")


def test_delete_post() -> None:
    """
    Test to validate deleting a post.

    Sends a DELETE request to the /posts/1 endpoint and checks if the response status code is 200.
    Logs the successful execution of the delete request.
    """
    response = requests.delete(f"{BASE_URL}/posts/1")
    assert response.status_code == 200, "Failed to delete post"
    LOGGER.info("DELETE /posts/1 executed successfully")


if __name__ == "__main__":
    pytest.main(["-v", "--tb=short", "--maxfail=1"])
