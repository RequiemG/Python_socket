import json
x = True
y1 = json.dumps(x)
print(y1)
print("y1type:",type(y1))
y2 = json.loads(y1)
print(y2)
print("y2type:",type(y2))