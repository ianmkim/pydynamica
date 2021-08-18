import numpy as np
import matplotlib.pyplot as plt

def gen_perlin(x, y, seed=None):
    if seed is not None:
        np.random.seed(seed)
    p = np.arange(256, dtype=int)
    np.random.shuffle(p)
    p = np.stack([p,p]).flatten()

    x1, y1 = x.astype(int), y.astype(int)
    xf = x - x1
    yf = y - y1

    u = fade(xf)
    v = fade(yf)

    n00 = gradient(p[p[x1] + y1], xf, yf)
    n01 = gradient(p[p[x1] + y1 + 1], xf, yf -1)
    n11 = gradient(p[p[x1 + 1] + y1 + 1], xf -1, yf-1)
    n10 = gradient(p[p[x1+1] + y1], xf -1, yf)

    x1 = lerp(n00, n10, u)
    x2 = lerp(n01, n11, u)
    return lerp(x1, x2, v)

def lerp(a, b, x):
    return a + x * (b-a)

def fade(t):
    return 6 * t**5 - 15 * t **4 + 10 *t **3

def gradient(h, x, y):
    vectors = np.array([[0,1], [0,-1], [1,0], [-1,0]])
    g = vectors[h%4]
    return g[:,:,0] * x + g[:,:,1] * y

def create_perlin(x, y, res = 5, seed=None):
    xlin = np.linspace(0, res, x)
    ylin = np.linspace(0, res, y)
    x, y = np.meshgrid(xlin, ylin)
    map = gen_perlin(x, y, seed=seed)
    return map

if __name__ == "__main__":
    perl = create_perlin(100,50 )
    mx= 0.0
    mn= perl[0][0]
    for row in perl:
        if max(row) >mx:
            mx= max(row)
        if min(row) <mn:
            mn= min(row) 
    print(mx)
    print(mn)
    plt.imshow(perl, origin="upper")
    plt.show()
    print("showing image")
    
