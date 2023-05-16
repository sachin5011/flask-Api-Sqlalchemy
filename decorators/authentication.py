import json
from functools import wraps

from flask import request, make_response
import re
import jwt
from extensions.sqlalchemy_extensions import db



def token_required(endpoint=""):
    def inner1(func):
        @wraps(func)
        def inner2(*args):
            endpoint = request.url_rule
            try:
                auth = request.headers.get("Authorization")
                if re.match("^Bearer *([^ ]+) *$", auth, flags=0):
                    token = auth.split(" ")[1]
                    try:
                        decoded_token = jwt.decode(token, "secret", algorithms="HS256")
                    except jwt.ExpiredSignatureError:
                        return make_response({"ERROR" : "TOKEN EXPIRED" }, 401)
                    role_id = decoded_token['role_id']
                    accessbility_view = db.Table("accessbility_view", db.metadata, autoload_with=db.engine)
                    data = db.session.query(accessbility_view).filter_by(endpoints=endpoint).first()
                    if len(data.roles)>0:
                        print(data.roles)
                        roles_allowed = data[0]['roles']
                        if role_id in roles_allowed:
                            return func(*args)
                        else:
                            return make_response({"Error" : "Invalid Role"})
                    else:
                        return make_response({"Error" : "Unknown Endpoint"})
                else:
                    return make_response({"message" : "Invalid Token"}, 401)

            except Exception as e:
                    return make_response({"ERROR":str(e)}, 401)

        return inner2

    return inner1