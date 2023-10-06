from tasks import process_image

input_image_path = "C:/Users/snw12/PycharmProjects/raspt_v1/foto"
output_image_path = "C:/Users/snw12/PycharmProjects/raspt_v1/image"

result = process_image.apply_async(args=[input_image_path, output_image_path], queue='default', routing_key='default')
result.get()  # Получаем результат, если это необходимо
