from collections import defaultdict
from flask import Flask, request, jsonify
from json import loads
import base64
import io
import PyPDF2
import pytesseract
from PIL import Image

app = Flask(__name__)

@app.route("/")
def home():
    return {"message": "Hello and Welcome"}


# collection = {"text": "TEXT_FROM_USER"}
@app.route("/get-keywords", methods=["POST"])
def getKeywords():
    try:
        variable = request.get_data()   # get data from body in terms of bytes
        text = loads(variable)          # convert the bytes into a Python object
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

@app.route("/pdf-to-text", methods=["POST"])
def getPdf():
    try:
        variable = request.get_data()
        encodedFile = loads(variable)
        pdfBytes = base64.b64decode(encodedFile)
        pdfIO = io.BytesIO(pdfBytes)

        pdfReader = PyPDF2.PdfFileReader(pdfIO)
        pdfText = ""

        for pageNum in range(pdfReader.getNumPages()):
            page = pdfReader.getPage(pageNum)
            pageText = page.extractText()

            if not pageText:
                # if the page is blank, we do OCR
                pageImage = page.getPixmap().getImage()
                pageImageBytes = io.BytesIO()
                pageImage.writeImage(pageImageBytes)
                pageImageBytes.seek(0)

                pageImagePIL = Image.open(pageImageBytes)
                pageTextOCR = pytesseract.image_to_string(pageImagePIL)
                pdfText += (pageTextOCR + " ")

            else:
                pdfText += (pageText + " ")

        dataToReturn = getKeywords(pdfText)
        return jsonify({"data": dataToReturn})
        
    except:
        return jsonify({"message": "Invalid format"})


from rake_nltk import Rake

def extractKeywords(text: str):
    r = Rake(max_length=100000000000000000000000000000000000)
    r.extract_keywords_from_text(text)
    data = defaultdict(list)
    for rating, keyword in r.get_ranked_phrases_with_scores():
        data[rating].append(keyword)

    data = sorted(data.items(), key=lambda x: x[0], reverse=True)    
    return data


if __name__ == "__main__":
    from waitress import serve
    serve(app, port=5000)
    # app.run(debug=True)


