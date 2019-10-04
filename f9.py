import numpy as np
import pandas as pd

class table():
    def birth(self, name):
        a = pd.read_excel(name)
        r = np.asarray(a)
        d1 = dict()
        self.j = dict()
        for i in range(len(r)):
            d1[r[i, 0]] = str(r[i, 1])[8:10] + '.' + str(r[i, 1])[5:7] + '.' + str(r[i, 1])[0:4]
            self.j[r[i, 0]] = r[i, 2]
        return d1

    def rwr(self, kurs, naprav, lol):
        r = self.nap[self.col[naprav]]
        self.table1[kurs, naprav] = lol

    def table(self, name):
        a = pd.read_excel(name)
        self.col = dict(zip(a.columns.values.tolist(),[i - 1 for i in range(len(a.columns.values.tolist()))]))
        r = np.asarray(a)
        self.table1 = list()
        for i in range(len(r)):
            self.table1.append(list())
            for j in range(1, len(r[i])):
                self.table1[i].append(str(r[i, j])[8:10] + '.' + str(r[i, j])[5:7] + '.' + str(r[i, j])[0:4])

    def date(self, kurs, naprav):
        if(kurs < len(self.col)):
            return self.table1[kurs - 1][self.col[naprav]]
        else:
            return '-'

    def max_kurs(self):
        return len(self.col)