# bubble sorting function
def sort(ls):
    for i in range(len(ls)):
        j = i + 1
        while j in range(len(ls)):
            if ls[i] > ls[j]:
                ls[i], ls[j] = ls[j], ls[i]
            j += 1

if __name__ == '__main__':
    ls = [int(input()) for i in range(10)]
    print(ls)
    sort(ls)
    print(ls)
