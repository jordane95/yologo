"""
Run a rest API exposing the logo ascii art model
"""
import io

from PIL import Image
from flask import Flask, request
from logo import LogoEncoder
import numpy as np


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def predict():
    if not request.method == "POST":
        return "Hello, world"

    if request.files.get("image"):
        image_file = request.files["image"]
        image_bytes = image_file.read()

        img = Image.open(io.BytesIO(image_bytes))
        encoder = LogoEncoder()
        results = encoder.encode_logo(np.asarray(img))
        return results


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7595)
