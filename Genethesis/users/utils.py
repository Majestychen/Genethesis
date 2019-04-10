import os
import secrets
from PIL import Image
from Genethesis import app
from flask_login import current_user

def save_avatar(new_image):
    random_hex = secrets.token_hex(16)
    _, file_ext = os.path.splitext(new_image.filename)
    avatar_filename = random_hex + file_ext
    avatar_path = os.path.join(app.root_path, 'static/avatars', avatar_filename)

    # Resize Image
    output_size = (300, 300)
    image = Image.open(new_image)
    image.thumbnail(output_size)

    image.save(avatar_path)
    return avatar_filename

def delete_avatar(old_image):
    old_avatar_path = os.path.join(app.root_path, 'static/avatars', old_image)
    os.remove(old_avatar_path)
    return

def save_signature(new_image):
    _, file_ext = os.path.splitext(new_image.filename)
    signature_filename = str(current_user.id) + file_ext
    signature_path = os.path.join(app.root_path, 'static/signatures', signature_filename)

    # Resize Image
    output_size = (300, 300)
    image = Image.open(new_image)
    image.thumbnail(output_size)

    image.save(signature_path)
    return signature_filename

def delete_signature(old_image):
    old_signature_path = os.path.join(app.root_path, 'static/signatures', old_image)
    os.remove(old_signature_path)
    return
