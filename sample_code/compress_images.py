import requests
from PIL import Image
from io import BytesIO
import base64


def download_image(url):
    # 画像をダウンロード
    response = requests.get(url)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        raise Exception("Failed to download image")


def compress_image(image, quality=10):
    # 画像を指定した品質で圧縮
    buffer = BytesIO()
    image.save(buffer, format="JPEG", quality=quality)
    buffer.seek(0)
    return Image.open(buffer)


def image_to_base64(image):
    # 画像をBase64エンコード
    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def main():
    # 画像のURL
    image_url = "https://img.7api-01.dp1.sej.co.jp/item-image/045222/C727DB4E4ED27296AE5BC274055774DE.jpg"

    try:
        # 画像をダウンロード
        original_image = download_image(image_url)
        original_size = len(original_image.fp.read())
        print(f"Original image size: {original_size / 1024:.2f} KB")

        # 画像を圧縮
        compressed_image = compress_image(original_image)
        compressed_buffer = BytesIO()
        compressed_image.save(compressed_buffer, format="JPEG")
        compressed_size = len(compressed_buffer.getvalue())
        print(f"Compressed image size: {compressed_size / 1024:.2f} KB")

        # # 圧縮画像をBase64エンコード
        # base64_string = image_to_base64(compressed_image)
        # print("Base64 encoded image string:")
        # print(base64_string)

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
