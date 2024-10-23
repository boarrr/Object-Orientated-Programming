def function_1(parameter):
    parameter = parameter + 1

def function_2(parameter2):
    parameter2[0] = parameter2[0] + 1


x = 5
y = [1,2]

print(f"Original value of x: {x} and y: {y}")

function_1(x)
function_2(y)

print(f"Final value of x: {x} and y: {y}")
