"""
Práctica 2: Sistema respiratorio

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Edgar Iván Rivas Rosas
Número de control: 21212748
Correo institucional: l21212748@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Instalar librerias en consola
#!pip install control
#!pip install slycot

# Librerías para cálculo numérico y generación de gráficas
import numpy as np
import math as m
import matplotlib.pyplot as plt
from scipy.signal import square
import control as ctrl


# Datos de la simulación
x0,t0,tend,dt,w,h = 0,0,20,1E-3,6,3
N = round((tend-t0)/dt) + 1
t = np.linspace(t0,tend,N)

u1 = (square(2 * np.pi * 0.5 * t, duty=0.5) + 1) * 2  # Señal de 0 a 4






def sys_endocrino(R,Rf,Cr,Cp,L):
    alpha3 = (L*Rf*Cp*Cr)
    alpha2 = (R*Rf*Cr*Cp)+(L*Cp)+(L*Cr)
    alpha1 = (R*Cp)+(R*Cr)+(Rf*Cr)
    alpha0 = 1
    
    num = 1
    den = [alpha3, alpha2, alpha1, alpha0]
    sys = ctrl.tf(num,den)
    return(sys)


#Funcion de transferencia: Individuo saludable [control]
sysS = sys_endocrino(500,50,10E-6,50E-6,0.1)
print('Individuo sano [control]: ')
print(sysS)

#Funcion de transferencia: Individuo enfermo [caso]
sysE = sys_endocrino(1,1000,500E-6,200E-6,5)
print('Individuo enfermo [caso]: ')
print(sysE)

morado =[68/255, 23/255, 82/255]
rosa =[255/255, 116/255, 139/255]
naranja =[255/255, 101/255, 0/255]
verde =[228/255, 241/255, 172/255]





def plotsignals(u, sysS, sysE, sysPID):
    fig = plt.figure()
    ts,Vs = ctrl.forced_response(sysS,t,u,x0)
    ts,Ve = ctrl.forced_response(sysE,t,u,x0)
    ts,VPID = ctrl.forced_response(sysPID,t,u,x0)
    plt.plot(t,VPID,"-", color = verde, label = "VID(t)")
    
    plt.plot(t,Vs,"-", color = morado, label = '$Cort(t): Control$')

    plt.plot(t,Ve,"-", color = naranja, label = '$Cort(t): Caso$')
        
    plt.grid(False)
    plt.xlim(0,20)
    plt.ylim(-0.25,4.25)
    plt.xticks(np.arange(0, 21, 2))
    plt.yticks(np.arange(0, 4.5, 0.5))
    plt.xlabel("$t$ [s]")
    plt.ylabel("$Cort(t)$ [V]")
    plt.legend(bbox_to_anchor = (0.5,-0.3), loc= "center", ncol=4,
               fontsize = 8, frameon = False)
    plt.show()
    fig.set_size_inches(w,h)
    fig.tight_layout()
    fig.savefig("LA y LC.pdf",bbox_inches = "tight")

# Componentes del controlador
Cr = 1000E-6
kP = 2
kI = 4
Re = 1/(kI*Cr)
Rr = kP * Re

numPID = [Rr*Cr, 1]
denPID = [Re*Cr,0]
PID = ctrl.tf(numPID,denPID)
X = ctrl.series(PID,sysE)
sysPID = ctrl.feedback(X,1, sign= -1)
    

plotsignals(u1, sysS, sysE, sysPID)




