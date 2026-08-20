
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
