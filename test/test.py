import os


async def test_middleware(async_client):
    response = await async_client.get(url=f"/middleware/")
    assert response.status_code == 200
    assert response.json() == {"message": "Middleware is working"}
    assert response.headers["x-method"] == "It was request GET method."


async def test_create_author(
                                async_client,
                                data_test_create_author):
    response = await async_client.post(
                                        url=f"/author/",
                                        json=data_test_create_author)
    response_json = response.json()
    assert response_json["name"] == data_test_create_author["name"]
    assert response_json["pseudo"] == data_test_create_author["pseudo"]
    assert response_json["city"] == data_test_create_author["city"]
    assert response.status_code == 201
    os.environ["ID"] = str(response_json["id"])


async def test_update_author(
                                async_client,
                                data_test_create_author,
                                data_test_update_author):
    id = os.environ["ID"]
    response = await async_client.put(
                                        url=f"/author/{id}/",
                                        json=data_test_update_author)
    response_json = response.json()
    assert response_json["name"] == data_test_create_author["name"]
    assert response_json["pseudo"] == data_test_update_author["pseudo"]
    assert response_json["city"] == data_test_create_author["city"]
    assert response.status_code == 200


async def test_retrive_author(async_client):
    id = os.environ["ID"]
    response = await async_client.get(
                                        url=f"/author/{id}/")
    response_json = response.json()
    assert response_json["id"] == int(id)
    assert response.status_code == 200


async def test_list_author(async_client):
    response = await async_client.get(
                                        url=f"/author/")
    assert response.status_code == 200


async def test_delete_author(async_client):
    id = os.environ["ID"]
    response = await async_client.delete(
                                        url=f"/author/{id}/")
    assert response.status_code == 204
