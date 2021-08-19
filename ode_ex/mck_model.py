# Mass-spring-damper system
class MCKmodel:
    def __init__(self, m_=1, c_=0, k_=0, xo_=0) -> None:
        self.m = m_
        self.c = c_
        self.k = k_
        self.xo = xo_
        

        self.u = lambda t, x: 0
        self.f = lambda t, x: 0

    def setU(self, ufunc_):
        self.u = ufunc_

    def setF(self, ffunc_):
        self.f = ffunc_

    def model(self, t, x):
        p = x[0]
        v = x[1]

        e = p - self.xo        
        U = self.u(t, x) + self.f(t, x)

        c = self.c/self.m
        k = self.k/self.m
        b = 1/self.m

        a = -c*v -k*e + b*U
        
        dxdt = v, a
        return dxdt


if __name__=="__main__":
    from math import sin, cos, pi
    m, c, k = 2, 1, 1

    mck = MCKmodel(m, c, k, 0)

    print(mck.model(1,[0, 1]))

    mck.setU(lambda t, x: sin(2*pi*t))
    print(mck.u(0.1, 0))
    
    mck.setF(lambda t, x: cos(2*pi*t))
    print(mck.f(0.1, 0))
    
    
