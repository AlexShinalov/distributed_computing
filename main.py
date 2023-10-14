from tasks import add_numbers

result = add_numbers.apply_async(args=[1, 5])
result.get()