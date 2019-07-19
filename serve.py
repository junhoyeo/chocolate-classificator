from flask import Flask, request, render_template
from PIL import Image
from io import BytesIO
import torch
from model import Net, transform, classes

app = Flask(__name__)
model = Net()
model.load_state_dict(torch.load('./model.pt'))
model.eval()

@app.route('/', methods=['GET', 'POST'])
def home():
  if request.method == 'POST':
    if 'image' not in request.files:
      return render_template('index.html', error='nono')
    image = request.files['image']
    if image.filename.split('.')[-1] not in ['png', 'jpg']:
      return render_template('index.html', error='nono')
    image = Image.open(BytesIO(image.read()))
    input = transform(image)
    input = input.view(1, 3, 224, 224)
    output = model(input)
    prediction = int(torch.max(output.data, 1)[1].numpy())
    return render_template('index.html', result=classes[prediction])
  return render_template('index.html')

app.run(debug=True)
