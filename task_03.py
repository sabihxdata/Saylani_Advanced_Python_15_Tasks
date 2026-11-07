''' Task 03 | Recursive JSON Path Explorer
Concepts: Recursion, nested lists/dictionaries
Problem: Implement find_paths(data, target) that recursively searches nested dictionaries and lists and returns all paths whose value equals target.
Requirements: Use dot notation for dictionary keys and [index] for list positions. Preserve traversal order; do not treat bool True as numeric 1.
Sample / expected behavior: Input: {"a":[{"x":5},5],"b":{"y":5}}, target=5 -> ["a[0].x", "a[1]", "b.y"]. '''


def find_paths(data, target):

    paths = []

    def search(current_data, current_path):

        
        if isinstance(current_data, dict):

            for key, value in current_data.items():

                if current_path:
                    new_path = current_path + "." + str(key)
                else:
                    new_path = str(key)

                if isinstance(value, (dict, list)):
                    search(value, new_path)

                elif type(value) == type(target) and value == target:
                    paths.append(new_path)

        
        elif isinstance(current_data, list):

            for index, value in enumerate(current_data):

                new_path = current_path + "[" + str(index) + "]"

                if isinstance(value, (dict, list)):
                    search(value, new_path)

                elif type(value) == type(target) and value == target:
                    paths.append(new_path)

        
        elif type(current_data) == type(target) and current_data == target:
            paths.append(current_path if current_path else "$")

    search(data, "")

    return paths




data = {
    "a": [
        {"x": 5},
        5
    ],
    "b": {
        "y": 5
    }
}

result = find_paths(data, 5)

print("Matching paths:", result)




print(find_paths({"name": "Ali", "age": 25}, 25))

print(find_paths([1, [2, 3], 2], 2))

print(find_paths({"a": True, "b": 1}, 1))