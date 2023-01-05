from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card

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
# @boards_bp.route('/<board_id>', methods=['GET'])
# def read_one_board(board_id):
#   board_id = int(board_id)
#   board = Board.query.get(board_id)

#   return{
#       "board_id": board.board_id,
#       "title": board.title,
#       "owner": board.owner
#   }

# get one board by title instead of id
@boards_bp.route('/<title>', methods=['GET'])
def read_one_board(title):
  boards = Board.query.all()
  for board in boards:
    if board.title == title:
      return {
        "board_id": board.board_id,
        "title": board.title,
        "owner": board.owner
      }
  else:
    return f"Board {title} not found!"

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





########################## CARD ROUTES ###################################

# card_routes
cards_bp = Blueprint('cards_bp', __name__, url_prefix='/cards')

# DELETE card
@cards_bp.route('/<card_id>', methods=['DELETE'])
def delete_card(card_id):
  card_id = int(card_id)

  db.session.delete(card_id)
  db.session.commit()

@boards_bp.route('/<board_id>/cards', methods=['POST'])
def create_card(board_id):
  request_body = request.get_json()
  
  boards = Board.query.all()
  new_card = Card(
    message=request_body["message"],
    likes_count=request_body["likes_count"]
  )
  for board in boards:
    if board.board_id == int(board_id):
      board.cards.append(new_card)
  
  db.session.add(new_card)
  db.session.commit()

  return make_response(jsonify(f"Card message {new_card.message} successfully created"), 201)


@boards_bp.route('/<board_id>/cards/<card_id>', methods=["PUT"])
def update_liked_card(card_id):
  card = Card.query.get(int(card_id))

  request_body = request.get_json()
  card.likes_count = request_body["likes_count"]

  db.session.commit()

  return make_response("Card like count has been updated successfully")

# read all cards from one board
@boards_bp.route('/<board_id>/cards', methods=['GET'])
def read_cards(board_id):
  cards = Card.query.all()

  cards_response = []
  for card in cards:
    if card.board_id == board_id:
      cards_response.append(
        {
          "card_id": card.card_id,
          "message": card.message,
          "likes_count": card.likes_count
        }
      )
  return jsonify(cards_response)
