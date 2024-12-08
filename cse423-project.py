import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import time
from IPython.display import clear_output
from PIL import Image

def create_opengl_context():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"OpenGL Window")
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glViewport(0, 0, 800, 600)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, 800, 0, 600)
    glMatrixMode(GL_MODELVIEW)
create_opengl_context()

# Create offscreen OpenGL context
glutInit([])
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(800, 600)
glutCreateWindow(b"Offscreen OpenGL Context")

def findZone(p1,p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    zone=False
    if abs(dx)>abs(dy):
        if dx>0 and dy>=0:
            zone=0
        elif dx<0 and dy>=0:
            zone=3
        elif dx<0 and dy<=0:
            zone=4
        elif dx>0 and dy<=0:
            zone=7
    else:
        if dx>=0 and dy>0:
            zone=1
        elif dx<=0 and dy>0:
            zone=2
        elif dx<=0 and dy<0:
            zone=5
        elif dx>=0 and dy<0:
            zone=6
    return zone

def convertZone_0_to_n(zone,x1,y1):
    if zone == 0:
        return x1,y1
    elif zone == 1:
        return y1,x1
    elif zone == 2:
        return -y1,x1
    elif zone == 3:
        return -x1,y1
    elif zone == 4:
        return -x1,-y1
    elif zone == 5:
        return -y1,-x1
    elif zone == 6:
        return y1,-x1
    elif zone == 7:
        return x1,-y1

def convertZone_n_to_0(p,zone):
    #zone_convert = [[1, 1], [1, 1], [1, -1], [-1, 1], [-1, -1], [-1, -1], [-1, 1], [1, -1]]

    if zone==0:
       p[0],p[1]=p[0],p[1]
    elif zone==1:
       p[0], p[1] = p[1], p[0]
    elif zone==2:
       p[0], p[1] = p[1], -p[0]
    elif zone==3:
       p[0], p[1] = -p[0], p[1]
    elif zone==4:
       p[0], p[1] = -p[0], -p[1]
    elif zone==5:
       p[0], p[1] = -p[1], -p[0]
    elif zone==6:
       p[0], p[1] = -p[1], p[0]
    elif zone==7:
       p[0], p[1] = p[0], -p[1]

    return p

def midPointAlgorithm(p1,p2):

    zone=findZone(p1,p2)

    p1=convertZone_n_to_0(p1,zone)
    p2=convertZone_n_to_0(p2,zone)



    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]

    d_init = 2 * dy - dx
    d = d_init

    x = p1[0]
    y = p1[1]
    x_new,y_new=convertZone_n_to_0([x,y],zone)

    #print(x_new,y_new)
    while (x < p2[0]):
        if d > 0:
            x += 1
            y += 1

            x_new, y_new = convertZone_n_to_0([x, y], zone)
            d += 2 * dy - 2 * dx
        else:
            x += 1
            x_new, y_new = convertZone_n_to_0([x, y], zone)
            d += 2 * dy

        glPointSize(5)
        glBegin(GL_POINTS)
        glVertex2f(a/1920,b/1080)
        glEnd()

def run(p1,p2):
    dx = p2[0]-p1[0]
    dy = p2[1]-p1[1]
    zone = findZone(p1,p2)
    p1, p2 = convertZone_n_to_0(zone,[p1,p2])
    midPointAlgorithm(p1,p2)

def drawPoints(x,y):
    glPointSize(2)
    #gl.glColor3f(1,.1,.1)
    glBegin(GL_POINTS)
    glVertex2f(x/1920,y/1080)
    glEnd()

def midpoint_circle(X,Y,R):
    D = 1 - R
    x = 0
    y = R

    while x < y:
        if D < 0:
            D = D + 2*x + 3
            x+=1
        else:
            D = D + 2*x -2*y +5
            x+=1
            y-=1

        drawPoints(X+y,Y+x) #Zone 0
        drawPoints(X+x,Y+y) #Zone 1
        drawPoints(X-x,Y+y) #Zone 2
        drawPoints(X-y, Y+x) #Zone 3
        drawPoints(X-y,Y-x) #Zone 4
        drawPoints(X-x,Y-y) #Zone 5
        drawPoints(X+x,Y-y) #Zone 6
        drawPoints(X+y,Y-x) #Zone 7

nosh = input("Enter any number between 1 to 3: ")

