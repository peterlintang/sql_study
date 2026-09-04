
import thread

def hello(arg):
    a = 10
    b = 20
    print("hello thread", arg)
    return a, b

e = 3
x, y = hello(e)
print (x, y)
print ("hello : ", (e))

thr1 = thread.Thread(target=hello, args=(10,))
thr1.start()
thr1.join()
#thread.start_new_thread( print_time, ("Thread-1", 2, ) )

print(thread.__doc__)



def create_user(name, age=18, *args, **kwargs):
    """
    *args: 接收多余的位置参数，打包成元组(tuple)
    **kwargs: 接收多余的关键字参数，打包成字典(dict)
    """
    print(f"Name: {name}, Age: {age}")
    print(f"args: {args}")
    print(f"kwargs: {kwargs}")

# 调用示例
create_user("Alice", 20, "Admin", "China", gender="Female", score=100)

