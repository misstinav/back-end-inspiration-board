from app.models.board import Board
import pytest

# https://stackoverflow.com/questions/37307346/is-the-server-running-on-host-localhost-1-and-accepting-tcp-ip-connections

def test_get_empty_board_list(client):
  #arrange
  #act
  response = client.get("/boards")
  response_body = response.get_json()
  #assert
  assert response.status_code == 200
  assert response_body == []

def test_update_board(client, one_board):
  #act
  response = client.put("/boards/1", json={
    "title": "Updated board title",
    "owner": "Serilla"})
  response_body = response.get_json()

  #assert
  assert response.status_code == 200
  assert response_body == "Board has been updated"
  board = Board.query.get(1)
  assert board.title == "Updated board title"
  assert board.owner == "Serilla"