numDraw = {
    1: [[[-1300, 750], [-1301, 850]]],
    2: [[[-1350, 400], [-1299, 401]], [[-1351, 350], [-1300, 349]],
        [[-1351, 300], [-1300, 299]], [[-1299, 400], [-1300, 350]],
        [[-1350, 349], [-1349, 299]]],
    3: [[[-1350, -1], [-1299, 0]], [[-1351, -50], [-1300, -49]],
        [[-1351, -101], [-1300, -100]], [[-1299, 0], [-1300, -100]]],
}

def loadDigits(n):
    for i in numDraw:
        if i == int(n):
            for k in numDraw[i]:
                glColor3f(.1,.1,.1)
                run(k[p[0]], k[p[1]])

loadDigits(nosh)

def drawPoint(x,y):
  glVertex2f(x/(800/2),y/(600/2))

def render(): #animate
  img_buf = glReadPixelsub(0, 0, 800, 600, GL_RGB, GL_UNSIGNED_BYTE)
  img = np.frombuffer(img_buf, np.uint8).reshape([600, 800], 3)[::-1]
  img_pil = Image.fromarray(img, 'RGB')
  img_pil.show()


if int(nosh)==3:
    a=300

    p=0.11
    t=9
    for i in range(t):
        glClear(GL_COLOR_BUFFER_BIT)

        t=np.array([[1, 0, a],
                     [0, 1, 0],
                     [0, 0, 1]])

        v1 = np.array([[-151],
                        [250],
                        [1]])


        v2 = np.array([[-150],
                        [1],
                        [1]])


        v3 = np.array([[-900],
                        [0],
                        [1]])

        v4 = np.array([[-901],
                        [251],
                        [1]])

        v5 = np.array([[-700],
                        [0],
                        [1]])


        v6 = np.array([[-400],
                        [0],
                        [1]])

        v11 = np.matmul(t,v1)
        v22 = np.matmul(t,v2)
        v33 = np.matmul(t,v3)
        v44 = np.matmul(t,v4)
        v55 = np.matmul(t,v5)
        v66 = np.matmul(t,v6)

        #for bus
        glColor3f(.05,0.25,1)
        run(v11[[0][0],[1][0]], v22[[0][0],[1][0]])  #right
        run(v22[[0][0],[1][0]], v33[[0][0],[1][0]])  #bottom
        run(v44[[0][0],[1][0]], v11[[0][0],[1][0]])  #up
        run(v44[[0][0],[1][0]], v33[[0][0],[1][0]])  #left
        glColor3f(0.3,0.3,0.3)
        midpoint_circle(v55[0][0], v55[1][0], 80)  #infront
        midpoint_circle(v66[0][0], v66[1][0], 80)  #back

        #shearing of zebra crossing
        s=np.array([[1, p, 0],
                     [0, 1, 0],
                     [0, 0, 1]])

        z9 = np.array([[551],
                        [700],
                        [1]])
        z10 = np.array([[550],
                        [501],
                        [1]])
        z11 = np.array([[0],
                        [500],
                        [1]])

        z12 = np.array([[1],
                        [701],
                        [1]])
        s99 = np.matmul(s,z9)
        s1010 = np.matmul(s,z10)
        s1111 = np.matmul(s,z11)
        s1212 = np.matmul(s,z12)
        glColor3f(1,1,1)
        run(s1212[[0][0],[1][0]], s99[[0][0],[1][0]])  #up
        run(s1010[[0][0],[1][0]], s99[[0][0],[1][0]])  #right
        run(s1111[[0][0],[1][0]], [s1010[0][0],[1][0]]) #bpttom
        run(s1111[[0][0],[1][0]], s1212[[0][0],[1][0]])  #left

        z5 = np.array([[551],
                        [450],
                        [1]])
        z6 = np.array([[550],
                        [251],
                        [1]])
        z7 = np.array([[0],
                        [250],
                        [1]])

        z8 = np.array([[1],
                        [451],
                        [1]])
        s55 = np.matmul(s,z5)
        s66 = np.matmul(s,z6)
        s77 = np.matmul(s,z7)
        s88 = np.matmul(s,z8)
        glColor3f(1,1,1)
        run(s88[[0][0],[1][0]], s55[[0][0],[1][0]]) #up
        run(s66[[0][0],[1][0]], s55[[0][0],[1][0]])  #right
        run(s77[[0][0],[1][0]], s66[[0][0],[1][0]])  #bottom
        run(s77[[0][0],[1][0]], s88[[0][0],[1][0]]) #left

        z1 = np.array([[551],
                        [200],
                        [1]])
        z2 = np.array([[550],
                        [1],
                        [1]])
        z3 = np.array([[0],
                        [0],
                        [1]])

        z4 = np.array([[1],
                        [201],
                        [1]])
        s11 = np.matmul(s,z1)
        s22 = np.matmul(s,z2)
        s33 = np.matmul(s,z3)
        s44 = np.matmul(s,z4)
        glColor3f(1,1,1)
        run(s44[[0][0],[1][0]], s11[[0][0],[1][0]])  #up
        run(s22[[0][0],[1][0]], s11[[0][0],[1][0]])  #right
        run(s33[[0][0],[1][0]], s22[[0][0],[1][0]])  #bottom
        run(s33[[0][0],[1][0]], s44[[0][0],[1][0]])  #left

        z13 = np.array([[551],
                        [-50],
                        [1]])
        z14 = np.array([[550],
                        [-249],
                        [1]])
        z15 = np.array([[0],
                        [-250],
                        [1]])

        z16 = np.array([[1],
                        [-49],
                        [1]])
        s1313 = np.matmul(s,z13)
        s1414 = np.matmul(s,z14)
        s1515 = np.matmul(s,z15)
        s1616 = np.matmul(s,z16)
        glColor3f(1,1,1)
        run(s1616[[0][0],[1][0]], s1313[[0][0],[1][0]])  #up
        run(s1414[[0][0],[1][0]], s1313[[0][0],[1][0]])  #right
        run(s1515[[0][0],[1][0]], s1414[[0][0],[1][0]])  #bottom
        run(s1515[[0][0],[1][0]], s1616[[0][0],[1][0]])  #left

        ##for lightpost
        glColor3f(.211,.211,.211)
        run([-1600, -200], [-1000, -201])   #nicher horizontal line
        run([-1600, 1000], [-1001, 1001])  #uporer horizontal line
        run([-1600, -200], [-1601, 1001])  #  left    vertical line
        run([-1000, -201], [-1001, 1001])   #right vertical line

        X = -1300
        Y = 0
        R = 150
        glColor3f(.1,1,.1) #Green circle
        midpoint_circle(X,Y,R)

        glColor3f(1,1,0.1) #Yellow circle
        midpoint_circle(-1300,400,150)

        glColor3f(1,.1,.1) #Red circle
        midpoint_circle(-1300,800,150)
        i =- 1400
        while i<=-1200:
          glColor3f(.211,.211,.211)
          run(  [i,-1000], [i+1  ,-200])
          i+=20

        #hooman
        glColor3f(1,1,1)
        midpoint_circle(250,-500,100) #Head
        glColor3f(1,1,1)
        run([250, -900], [251, -600]) #body
        run([250,-650], [350,-750]) #left hand
        run([251,-651],[150,-750])  #right hand
        run([250,-867], [350,-967]) #right leg
        run([251,-868],[150,-967])  #left leg

        for i in range(145,0,-5) :
            glColor3f(.1,1,.1)
            midpoint_circle(-1300,0,i)

        #print 3
        loadDigits(nosh)

        render() #animate
        time.sleep(0.9) #animate
        clear_output(wait=True) # refreshes the window
        a=a+200

