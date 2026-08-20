
fo = open("hello.aa", "r+")
print(fo.name)
print(fo.closed)
print(fo.mode)
fo.write("hello world\n")
aa = fo.read()
print(aa)
fo.close()
