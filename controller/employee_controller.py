from flask import Blueprint, request, make_response, send_file
from models.all_model import Employee
from extensions.sqlalchemy_extensions import db
from datetime import datetime

emp_api = Blueprint("emp_api", __name__)

# Get all item method
@emp_api.route('/', methods=["GET"])
def getallemployee():
    data = Employee.query.all()
    response = []
    for emp in data:
        emp_data = {}
        emp_data['emp_id'] = emp.emp_id
        emp_data["emp_name"] = emp.emp_name
        emp_data["emp_email"] = emp.emp_email
        emp_data["avatar"] = emp.avatar
        response.append(emp_data)

    if len(response) > 0:
        res = make_response({'payload' : response}, 200)
        # allowing cross origin http requests
        # res.headers['Access-Control-Allow-Origin'] = "*"
        return res
    else:
        return make_response({"message" : "No data found"}, 204)
# Get single item method
@emp_api.route('/<int:employee_id>', methods=['GET'])
def getsingleemplyeedata(employee_id):
    data = Employee.query.filter_by(emp_id=employee_id).first()
    if not data:
        return make_response({"message" : "No data found"}, 204)
    emp_data = {}
    emp_data['emp_id'] = data.emp_id
    emp_data["emp_name"] = data.emp_name
    emp_data["emp_email"] = data.emp_email
    emp_data["avatar"] = data.avatar
    return make_response({"payload" : emp_data}, 200)

# Post Method
@emp_api.route('/post/<int:employee_id>', methods=["POST"])
def insertemployeetodb(employee_id):
    data = Employee.query.filter_by(emp_id=employee_id).first()
    if data:
        make_response({"message" : "No data found"}, 204)
    res = request.json
    data = Employee(emp_id=employee_id, emp_name=res['emp_name'], emp_email=res['emp_email'])
    db.session.add(data)
    db.session.commit()
    return make_response({"payload" : res}, 200)

# Put method
@emp_api.route('/update/<employee_id>', methods=["PUT"])
def updateemployeedata(employee_id):
    data = Employee.query.filter_by(emp_id=employee_id).first()
    if not data:
        return make_response({"message" : "No data found"}, 204)
    res = request.json
    data.emp_name = res['emp_name']
    data.emp_email = res["emp_email"]
    db.session.commit()
    return make_response({'payload' : res}, 200)

# Delete method
@emp_api.route('/delete/<employee_id>', methods=["DELETE"])
def deleteemployeedata(employee_id):
    data = Employee.query.get(employee_id)
    if not data:
        return make_response({"message": "No data found"}, 204)
    db.session.delete(data)
    db.session.commit()
    return make_response({"message" : "No data found"}, 200)


# Patch method
@emp_api.route('/patch/<employee_id>', methods=["PATCH"])
def patchemployeedata(employee_id):
    data = Employee.query.get(employee_id)
    # print(data.emp_id, data.emp_name, data.emp_email)
    if not data:
        return make_response({"message" : "Data does not exists"}, 204)
    res = request.json
    for key in res:
        if key == "emp_name":
            data.emp_name = res[key]
        else:
            data.emp_email = res[key]
    db.session.commit()
    return make_response({'payload' : res}, 200)

# Pagination Logic implementation
@emp_api.route('/pagination/limit/<int:limit>/page/<int:page>', methods=["GET"])
def getallpagination(limit, page):
    start_page = (page*limit) - limit
    data = Employee.query.order_by(Employee.emp_id).limit(3)
    response = []
    for emp in data:
        emp_data = {}
        emp_data['emp_id'] = emp.emp_id
        emp_data["emp_name"] = emp.emp_name
        emp_data["emp_email"] = emp.emp_email
        response.append(emp_data)

    if len(response) > 0:
        res = make_response({'payload': response}, 200)
        return res
    else:
        return make_response({"message": "No data found"}, 204)


# File uploading
@emp_api.route('/upload/avatar/<employee_id>', methods=["PUT"])
def uploademployeeavatar(employee_id):
    file = request.files['avatar']
    unique_name = str(datetime.now().timestamp()).replace(".","")
    lst_filename = (file.filename).split(".")
    ext = lst_filename[-1]
    final_file_path = f"uploads/{unique_name}.{ext}"
    file.save(final_file_path)
    data = Employee.query.filter_by(emp_id=employee_id).first()
    if not data:
        return make_response({"message" : "Data not exists"}, 204)

    data.avatar = final_file_path
    db.session.commit()
    return {"message" : "Avatar has been saved successfully"}

@emp_api.route('/upload/<filename>')
def getuploadedavatar(filename):
    # data = Employee.query.filter_by(emp_id=employee_id).first()
    # filepath = data.avatar
    return send_file(f"uploads/{filename}")