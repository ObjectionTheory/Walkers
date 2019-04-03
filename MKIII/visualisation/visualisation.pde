float L1 = 88;
float L2 = 91;
float L3 = 47;
float L4 = 90;
float A = 28;
float B = 103;
float D = 25;
float Dang = 23.6;

float angle1 = 0;
float angle2 = 60;

PVector p1 = new PVector(0, 0);
PVector p2 = new PVector(0, 0);
PVector p3 = new PVector(-10, 23.5);
PVector p4 = new PVector(0, 0);
PVector p5 = new PVector(0, 0);
PVector p6 = new PVector(0, 0);
PVector temp1;
PVector temp2;

void findP2(float angle) {
  p2.x = L1 * cos(radians(-angle)) + p1.x;
  p2.y = L1 * sin(radians(-angle)) + p1.y;
}

void findP4(float angle) {
  p4.x = A * cos(radians(angle)) + p3.x;
  p4.y = A * sin(radians(angle)) + p3.y;
}

void findP5() {
  
  PVector P2 = p2.copy();
  PVector P4 = p4.copy();
  float d = dist(P2.x, P2.y, P4.x, P4.y);
  println(d);
  float a = (sq(L3) - sq(B) + sq(d)) / (2*d);
  float h = sqrt(sq(L3) - sq(a));
  float px = P2.x + a * (P4.x-P2.x)/d;
  float py = P2.y + a * (P4.y-P2.y)/d;
  PVector vect1 = new PVector(px + h*(P4.y - P2.y)/d,
                              py - h*(P4.x-P2.x)/d
                              ); 
  PVector vect2 = new PVector(px - h*(P4.y - P2.y)/d,
                              py + h*(P4.x-P2.x)/d
                              );
  //println(P2.x == p2.x, P4.x ==p4.x);                           
  ellipse(p2.x, p2.y, 10, 10);
  ellipse(p4.x, p4.y, 10, 10);
                         
  temp1 = vect1;
  temp2 = vect2;

  if (vect1.y > vect2.y) {
    p5 = vect1.copy();
  } else {
    p5 = vect2.copy();
  }
  
}

void findP6() {
  float len = sqrt(sq(p2.x - p5.x) + sq(p2.y - p5.y));
  float dx = (p2.x-p5.x)/len;
  float dy = (p2.y-p5.y)/len;
  p6.x = p2.x + L4 * dx;
  p6.y = p2.y + L4 * dy;
  
}


void setup() {
  size(400, 400, P3D);
  
}

void draw() {
  background(255);
  strokeWeight(3);
  pushMatrix();

  translate(100, 200);
  translate(50, 0);
  rotateX(PI);
  findP2(angle1);
  findP4(angle2);
  findP5();
  findP6();
  

  stroke(255, 0, 0);
  line(p1.x, p1.y, p2.x, p2.y);
  stroke(255, 0, 0);
  line(p3.x, p3.y, p4.x, p4.y);
  stroke(0, 255, 0);
  line(p4.x, p4.y, p5.x, p5.y);
  //line(p4.x, p4.y, p2.x, p2.y);
  stroke(0, 0, 255);
  line(p2.x, p2.y, p6.x, p6.y);
  line(p5.x, p5.y, p2.x, p2.y);
  
  stroke(0);
  strokeWeight(0.5);
  //ellipse(p3.x, p3.y, A*2, A*2);
  //ellipse(p1.x, p1.y, L1*2, L1*2);
  ellipse(p4.x, p4.y, B*2, B*2);
  ellipse(p2.x, p2.y, L3*2, L3*2);
  ellipse(p5.x, p5.y, 10, 10);
  //ellipse(temp1.x, temp1.y, 20, 20);
  //ellipse(temp2.x, temp2.y, 20, 20);
 
  popMatrix();
  
  if (keyPressed) {
   if (key == 's') {
      angle1 ++; 
   }
   if (key == 'w') {
      angle1 --; 
   }
   if (key == 'd') {
      angle2 ++; 
   }
   if (key == 'a') {
      angle2 --; 
   }
  }
  println(p6.x, p6.y, 180-angle1, angle2+90);
}
