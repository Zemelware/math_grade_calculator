import math_grade_calculator as mc

url = input("Enter the url of the 'My Works' page in your math class: ")
username = input("Enter your Edsby username: ")
password = input("Enter your Edsby password: ")

print("Calculating. This may take a few seconds...")

mc.calculate(url, username, password)
