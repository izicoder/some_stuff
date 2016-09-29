# sieve of Erathosphen
def sieve(n):
    ls = range(2, n + 1)
    p = 2
    while p**2 <= n:
        nums = range(2 * p, n + 1, p)
        ls = [i for i in ls if i not in nums]
        p = ls[ls.index(p) + 1]
    return list(ls)

if __name__ == '__main__':
    print(sieve(120))
