from flask import Blueprint, make_response, request, send_file
from extensions.sqlalchemy_extensions import db
from models.all_model import User, Endpoint
from datetime import datetime, timedelta
import jwt
from decorators.authentication import token_required


user_api = Blueprint("user_api", __name__)


@user_api.route('/users/getall', methods=['GET'])
# @token_required('/users/getall')
def getallusers():
    user_data = User.query.all()
    response = []
    for data in user_data:
        user_dict = {}
        user_dict['id'] = data.id
        user_dict['name'] = data.name
        user_dict['email'] = data.email
        user_dict['phone'] = data.phone
        user_dict['password'] = data.password
        user_dict['role'] = data.role
        user_dict['avatar'] = data.avatar
        user_dict['role_id'] = data.role_id
        response.append(user_dict)
    if len(response) < 1:
        return make_response({"message" : "No users in database"}, 204)
    return make_response({"payload" : response}, 200)

@user_api.route('/users/post/<int:uid>', methods=["POST"])
def postuserdatatodb(uid):
    user_data = User.query.filter_by(id=uid).first()
    if user_data:
        return make_response({"message" : "User already exists in database"}, 201)
    response = request.json
    save_user = User(id=uid, name=response['name'], email=response['email'], phone=response['phone'],
                     role=response['role'], password=response['password'], avatar=response['avatar'], role_id=response['role_id'])
    db.session.add(save_user)
    db.session.commit()
    return make_response({"payload" : response}, 200)

@user_api.route("/endpoints/<eid>", methods=["POST"])
@token_required()
def addendpointstodb(eid):
    end_data = Endpoint.query.filter_by(id=eid).first()
    if end_data:
        return make_response({"message" : "Endpoint already exist"}, 204)
    response = request.json
    save_endpoint = Endpoint(endpoints=response['endpoints'], method=response['method'])
    db.session.add(save_endpoint)
    db.session.commit()
    return make_response({"payload" : response}, 200)

@user_api.route('/users/put/<uid>', methods=["PUT"])
def putuserdatatodb(uid):
    user_data = User.query.filter_by(id=uid).first()
    if not user_data:
        return make_response({"message"  : "No user found"}, 204)
    response = request.json
    user_data.name = response['name']
    user_data.email = response['email']
    user_data.phone = response['phone']
    user_data.password = response['password']
    user_data.role = response['role']
    user_data.avatar = response['avatar']
    user_data.role_id = response['role_id']
    db.session.commit()
    return make_response({"payload": response}, 200)

@user_api.route("/users/patch/<uid>", methods=["PATCH"])
def patchuserdata(uid):
    user_data = User.query.get(uid)
    response = request.json
    for key in response:
        if key == "name":
            user_data.name = response[key]
        elif key == "email":
            user_data.email = response[key]
        elif key == "password":
            user_data.password = response[key]
        elif key == "phone":
            user_data.phone = response[key]
        elif key == "role":
            user_data.role = response[key]
        elif key == "avatar":
            user_data.avatar = response[key]
        elif key == 'role_id':
            user_data.role_id = response[key]
    db.session.commit()
    return make_response({'payload' : response}, 200)

@user_api.route('/users/delete/<uid>', methods=["DELETE"])
# @authentication('/users/delete/<uid>')
def deleteuserfromdb(uid):
    user_data = User.query.get(uid)
    if not user_data:
        return make_response({"message" : "User does not exists in database"}, 204)
    db.session.delete(user_data)
    db.session.commit()
    return make_response({'message' : "User has been successfully deleted"}, 200)

@user_api.route('/users/avatar/<uid>', methods=["PUT"])
def setavatarforuser(uid):
    file = request.files['avatar']
    unique_name = str(datetime.now().timestamp()).replace(".", "")
    lst_filename = (file.filename).split(".")
    ext = lst_filename[-1]
    final_file_path = f"uploads/users/{unique_name}.{ext}"
    file.save(final_file_path)
    user_data = User.query.filter_by(id=uid).first()
    if not user_data:
        return make_response({'message' : "Data does not exists"}, 204)
    user_data.avatar = final_file_path
    db.session.commit()
    return make_response({"message" : "Avatar saved"}, 200)

@user_api.route("/users/avatar/<filename>")
def getavatarfromdatabase(filename):
    return send_file(f"uploads/users/{filename}")


# User authorization
@user_api.route("/users/login", methods=["POST"])
def userlogin():
    response = request.json
    username = response['email']
    password = response['password']
    print(username, password)
    login_data =  User.query.filter_by(email=username).first()
    # print(login_data.email, login_data.password)
    exp_time = datetime.now() + timedelta(minutes=15)
    exp_epoc_time = int(exp_time.timestamp())
    payload = {
        "username" : login_data.email,
        'password' : login_data.password,
        "role_id" : login_data.role_id,
        "exp" : exp_epoc_time
    }
    token = jwt.encode(payload, "secret", algorithm="HS256")
    return make_response({"token" : token}, 200)

@user_api.route("/users/addmultiple", methods=["POST"])
def addmultipleusers():
    data = request.json
    for userdata in data:
        save_user = User(id=userdata["id"], name=userdata['name'], email=userdata['email'], phone=userdata['phone'],
                         role=userdata['role'], password=userdata['password'], avatar=userdata['avatar'],
                         role_id=userdata['role_id'])
        db.session.add(save_user)
        db.session.commit()
    return make_response({"Message" : "All Data Inserted Successfully"})

# @user_api.route("/users/test", methods=["GET"])
# # @authentication("/users/test")
# def testdata():
#     accessbility_view = db.Table("accessbility_view", db.metadata, autoload_with=db.engine)
#     data = db.session.query(accessbility_view).filter_by(endpoints='/users/post/<uid>').first()
#     print(data.roles)
#     # response = []
#     # for d in data:
#     #     d_dict = {}
#     #     d_dict['endpoints'] = d.endpoints
#     #     d_dict["roles"] = d.roles
#     #     response.append(d_dict)
#     return make_response({"payload" : "Success"}, 200)