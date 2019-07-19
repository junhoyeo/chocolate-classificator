from flask import Flask, request, render_template, url_for
from PIL import Image
from io import BytesIO
import torch
from model import Net, transform
import time

app = Flask(__name__)
model = Net()
model.load_state_dict(torch.load('./model.pt'))
model.eval()


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'image' not in request.files:
            return render_template('index.html', error='파일이 업로드되지 않았어요.')
        image = request.files['image']
        if image.filename.split('.')[-1] not in ['png', 'jpg']:
            return render_template(
                'index.html',
                error='이미지 형식이 잘못되었어요. png나 jpg 확장자를 가진 파일만 업로드할 수 있어요.')
        image_first_name = image.filename
        image_name = 'uploads/{}-{}'.format(int(time.time()), image.filename)
        image_path = './static/{}'.format(image_name)
        image.save(image_path)
        try:
            image = Image.open(image_path)
            input = transform(image)
            input = input.view(1, 3, 224, 224)
            output = model(input)
            prediction = int(torch.max(output.data, 1)[1].numpy())
        except BaseException:
            return render_template('index.html', error='이미지 처리 중 에러가 발생했어요.')
        return render_template('index.html',
                               success=True,
                               result=prediction,
                               image=image_name,
                               filename=image_first_name
                               )
    return render_template('index.html')


app.run(debug=True)
