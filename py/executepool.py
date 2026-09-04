from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed

# 1. 使用线程池处理 I/O 任务
def fetch_data(url):
    # 模拟网络请求
    return f"Data from {url}"

with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(fetch_data, f"http://example.com/{i}") for i in range(5)]
    for future in as_completed(futures):
        print(future.result())

# 2. 使用进程池处理 CPU 任务
def compute_square(n):
    return n * n

with ProcessPoolExecutor(max_workers=4) as executor:
    results = executor.map(compute_square, [1, 2, 3, 4, 5])
    print(list(results))  # 输出: [1, 4, 9, 16, 25]

