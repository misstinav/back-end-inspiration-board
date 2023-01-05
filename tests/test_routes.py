from app.models.board import Board
import pytest

def test_get_empty_board_list(client):
  #arrange
  #act
  response = client.get("/boards")
  response_body = response.get_json()
  #assert
  assert response.status_code == 200
  assert response_body == []