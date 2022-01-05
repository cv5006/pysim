from math import sin, cos, pi


class TwoDofPlanarArm:
    def __init__(self):
        self.m = [0, 0]
        self.l = [0, 0]
        self.lc = [0, 0]
        self.I = [0, 0]
        self.b = [0, 0]
        self.gf = [[],[]]


    def Dynamics(self, t, x):
        _ = t
        q1, q2 = x[0], x[1]
        w1, w2 = x[2], x[3]

        g = 9.81

        m1, m2 = self.m[0], self.m[1]
        
        l1, lc1, lc2 = self.l[0], self.lc[0], self.lc[1]
        lc1_2, lc2_2, l1_2, l1lc2 = lc1*lc1, lc2*lc2, l1*l1, l1*lc2
        
        I1, I2 = self.I[0], self.I[1]

        d11 = m1*lc1_2 + m2*(l1_2 + lc2_2 + 2*l1lc2*cos(q2)) + I1 + I2
        d12 = m2*(lc2_2 + l1lc2*cos(q2)) + I2
        d21 = d12
        d22 = m2*lc2_2 + I2

        det_d = d11*d22 - d12*d21
        id11 =  d22/det_d
        id12 = -d12/det_d
        id21 = -d21/det_d
        id22 =  d11/det_d

        h = -m2*l1lc2*sin(q2)
        c11 =  h*w2
        c12 =  h*(w1 + w2)
        c21 = -h*w1
        c22 =  0

        g2 = m2*lc2*g*cos(q1 + q2)
        g1 = (m1*lc1 + m2*l1)*g*cos(q1) + g2
        
        torque1 = 0 - (c11*w1 + c12*w2) - g1 - self.b[0]*w1
        torque2 = 0 - (c21*w1 + c22*w2) - g2 - self.b[1]*w2

        dw1dt = id11*torque1 + id12*torque2
        dw2dt = id21*torque1 + id22*torque2

        dxdt = [w1, w2, dw1dt, dw2dt]
        return dxdt


if __name__ == "__main__":
    tdpa = TwoDofPlanarArm()
    tdpa.m = [1, 1]
    tdpa.l = [1, 1]
    tdpa.lc = [0.5, 0.5]

    print(tdpa.Dynamics(0, [-pi/2, 0, 0, 0]))