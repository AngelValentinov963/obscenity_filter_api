import requests

url = "http://127.0.0.1:8000/nsfw_detector/"
#url = "http://127.0.0.1:8000/detect-guns/"
pic_name = "960-600-dariia-beloded.jpg"
with open(pic_name, "rb") as image_file:
    files = {"file": (pic_name, image_file, "image/jpeg")}
    response = requests.post(url, files=files)

print(response.status_code)
print(response.json())

