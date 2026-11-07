'''Task 09 | Streaming Log Inspector
Concepts: Generators, iterators, file handling
Problem: Write a generator read_errors(path) that streams a log file line by line, yielding (line_number, timestamp, message) only for ERROR records. Build summarize_errors() to count errors by date.
Requirements: Do not load the whole file into memory. Skip malformed lines while tracking their count. Expected format: YYYY-MM-DD HH:MM:SS | LEVEL | message.
Sample / expected behavior: Input line: 2026-11-07 10:30:00 | ERROR | Connection lost -> (1,"2026-11-07 10:30:00","Connection lost").'''


from datetime import datetime


def read_errors(path, stats=None):
    """
    Read a log file line by line.
    Yield (line_number, timestamp, message) for ERROR records.

    Malformed lines are skipped and counted.
    """
    if stats is None:
        stats = {"malformed": 0}

    with open(path, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            try:
                parts = line.strip().split("|", 2)

                if len(parts) != 3:
                    raise ValueError("Invalid log format")

                timestamp = parts[0].strip()
                level = parts[1].strip()
                message = parts[2].strip()

                # Validate timestamp.
                datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

                if not level or not message:
                    raise ValueError("Missing log information")

                if level == "ERROR":
                    yield (line_number, timestamp, message)

            except ValueError:
                stats["malformed"] += 1


def summarize_errors(path):
    """
    Count ERROR records by date.
    Also return the number of malformed lines.
    """
    stats = {"malformed": 0}
    error_counts = {}

    for line_number, timestamp, message in read_errors(path, stats):
        date = timestamp.split(" ")[0]

        if date not in error_counts:
            error_counts[date] = 0

        error_counts[date] += 1

    return error_counts, stats["malformed"]



sample_logs = [
    "2026-11-07 10:30:00 | ERROR | Connection lost",
    "2026-11-07 10:35:00 | INFO | User logged in",
    "2026-11-07 10:40:00 | WARNING | Disk space is low",
    "2026-11-07 11:00:00 | ERROR | Database timeout",
    "This is a malformed log line",
    "2026-11-08 09:15:00 | ERROR | Permission denied"
]

file_path = "sample_logs.txt"

with open(file_path, "w", encoding="utf-8") as file:
    for log in sample_logs:
        file.write(log + "\n")



print("TEST 1: ERROR LOG RECORDS")
print("-" * 50)

for record in read_errors(file_path):
    print(record)



print("\nTEST 2: ERROR SUMMARY")
print("-" * 50)

error_counts, malformed_count = summarize_errors(file_path)

for date, count in error_counts.items():
    print(date, ":", count, "errors")

print("Malformed lines:", malformed_count)



print("\nTEST 3: GENERATOR CHECK")
print("-" * 50)

result = read_errors(file_path)

print("Is generator:", hasattr(result, "__next__"))
print("First error:", next(result))
