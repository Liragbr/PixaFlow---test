import pytest
from fastapi.testclient import TestClient
from main import app 

client = TestClient(app)

@pytest.fixture
def sample_task():
    return {
        "titulo": "Tarefa de Teste",
        "descricao": "Esta é uma tarefa criada para testes unitários.",
        "estado": "pendente"
    }

def test_create_task(sample_task):
    response = client.post("/tasks", json=sample_task)
    assert response.status_code == 201
    data = response.json()
    assert data["titulo"] == sample_task["titulo"]
    assert data["descricao"] == sample_task["descricao"]
    assert data["estado"] == sample_task["estado"]
    assert "id" in data

def test_list_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_task_by_id(sample_task):
    create_response = client.post("/tasks", json=sample_task)
    task_id = create_response.json()["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["titulo"] == sample_task["titulo"]
    assert data["descricao"] == sample_task["descricao"]

def test_update_task(sample_task):

    create_response = client.post("/tasks", json=sample_task)
    task_id = create_response.json()["id"]

    updated_task = {
        "titulo": "Tarefa Atualizada",
        "descricao": "Descrição atualizada.",
        "estado": "em andamento"
    }

    # Atualizar a tarefa
    response = client.put(f"/tasks/{task_id}", json=updated_task)
    assert response.status_code == 200
    data = response.json()
    assert data["titulo"] == updated_task["titulo"]
    assert data["descricao"] == updated_task["descricao"]
    assert data["estado"] == updated_task["estado"]

def test_delete_task(sample_task):
  
    create_response = client.post("/tasks", json=sample_task)
    task_id = create_response.json()["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204

    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404
