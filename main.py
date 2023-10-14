from tasks import process_image
import os

# Получаем список всех файлов в папке "foto"
image_folder = 'foto'
images = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith('.jpg')]

# Отправляем задачи на обработку
for image_path in images:
    process_image.delay(image_path)
