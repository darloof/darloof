import secrets
import os
from PIL import Image
from flask import current_app as app
import base64
import hashlib

def save_picture(picture_object):
    picture_data = picture_object.read()
    picture_hash = hashlib.sha1(picture_data).hexdigest()

    _, f_ext = os.path.splitext(picture_object.filename)
    picture_fn = picture_hash + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(picture_object)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn