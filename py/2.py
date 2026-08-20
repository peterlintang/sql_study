import os

fd = os.open("hello.txt", os.O_CREAT|os.O_RDWR, 0o644)
os.write(fd, "hello world\n".encode('utf-8'))
os.close(fd)

f = open("11.txt", mode='x', encoding='utf-8')
print(dir(f))
f.close()
