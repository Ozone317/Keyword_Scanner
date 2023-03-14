from collections import defaultdict
from flask import Flask, request, jsonify
from json import loads

app = Flask(__name__)

@app.route("/")
def home():
    return {"message": "Hello and Welcome"}


# collection = {"text": "TEXT_FROM_USER"}
@app.route("/getkeywords", methods=["POST"])
def getKeywords():
    try:
        variable = request.get_data()
        text = loads(variable)
        # print(type(text))
        # print(text)

        # res = request.get_json()
        # print(type(res))

        text = text["text"]
        data = extractKeywords(text)
        # print(text)
        return jsonify({"data": data})
    except:
        return jsonify({"message": "Invalid format"})


from rake_nltk import Rake

def extractKeywords(text: str):
    r = Rake()
    r.extract_keywords_from_text(text)
    data = defaultdict(list)
    for rating, keyword in r.get_ranked_phrases_with_scores():
        data[rating].append(keyword)

    return data


if __name__ == "__main__":
    from waitress import serve
    serve(app, port=5000)
    # app.run(debug=True)


