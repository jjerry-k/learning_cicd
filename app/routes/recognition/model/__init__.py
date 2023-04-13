import os
import numpy as np
import torch
import torchvision
from torchvision import transforms

import json
with open(os.path.join(os.path.dirname(__file__), "imagenet_class_index.json")) as f:
    classes_name = json.load(f)

torch_model = torchvision.models.mobilenet_v3_small(pretrained=True)
torch_model.eval()
def predict_torch(img):
    transforms_img = transforms.Compose([transforms.Resize((224, 224)), transforms.ToTensor()])
    img = transforms_img(img)
    img = torch.unsqueeze(img, 0)
    with torch.inference_mode():
        classes = torch.softmax(torch_model(img), dim=1).cpu().detach().numpy()
    #print("--- %s seconds ---" % (time.time() - start_time))

    top_n_preds = np.argpartition(classes, -5)[:, -5:]
    top_n_preds = top_n_preds[0]

    finalResult = top_n_preds[np.argsort(-classes[:, top_n_preds])]

    return {'prediction': [
        {'classname': classes_name[str(finalResult[0, 1])][1], 'possibility': classes[0, finalResult[0, 1]] * 100},
        {'classname': classes_name[str(finalResult[0, 2])][1], 'possibility': classes[0, finalResult[0, 2]] * 100},
        {'classname': classes_name[str(finalResult[0, 3])][1], 'possibility': classes[0, finalResult[0, 3]] * 100},
        {'classname': classes_name[str(finalResult[0, 4])][1], 'possibility': classes[0, finalResult[0, 4]] * 100}
        ]
    }

import onnxruntime as ort
ort_session = ort.InferenceSession(os.path.join(os.path.dirname(__file__), "mobilenet_v3_small.onnx"), providers=['CPUExecutionProvider'])

def softmax(x):
    return(np.exp(x - np.max(x)) / np.exp(x - np.max(x)).sum())

def predict_onnx(img):
    transforms_img = transforms.Compose([transforms.Resize((224, 224)), transforms.ToTensor()])
    img = transforms_img(img)
    img = torch.unsqueeze(img, 0).numpy()
    outputs = ort_session.run(None,{"actual_input_1": img},)
    classes = softmax(outputs[0])
    top_n_preds = np.argpartition(classes, -5)[:, -5:]
    top_n_preds = top_n_preds[0]

    finalResult = top_n_preds[np.argsort(-classes[:, top_n_preds])]

    return {'prediction': [
        {'classname': classes_name[str(finalResult[0, 1])][1], 'possibility': classes[0, finalResult[0, 1]] * 100},
        {'classname': classes_name[str(finalResult[0, 2])][1], 'possibility': classes[0, finalResult[0, 2]] * 100},
        {'classname': classes_name[str(finalResult[0, 3])][1], 'possibility': classes[0, finalResult[0, 3]] * 100},
        {'classname': classes_name[str(finalResult[0, 4])][1], 'possibility': classes[0, finalResult[0, 4]] * 100}
        ]
    }