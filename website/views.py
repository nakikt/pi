from flask import Blueprint,redirect
from .blockchain import Blockchain
from . import blocks, PORT
from flask import jsonify, request
from .models import User
import requests
from .methods import mine_block, New_blockchains
from flask_login import login_user, current_user, login_required


views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
def home():
    response =[]

    response.append(str("Strona startowa - IN PROGRESS"))

    return jsonify(response), 200
#Wyświetla wszystkie książeczki
@views.route("/doctor")
@login_required
def doctor():

    response =[]
    user = User.query.filter_by(id=current_user.id).first()
    if user.role != "A":
        return redirect(url_for("views.home"))
    for block in blocks:
        response.append(str( {
            'id': block.last_block['health_card'][-1]['id'],
            'name_surname': block.last_block['health_card'][-1]['name_surname'],
            'time': block.last_block['timestamp'],
            'birth_date': block.last_block['health_card'][-1]['birth_date'],
            'diseases': block.last_block['health_card'][-1]['diseases'],
            'vaccinations': block.last_block['health_card'][-1]['vaccinations'],
        }))

    return jsonify(response), 200
#Wyświetla wybraną książeczkę zdrowia

@views.route("/patient", methods=['GET'])
@login_required
def patient(id):
    print(current_user)
    response = []
    user = User.query.filter_by(id=current_user.id).first()
    id = user.blockchain_id
    response.append(str({
        'id': blocks[id].last_block['health_card'][-1]['id'],
        'name_surname': blocks[id].last_block['health_card'][-1]['name_surname'],
        'time': blocks[id].last_block['timestamp'],
        'birth_date': blocks[id].last_block['health_card'][-1]['birth_date'],
        'diseases': blocks[id].last_block['health_card'][-1]['diseases'],
        'vaccinations': blocks[id].last_block['health_card'][-1]['vaccinations'],
    }))

    return jsonify(response), 200



@views.route("/doctor/<id>", methods=['GET'])
@login_required
def doctor_view(id):
    response = []
    id = int(id)
    response.append(str({
        'id': blocks[id].last_block['health_card'][-1]['id'],
        'name_surname': blocks[id].last_block['health_card'][-1]['name_surname'],
        'time': blocks[id].last_block['timestamp'],
        'birth_date': blocks[id].last_block['health_card'][-1]['birth_date'],
        'diseases': blocks[id].last_block['health_card'][-1]['diseases'],
        'vaccinations': blocks[id].last_block['health_card'][-1]['vaccinations'],
    }))

    return jsonify(response), 200

@views.route("/doctor/<id>/edit", methods=['GET', 'POST'])
@login_required
def doctor_edit(id):
    # get the value passed in from the client
    values = request.get_json()
    # check that the required fields are in the POST'ed data
    required_fields = ['id','name_surname', 'birth_date', 'diseases', 'vaccinations']
    if not all(k in values for k in required_fields):
        return ('Missing fields', 400)
    # create a new transaction
    id = int(values['id'])
    if not blocks[id].valid_new(id):
        response = str({
            'Message: The validity of the block was checked by other nodes and rejected.'
        })
        print('The validity of the block was checked by other nodes and rejected.')
        return (jsonify(response), 201)
    print('The validity of the block was checked by other nodes')
    try:
        mine_block(blocks[id], values['id'], values['name_surname'], values['birth_date'], values['diseases'], values['vaccinations'])
        print('Block was mined to the blockchain')
    except:
        print('Failed to add block to blockchain')
    try:
        neighbours = blocks[int(id)].nodes
        for node in neighbours:
            # blocks[id].update_blockchain(id)
            requests.get(f'http://{node}//nodes/sync/{id}')

    except:
        print("Problem with sync")
    response = str({'Block was successfully added'})
    return (jsonify(response), 201)