elif (int(nosh)==1):
  b= 50
  t=15
  p=0.13
  for i in range(t):
        glClear(GL_COLOR_BUFFER_BIT)

        t=np.array([[1, 0, 0],
                     [0, 1, b],
                     [0, 0, 1]])

        v1 = np.array([[250],
                        [-500],
                        [1]])

        v2 = np.array([[251],
                        [-600],
                        [1]])
        v3 = np.array([[250],
                        [-900],
                        [1]])
        v4 = np.array([[350],     #left hand
                        [-750],
                        [1]])
        v5 = np.array([[250],      #left hand
                        [-650],
                        [1]])
        v6 = np.array([[150],     #right hand
                        [-750],
                        [1]])
        v7 = np.array([[251],     #right hand
                        [-651],
                        [1]])
        v8 = np.array([[350],      #right leg
                        [-967],
                        [1]])
        v9 = np.array([[250],      #right leg
                        [-867],
                        [1]])
        vx = np.array([[150],      #left leg
                        [-967],
                        [1]])
        vy = np.array([[251],  # left leg
                       [-868],
                       [1]])

        v11 = np.matmul(t,v1)
        v22 = np.matmul(t,v2)   #body
        v33 = np.matmul(t,v3)   #body
        v44 = np.matmul(t,v4)   #left hand
        v55 = np.matmul(t,v5)   #left hand
        v66 = np.matmul(t,v6)   #right hand
        v77 = np.matmul(t,v7)   #right hand
        v88 = np.matmul(t,v8)   #right leg
        v99 = np.matmul(t,v9)   #right leg
        vxx = np.matmul(t, vx)
        vyy = np.matmul(t, vy)

        glColor3f(0.5,0.5,0.5)
        run(v33[0][0],v33[1][0], v22[0][0],v22[1][0])   #body
        run(v55[0][0],v55[1][0], v44[0][0],v44[1][0])  #left hand
        run(v77[0][0],v77[1][0], v66[0][0],v66[1][0])  #right hand
        run(v99[0][0],v99[1][0], v88[0][0],v88[1][0])  #right leg
        run(vxx[0][0], vxx[1][0], vyy[0][0], vyy[1][0])  # left leg
        midpoint_circle(v11[0][0], v11[1][0], 100)       #head

        #shearing of zebra crossing
        s=np.array([[1, p, 0],
                     [0, 1, 0],
                     [0, 0, 1]])

        z1 = np.array([[551],
                        [200],
                        [1]])
        z2 = np.array([[550],
                        [1],
                        [1]])
        z3 = np.array([[0],
                        [0],
                        [1]])

        z4 = np.array([[1],
                        [201],
                        [1]])
        s11 = np.matmul(s,z1)
        s22 = np.matmul(s,z2)
        s33 = np.matmul(s,z3)
        s44 = np.matmul(s,z4)
        glColor3f(1,1,1)
        run(s44[0][0],s44[1][0], s11[0][0],s11[1][0])
        run(s22[0][0],s22[1][0], s11[0][0],s11[1][0])
        run(s33[0][0],s33[1][0], s22[0][0],s22[1][0])
        run(s33[0][0],s33[1][0], s44[0][0],s44[1][0])

        z5 = np.array([[551],
                        [450],
                        [1]])
        z6 = np.array([[550],
                        [251],
                        [1]])
        z7 = np.array([[0],
                        [250],
                        [1]])

        z8 = np.array([[1],
                        [451],
                        [1]])
        s55 = np.matmul(s,z5)
        s66 = np.matmul(s,z6)
        s77 = np.matmul(s,z7)
        s88 = np.matmul(s,z8)
        glColor3f(1,1,1)
        run(s88[0][0],s88[1][0], s55[0][0],s55[1][0])
        run(s66[0][0],s66[1][0], s55[0][0],s55[1][0])
        run(s77[0][0],s77[1][0], s66[0][0],s66[1][0])
        run(s77[0][0],s77[1][0], s88[0][0],s88[1][0])

        z9 = np.array([[551],
                        [700],
                        [1]])
        z10 = np.array([[550],
                        [501],
                        [1]])
        z11 = np.array([[0],
                        [500],
                        [1]])

        z12 = np.array([[1],
                        [701],
                        [1]])
        s99 = np.matmul(s,z9)
        s1010 = np.matmul(s,z10)
        s1111 = np.matmul(s,z11)
        s1212 = np.matmul(s,z12)
        glColor3f(1,1,1)
        run(s1212[0][0],s1212[1][0], s99[0][0],s99[1][0])
        run(s1010[0][0],s1010[1][0], s99[0][0],s99[1][0])
        run(s1111[0][0],s1111[1][0], s1010[0][0],s1010[1][0])
        run(s1111[0][0],s1111[1][0], s1212[0][0],s1212[1][0])

        z13 = np.array([[551],
                        [-50],
                        [1]])
        z14 = np.array([[550],
                        [-249],
                        [1]])
        z15 = np.array([[0],
                        [-250],
                        [1]])

        z16 = np.array([[1],
                        [-49],
                        [1]])
        s1313 = np.matmul(s,z13)
        s1414 = np.matmul(s,z14)
        s1515 = np.matmul(s,z15)
        s1616 = np.matmul(s,z16)
        glColor3f(1,1,1)
        run(s1616[0][0],s1616[1][0], s1313[0][0],s1313[1][0])
        run(s1414[0][0],s1414[1][0], s1313[0][0],s1313[1][0])
        run(s1515[0][0],s1515[1][0], s1414[0][0],s1414[1][0])
        run(s1515[0][0],s1515[1][0], s1616[0][0],s1616[1][0])


       #blabla
        ##for lightpost
        glColor3f(.211,.211,.211)
        run(-1400, -1000, -1401, -200)   #left vertical of stand
        run(-1200, -1000, -1201, -200)   #right vertical of stand
        run(-1400, -1000, -1200, -1001)   #uporer connected line
        glColor3f(.211,.211,.211)
        run(-1600, -200, -1000, -201)   #nicher horizontal line
        run(-1600, 1000, -1001, 1001)  #uporer horizontal line
        run(-1600, -200, -1601, 1001)  #  left    vertical line
        run(-1000, -201, -1001, 1001)   #right vertical line


        X = -1300
        Y = 0
        R = 150
        glColor3f(.1,1,.1) #Green circle
        midpoint_circle(X,Y,R)

        glColor3f(1,1,0.1) #Yellow circle
        midpoint_circle(-1300,400,150)

        glColor3f(1,.1,.1) #Red circle
        midpoint_circle(-1300,800,150)
        i =- 1400
        while i<=-1200:
          glColor3f(.211,.211,.211)
          run(  i,-1000, i+1  ,-200)
          i+=20

        #Vehicle
        glColor3f(.05,0.25,1)
        run(-900, 0, -901, 251)
        run(-150, 1, -151, 250)
        run(-900, 0, -150, 1,)
        run(-901, 251, -151, 250)
        glColor3f(.05,0.25,1)
        midpoint_circle(-700,0,80)
        midpoint_circle(-400,0,80)

        if int(nosh)==1:

          for i in range(145,0,-5) :
              glColor3f(1,.1,.1)
              midpoint_circle(-1300,800,i)

        #print 1 or print 2
        loadDigits(nosh)

        render() #animate
        time.sleep(0.7) #animate
        clear_output(wait=True) #refreshes the window
        b=b+170


