from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board

# example_bp = Blueprint('example_bp', __name__)

boards_bp = Blueprint('boards_bp', __name__, url_prefix='/boards')

@boards_bp.route('', methods=['GET'])
def read_boards():
  boards = Board.query.all()

  boards_response = []
  for board in boards:
    boards_response.append(
      {
        # change 'id' to 'board_id'
        "board_id": board.board_id,
        "title": board.title,
        "owner": board.owner
      }
    )
  return jsonify(boards_response)


#lets try to search by title rather than id
@boards_bp.route('/<board_id>', methods=['GET'])
def read_one_board(board_id):
  board_id = int(board_id)
  board = Board.query.get(board_id)

  return{
      "board_id": board.board_id,
      "title": board.title,
      "owner": board.owner
  }


@boards_bp.route('', methods=['POST'])
def create_board():
  request_body = request.get_json()
  new_board = Board(
    title=request_body["title"],
    owner=request_body["owner"]
  )
  db.session.add(new_board)
  db.session.commit()

  return make_response(jsonify(f"Board {new_board.title} successfully created"), 201)
