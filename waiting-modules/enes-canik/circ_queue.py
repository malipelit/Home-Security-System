class CircularQueue:

    # constructor for the class
    # taking input for the size of the Circular queue 
    # from user
    def __init__(self, maxSize):
        self.queue = maxSize*[False]
        # user input value for maxSize
        self.maxSize = maxSize
        self.tail = 0

    # add element to the queue
    def enqueue(self, data):
        # add element to the queue
        self.queue[self.tail] = data
        # increment the tail pointer
        self.tail = (self.tail+1) % self.maxSize
        return True

    # find the size of the queue
    def size(self):
        if self.tail >= self.head:
            qSize = self.tail - self.head
        else:
            qSize = self.maxSize - (self.head - self.tail)
        # return the size of the queue
        return qSize

    def avg(self):
        return sum(self.queue)/self.maxSize

