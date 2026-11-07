'''  Task 04 | Dependency Execution Planner
Concepts: Graphs, sets, algorithms
Problem: Given tasks and prerequisite pairs (A,B) meaning A must finish before B, return a valid execution order.
Requirements: Detect cycles and raise ValueError with a clear message. For multiple available tasks, select alphabetically first. Reject unknown task names.
Sample / expected behavior: Tasks=["build","test","deploy"]; dependencies=[("build","test"),("test","deploy")] -> ["build","test","deploy"].'''


def execution_planner(tasks, dependencies):

    
    if len(tasks) != len(set(tasks)):
        raise ValueError("Duplicate task names are not allowed")

    
    graph = {}
    in_degree = {}

    for task in tasks:
        graph[task] = []
        in_degree[task] = 0

    
    for first, second in dependencies:

        if first not in graph or second not in graph:
            raise ValueError("Unknown task name found")

        if second not in graph[first]:
            graph[first].append(second)
            in_degree[second] += 1

    
    available = []

    for task in tasks:
        if in_degree[task] == 0:
            available.append(task)

    available.sort()

    execution_order = []

    
    while available:

        current_task = available.pop(0)
        execution_order.append(current_task)

        for next_task in graph[current_task]:

            in_degree[next_task] -= 1

            if in_degree[next_task] == 0:
                available.append(next_task)

        available.sort()

    
    if len(execution_order) != len(tasks):
        raise ValueError("Cycle detected in task dependencies")

    return execution_order




tasks = ["build", "test", "deploy"]

dependencies = [
    ("build", "test"),
    ("test", "deploy")
]

result = execution_planner(tasks, dependencies)

print("Execution Order:", result)




print(execution_planner(
    ["database", "backend", "frontend"],
    [("database", "backend"), ("backend", "frontend")]
))


try:
    print(execution_planner(
        ["build", "test"],
        [("build", "deploy")]
    ))
except ValueError as error:
    print(error)



try:
    print(execution_planner(
        ["A", "B", "C"],
        [("A", "B"), ("B", "C"), ("C", "A")]
    ))
except ValueError as error:
    print(error)