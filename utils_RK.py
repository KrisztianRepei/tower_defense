import math

def dist_RK(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

def clamp_RK(v, lo, hi):
    return max(lo, min(hi, v))

def lerp_RK(a, b, t):
    return a + (b - a) * t
