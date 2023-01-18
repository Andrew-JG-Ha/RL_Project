class DEQUE:
    """
    Implementation of the double ended queue data structure
    """
    def __init__(self, size = 10) -> None:
        self.queue = [None]*size
        self.tail = 0
        self.head = 0
        self.length = 0
        self.queueSize = size

    def dequeue(self):
        """
        Removes and returns the first value
        """
        element = self.queue[self.head]
        self.queue[self.head] = None
        self.length -= 1
        self.head = (self.head + 1) % self.queueSize
        return element
    
    def enqueue(self, element) -> None:
        """
        Adds the element to the rear of the queue and automatically scale the list if the head and tail overlap
        """
        if (self.tail == self.head and self.length == self.queueSize):
            self.scale()
        self.queue[self.tail] = element
        self.tail = (self.tail + 1) % self.queueSize
        self.length += 1

    def addFront(self, element) -> None:
        """
        Adds the element to the front of the queue and automatically scales the list if the head and tail overlap
        """
        if (self.tail == self.head and self.length == self.queueSize):
            self.scale()
        self.head = (self.head - 1) % self.queueSize
        self.queue[self.head] = element
        self.length += 1

    def removeLast(self):
        """
        Removes and returns the last value
        """
        self.tail = (self.tail - 1) % self.queueSize
        element = self.queue[self.tail]
        self.queue[self.tail] = None
        self.length -= 1
        return element

    def clear(self) -> None:
        """
        Clears the deque of all values and resets the head and tail to be at the 0th index
        """
        while self.length > 0:
            self.dequeue()
        
    def scale(self) -> None:
        """
        Rescales the deque to 2 times the current size
        """
        self.queueSize *= 2
        newQueue = [None] * self.queueSize
        currentLength = self.length
        for index in range(0, currentLength):
            newQueue[index] = self.queue[(self.head + index) % currentLength]
        self.length = currentLength
        self.head = 0
        self.tail = currentLength
        self.queue = newQueue

    def getTail(self):
        """
        Returns the value at the end of the deque
        """
        return self.queue[self.tail]

    def getHead(self):
        """
        Returns the value at the head of the deque
        """
        return self.queue[self.head]

    def printDeque(self) -> None:
        """
        Prints all the elements in the deque and specifies the head and tail 
        """
        print("[", end="")
        for index in range(0, self.queueSize):
            if index == self.head:
                print("HEAD:", end="")
            if index == self.tail:
                print("TAIL:", end="")
            
            if (index == self.queueSize - 1):
                print(self.queue[index], end="")
            else:
                print(self.queue[index], end=", ")
        print("]")