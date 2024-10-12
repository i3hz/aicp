import numpy as np
from numdifftools import Gradient
import pickle

def f(arr):
    x,y = arr 
    return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2

def Fib(n):
    if n == 0 :
        return [1]
    f = [1,1]
    for i in range(2, n+1):
        f.append( f[-2] + f[-1])
    return f

def Fibonacci(f, x_l, x_u, n):
    fib = Fib(n)
    x1 = x_l + (fib[n-2]/ fib[n])*(x_u - x_l)
    x2 = x_l + (fib[n-1]/ fib[n])*(x_u - x_l)
    while n>1 :
        # print(f"n = {n} | x_l = {x_l} | x_u = {x_u} | x1 = {x1} | x2 = {x2}")
        n = n - 1
        f1 = f(x1)
        f2 = f(x2)
        if f1 < f2 :
            x_u = x2
            x2 = x1
            x1 = x_l + (fib[n-2]/ fib[n])*(x_u - x_l)
            f2 = f1
            f1 = f(x1)
        elif f1 > f2 :
            x_l = x1
            x1 = x2
            f1 = f2
            x2 = x_l + (fib[n-1]/ fib[n])*(x_u - x_l)
            f2 = f(x2)
        else :
            x_l = x_l + 0.03*(x_u - x_l)
            x1 = x_l + (fib[n-2]/ fib[n])*(x_u - x_l)
            x2 = x_l + (fib[n-1]/ fib[n])*(x_u - x_l)
    return min([x_l , x_u], key = f) 
df = Gradient(f)
def GD_(f,df,x0, lr =0.01 ,eps =1e-9 ):
    xk = x0 ; xk1 = x0+ 2*eps
    dfxk = df(xk)
    path = [xk] 
    while np.linalg.norm(dfxk) > eps and np.linalg.norm(xk-xk1) > eps  :
        xk1 = xk
        xk = xk - lr*dfxk
        dfxk = df(xk)
        path.append(xk)
    return xk, np.array(path)

def GD(f,df,x0, eps =1e-9 ):
    xk = x0 ; xk1 = x0+ 2*eps
    dfxk = df(xk)
    path = [xk] 
    def phi(al):
        return f(xk - al*dfxk)
    
    while np.linalg.norm(dfxk) > eps and np.linalg.norm(xk-xk1) > eps  :
        al = Fibonacci(phi, 0, 10, 40)
        xk1 = xk
        xk = xk - al*dfxk
        dfxk = df(xk)
        path.append(xk)
    return xk, np.array(path)

if __name__ == "__main__":
    arr = np.array([3,2.4])
    xop1, path1 = GD(f,df,arr ,eps =1e-9 )
    xop2, path2 = GD_(f,df,arr ,lr=.001,eps =1e-9 )
    data = {
        'GD pas optimal' :{
            "path" : path1,
            "x_optimal" : xop1
        },
        'GD pas fixe' :{
            "path" : path2,
            "x_optimal" : xop2
        }
    }

    pickle_filename = 'data.pkl'

    # Save the data dictionary to a Pickle file
    with open(pickle_filename, 'wb') as pickle_file:
        pickle.dump(data, pickle_file)

    print(f'Data saved to {pickle_filename}')
    
    