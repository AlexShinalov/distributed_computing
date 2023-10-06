from tasks import process_image

image_path = "/path/to/your/image.jpg"
process_image.delay(image_path)