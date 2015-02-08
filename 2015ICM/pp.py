#带权二分图匹配模版

class KM():
    def __init__(self, n, m):
        self.maxn = 400
        self.INF = 1000000000
        self.n = n
        self.m = m
        self.mat = [[-self.INF for i in range(n)] for j in range(m)]
        self.match1 = [-1 for i in range(m)]
        self.match2 = [-1 for i in range(n)]
    def add_edge(self,u,v,w):
        self.mat[u][v] = w
    def run(self):
        l1 = [0 for i in range(self.maxn)]
        l2 = [0 for i in range(self.maxn)]
        s = [0 for i in range(self.maxn)]
        for i in range(self.m):
            l1[i] = -self.INF
            for j in range(self.n):
                l1[i] = max(self.mat[i][j], l1[i])
            if l1[i] == -self.INF:
                return -1
        for i in range(self.n):
            l2[i] = 0
        i = 0
        while i < self.m:
            t = [-1 for j in range(self.maxn)]
            p = 0
            q = 0
            s[0] = i
            while p<=q and self.match1[i]<0:
                k = s[p]
                j = 0
                while j<self.n and self.match1[i]<0:
                    if l1[k]+l2[j]==self.mat[k][j] and t[j]<0:
                        q += 1
                        s[q] = self.match2[j]
                        t[j] = k
                        if s[q]<0:
                            p = j
                            while p >= 0:
                                self.match2[j] = k = t[j]
                                p = self.match1[k]
                                self.match1[k] = j
                                j = p
                    j += 1
                p += 1
            if self.match1[i] < 0:
                i -= 1
                p = self.INF
                for k in range(q+1):
                    for j in range(self.n):
                        if t[j]<0 and l1[s[k]]+l2[j]-self.mat[s[k]][j]<p:
                            p = l1[s[k]]+l2[j]-mat[s[k]][j]
                for j in range(n):
                    if t[j] >= 0:
                        l2[j] += p
                for k in range(q+1):
                    l1[s[k]] -= p
            i += 1
        ret = 0
        for i in range(self.m):
            if self.match1[i] == -1:
                continue
            ret += self.mat[i][self.match1[i]]
        return ret
#End KM

#Everything is OK
