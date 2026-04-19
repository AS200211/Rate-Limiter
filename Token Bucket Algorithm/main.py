import time
import threading
from collections import defaultdict


class Bucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.token = capacity
        self.refill_rate = refill_rate
        self.last_refill_ts = time.time()
        self.lock = threading.Lock()

    def _refill(self):
        now = time.time()
        elapsed = now - self.last_refill_ts
        add = int(elapsed*self.refill_rate)
        if add>0:
            self.token = min(self.capacity, self.token+add)
            self.last_refill_ts = now

    def allow_request(self) -> bool:
        with self.lock:
            self._refill()
            if self.token > 0:
                self.token-=1
                return True
            return False



class TokenBucketRateLimiter:
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.buckets = defaultdict(lambda: Bucket(capacity, refill_rate))
    
    def allow(self, user_id: str) -> bool:
        return self.buckets[user_id].allow_request()