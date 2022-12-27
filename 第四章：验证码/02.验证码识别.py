# 使用第三方库识别验证码
import pytesseract
from PIL import Image

if __name__ == '__main__':
    im = Image.open('code.jpg')
    """
    使用pytesseract识别验证码需要本地安装Tesseract-OCR，参考https://www.jianshu.com/p/2db541800418
    """
    result = pytesseract.image_to_string(im)
    print(result)