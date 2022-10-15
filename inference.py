import boto3
import botocore

import torch
import gradio as gr
from torchvision import transforms

def download_model():
    bucket = 'mlops-tutorials'
    object_name = 'model.script.pt'
    filename = 'model.script.pt'

    s3 = boto3.resource('s3')

    try:
        s3.Bucket(bucket).download_file(object_name, filename)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise
    return 

def demo():
    #assert cfg.ckpt_path

    model = torch.jit.load('model.script.pt')

    model.eval()

    # Labels for CIFAR10 dataset
    labels = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck'] 

    def classify_top10(inp):
        inp = transforms.ToTensor()(inp).unsqueeze(0)
        with torch.no_grad():
            prediction = torch.nn.functional.softmax(model(inp)[0], dim=0)
            confidences = {labels[i]: float(prediction[i]) for i in range(10)}    
        return confidences
    
    im = gr.Image(shape=(224, 224), type="pil")

    gr.close_all()

    demo = gr.Interface(
        fn=classify_top10,
        inputs=[im],
        outputs=gr.Label(num_top_classes=10),
        examples='images',
    )

    demo.launch(server_name="0.0.0.0", share=True)


def main():
    demo()

if __name__ == "__main__":
    download_model()
    main()



