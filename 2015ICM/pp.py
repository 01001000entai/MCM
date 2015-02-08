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
        for i in range(m):
            l1[i] = -self.INF
            for j in range(n):
                l1[i] = max(self.mat[i][j], l1[i])
            if l1[i] == -self.INF:
                return -1
        for i in range(n):
            l2[i] = 0
        for i in range(m):
            t = [-1 for j in range(self.maxn)]
            p = 0
            q = 0
            s[0] = i
            while p<=q and self.match1[i]<0:
                k = s[p]
                j = 0
                while j<n and self.match1[i]<0:
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
                    for j in range(n):
                        if t[j]<0 and l1[s[k]]+l2[j]-self.[s[k]][j]<p:
                            p = l1[s[k]]+l2[j]-mat[s[k]][j]
                for j in range(n):
                    if t[j] >= 0:
                        l2[j] += p
                for k in range(q+1):
                    l1[s[k]] -= p
            ret = 0
            for i in range(m):
                ret += self.mat[i][self.match1[i]]
            return ret
#End KM
