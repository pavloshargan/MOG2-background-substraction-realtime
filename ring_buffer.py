class RingBuffer:
    def __init__(self,size_max):
        self.max = size_max
        self.data = []
        self.cur = 0
        
    def append(self, frame):
        if len(self.data) == self.max:
            self.data[self.cur] = frame
        else:
            self.data.append(frame)
        self.cur = (self.cur+1)%self.max

    def get_sorted(self):
        return [self.data[(self.cur+i)%len(self.data)] for i in range(self.max)]

    def get_last(self):
        if self.cur==0:
            idx_of_last = self.max-1
        else:
            idx_of_last = self.cur-1
        return self.data[idx_of_last].copy()

    def get_first(self):
        return self.data[self.cur].copy()

    def is_not_empty(self):
        return  (len(self.data) > 0)

    def is_full(self):
        return  (len(self.data) >= self.max)