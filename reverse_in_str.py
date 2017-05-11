# Reverse order of blocks in string
st_old = input()
n = int(input('Input number of symbols in block: '))

for i in range(len(st_old)-n, -n, -n):
    print(st_old[i:i+n], end='')

# Generating Markov rules
for i in range(0, 26):
    print('#',chr(ord('a')+i),'->', chr(ord('a')+(i+2)%26), '#', sep='')
# a = [chr(ord('a')+i)+'->'+chr(ord('a')+(i+2)%26)+'\n' for i in range(0, 26)]; print(a)
