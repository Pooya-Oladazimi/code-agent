from functions.get_file_content import get_file_content

result = get_file_content("calculator", "main.py")
print(result)
result = get_file_content("calculator", "pkg")
print(result)
