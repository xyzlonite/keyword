from dotenv import load_dotenv
from flask import Flask, jsonify, request

from api.api2 import get_driver

# from flask_cors import CORS


# .env 파일에서 환경 변수 로드
load_dotenv()

app = Flask(__name__)

# CORS 설정
# CORS(app)


@app.route("/", methods=["GET"])
def index():
    return "Hello World!"


@app.route("/find", methods=["GET"])
def find():
    # Get
    user_id = request.args.get("user_id")
    user_pw = request.args.get("user_pw")
    keyword = request.args.get("keyword")

    data = {}

    data["user_id"] = user_id
    data["user_pw"] = user_pw
    data["keywords"] = keyword

    print(f"data: {data}")

    result = get_driver(data)

    print(f"result: {result}")

    return jsonify(result)


@app.route("/search", methods=["POST"])
def search():
    # user_id = request.args.get("user_id")
    # user_pw = request.args.get("user_pw")
    # keyword = request.args.get("keyword")

    data = request.get_json()

    print(f"data: {data}")

    # print(f"user_id: {user_id} / user_pw: {user_pw} /keyword: {keyword}")

    result = get_driver(data)

    print(f"result: {result}")

    return jsonify(result)


if __name__ == "__main__":
    app.run(port=8080)