elif(int(nosh)==2):
  p=0.13
  c=100
  glClear(GL_COLOR_BUFFER_BIT)

  t=np.array([[1, 0, c],
              [0, 1, 0],
              [0, 0, 1]])

  v1 = np.array([[-151],
                  [250],
                  [1]])


  v2 = np.array([[-150],
                  [1],
                  [1]])


  v3 = np.array([[-900],
                  [0],
                  [1]])

  v4 = np.array([[-901],
                  [251],
                  [1]])

  v5 = np.array([[-700],
                  [0],
                  [1]])


  v6 = np.array([[-400],
                  [0],
                  [1]])

  v11 = np.matmul(t,v1)
  v22 = np.matmul(t,v2)
  v33 = np.matmul(t,v3)
  v44 = np.matmul(t,v4)
  v55 = np.matmul(t,v5)
  v66 = np.matmul(t,v6)


  glColor3f(.05,0.25,1)

  run(v11[0][0],v11[1][0], v22[0][0],v22[1][0])
  run(v22[0][0],v22[1][0], v33[0][0],v33[1][0])
  run(v44[0][0],v44[1][0], v11[0][0],v11[1][0])
  run(v44[0][0],v33[1][0], v33[0][0],v44[1][0])
  midpoint_circle(v55[0][0], v55[1][0], 80)
  midpoint_circle(v66[0][0], v66[1][0], 80)

  #shearing of zebra crossing
  s=np.array([[1, p, 0],
                [0, 1, 0],
                [0, 0, 1]])

  z1 = np.array([[551],
                  [200],
                  [1]])
  z2 = np.array([[550],
                  [1],
                  [1]])
  z3 = np.array([[0],
                  [0],
                  [1]])

  z4 = np.array([[1],
                  [201],
                  [1]])
  s11 = np.matmul(s,z1)
  s22 = np.matmul(s,z2)
  s33 = np.matmul(s,z3)
  s44 = np.matmul(s,z4)
  glColor3f(1,1,1)
  run(s44[0][0],s44[1][0], s11[0][0],s11[1][0])
  run(s22[0][0],s22[1][0], s11[0][0],s11[1][0])
  run(s33[0][0],s33[1][0], s22[0][0],s22[1][0])
  run(s33[0][0],s33[1][0], s44[0][0],s44[1][0])

  z5 = np.array([[551],
                  [450],
                  [1]])
  z6 = np.array([[550],
                  [251],
                  [1]])
  z7 = np.array([[0],
                  [250],
                  [1]])

  z8 = np.array([[1],
                  [451],
                  [1]])
  s55 = np.matmul(s,z5)
  s66 = np.matmul(s,z6)
  s77 = np.matmul(s,z7)
  s88 = np.matmul(s,z8)
  glColor3f(1,1,1)
  run(s88[0][0],s88[1][0], s55[0][0],s55[1][0])
  run(s66[0][0],s66[1][0], s55[0][0],s55[1][0])
  run(s77[0][0],s77[1][0], s66[0][0],s66[1][0])
  run(s77[0][0],s77[1][0], s88[0][0],s88[1][0])


  z9 = np.array([[551],
                  [700],
                  [1]])
  z10 = np.array([[550],
                  [501],
                  [1]])
  z11 = np.array([[0],
                  [500],
                  [1]])

  z12 = np.array([[1],
                  [701],
                  [1]])
  s99 = np.matmul(s,z9)
  s1010 = np.matmul(s,z10)
  s1111 = np.matmul(s,z11)
  s1212 = np.matmul(s,z12)
  glColor3f(1,1,1)
  run(s1212[0][0],s1212[1][0], s99[0][0],s99[1][0])
  run(s1010[0][0],s1010[1][0], s99[0][0],s99[1][0])
  run(s1111[0][0],s1111[1][0], s1010[0][0],s1010[1][0])
  run(s1111[0][0],s1111[1][0], s1212[0][0],s1212[1][0])

  z13 = np.array([[551],
                  [-50],
                  [1]])
  z14 = np.array([[550],
                  [-249],
                  [1]])
  z15 = np.array([[0],
                  [-250],
                  [1]])

  z16 = np.array([[1],
                  [-49],
                  [1]])
  s1313 = np.matmul(s,z13)
  s1414 = np.matmul(s,z14)
  s1515 = np.matmul(s,z15)
  s1616 = np.matmul(s,z16)
  glColor3f(1,1,1)
  run(s1616[0][0],s1616[1][0], s1313[0][0],s1313[1][0])
  run(s1414[0][0],s1414[1][0], s1313[0][0],s1313[1][0])
  run(s1515[0][0],s1515[1][0], s1414[0][0],s1414[1][0])
  run(s1515[0][0],s1515[1][0], s1616[0][0],s1616[1][0])

  #blabla
  ##for lightpost
  glColor3f(.211,.211,.211)
  run(-1400, -1000, -1401, -200)   #left vertical of stand
  run(-1200, -1000, -1201, -200)   #right vertical of stand
  run(-1400, -1000, -1200, -1001)   #uporer connected line
  glColor3f(.211,.211,.211)
  run(-1600, -200, -1000, -201)   #nicher horizontal line
  run(-1600, 1000, -1001, 1001)  #uporer horizontal line
  run(-1600, -200, -1601, 1001)  #  left    vertical line
  run(-1000, -201, -1001, 1001)   #right vertical line


  X = -1300
  Y = 0
  R = 150
  glColor3f(.1,1,.1) #Green circle
  midpoint_circle(X,Y,R)

  glColor3f(1,1,0.1) #Yellow circle
  midpoint_circle(-1300,400,150)

  glColor3f(1,.1,.1) #Red circle
  midpoint_circle(-1300,800,150)
  i=-1400
  while i<=-1200:
    glColor3f(.211,.211,.211)
    run(  i,-1000, i+1  ,-200)
    i+=20

  #Person
  glColor3f(1,1,1)
  midpoint_circle(250,-500,100) #Head
  glColor3f(1,1,1)
  run(250, -900, 251, -600) #body
  run(250,-650, 350,-750) #left hand
  run(251,-651,150,-750)  #right hand
  run(250,-867, 350,-967) #right leg
  run(251,-868,150,-967)  #left leg

  for i in range(145,0,-5) :
    glColor3f(1,1,.1)
    midpoint_circle(-1300,400,i)

  #print 2
  loadDigits(nosh)

  render() #animate
  time.sleep(0.7) #animate
  clear_output(wait=True) #this actually refreshes the window

render()