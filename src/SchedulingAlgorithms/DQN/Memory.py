import numpy as np
from collections import deque

class Memory(object):
    """Memory buffer for Experience Replay."""

    def __init__(self, max_size):
        """Initialize a buffer containing max_size experiences."""
        self.buffer = deque(maxlen=max_size)

    def add(self, experience):
        """Add an experience to the buffer."""
        self.buffer.append(experience)

    def sample(self, batch_size):
        """Sample a batch of experiences from the buffer."""
        buffer_size = len(self.buffer)
        index = np.random.choice(
            np.arange(buffer_size),
            size=batch_size,
            replace=False
        )

        return [self.buffer[i] for i in index]

    def __len__(self):
        """Interface to access buffer length."""
        return len(self.buffer)