import os
import secrets
from PIL import Image
from flask_login import current_user
from Genethesis import app

def save_illustrations(images):

    for image in images:

        user_path = os.path.join(app.root_path, 'static/illustrations', str(current_user.id))
        all_images = os.listdir(user_path)
        
        fn, ext = os.path.splitext(image.filename)

        if image.filename.replace(' ', '_') in all_images:
                random_hex = secrets.token_hex(8)
                image_name = fn.replace(' ', '_') + random_hex + ext
        else:
                image_name = image.filename.replace(' ', '_')


        image_path = os.path.join(app.root_path, 'static/illustrations', str(current_user.id), image_name)

        # Resize Image
        output_size = (720, 720)
        cpd_image = Image.open(image)
        cpd_image.thumbnail(output_size)

        cpd_image.save(image_path)