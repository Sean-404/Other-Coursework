PImage img;
Table table;
PShape map;
float rotx = PI/4;
float roty = PI/4;
float zoom = 1;
float camX = 0;
float camY = 0;
int state;
boolean zoomed = false;

void setup(){
 size(1920,1080,P3D);
  table = loadTable("Data.csv","header");
  img = loadImage("uk-admin.jpg");
  rectMode(CENTER);
  //2448 2802
  map = createShape(RECT,0,0,2448,2802);
  map.setTexture(img);
}

void textDisplay(){
  text("1 = Population 1991",-1200,-1300,5);
  text("2 = Population 2001",-1200,-1200,5);
  text("3 = Population 2011",-1200,-1100,5);
  text("Use arrow keys to move image",-1200,-1000,5);
  text("Scroll up and down to zoom in and out",-1200,-900,5);
  text("Hold mouse to rotate image",-1200,-800,5);
  text("Double click to zoom in and out",-1200,-700,5);
}

void draw(){
  background(168,205,234);
  rotateX(rotx);
  rotateY(roty);
  
  textSize(50);
  fill(0,0,0);
  
  textDisplay();
  
  shape(map);
  translate(-1224,-1401);
  
  for (TableRow row : table.rows()){
    int no = row.getInt("No");
    String city = row.getString("City");

    String x1991 = row.getString("1991");
    String y1991 = x1991.replace(",","").replace("...","0");
    int pop1991 = Integer.parseInt(y1991);

    String x2001 = row.getString("2001");
    String y2001 = x2001.replace(",","").replace("...","0");
    int pop2001 = Integer.parseInt(y2001);

    String x2011 = row.getString("2011");
    String y2011 = x2011.replace(",","").replace("...","0");
    int pop2011 = Integer.parseInt(y2011);

    int x = row.getInt("xPos");
    int y = row.getInt("yPos");
    
    int pop1991small = pop1991/1000;
    int pop2001small = pop2001/1000;
    int pop2011small = pop2011/1000;
    
    if(state == 0){
      createBar(pop1991small,20,x,y,city);
    }else if(state == 1){
      createBar(pop2001small,20,x,y,city);
    }else if(state == 2){
      createBar(pop2011small,20,x,y,city);
    }
    
  }
  camera(camX, camY, (height*0.5)/tan(PI/6)*zoom, camX, camY,0,0,1,0);
}

void createBar(int h, float w, float x, float y, String city){
  float mappedPop = map(h,0,1,0,1);
  fill(255,0,0,mappedPop);
  
  pushMatrix();
  float boxHeight = h;
  translate(x,y,boxHeight/2);
  box(w,w,boxHeight);
  popMatrix();

  fill(78);
  textSize(20);
  text(city, x+w, y+(w/2),5);
}

void mouseDragged(){
  float speed = 0.01;
  rotx += (pmouseY - mouseY) * speed;
  roty += (mouseX - pmouseX) * speed;
}

void mouseWheel(MouseEvent event){
  float e = event.getCount();
  zoom += e;
}

void mouseClicked(MouseEvent event){
  if (event.getCount() == 2 && zoomed == false){
    zoomIn();
    zoomed = true;
  }
  else if (event.getCount() == 2 && zoomed == true){
    zoomOut();
    zoomed = false;
  }
}

void zoomIn(){
  zoom -= 3;
}

void zoomOut(){
  zoom += 3;
}

void keyPressed(){
  if (key==CODED){
    if(keyCode == UP){
      camY-=100;
    } else if(keyCode == DOWN){
      camY+=100;
    } else if(keyCode == LEFT){
      camX-=100;
    } else if(keyCode == RIGHT){
      camX+=100;
    }
  }
  if(keyPressed){
    if(key == '1'){
      state = 0;
      return;
    }
    else if(key == '2'){
      state = 1;
      return;
    }
    else if(key == '3'){
      state = 2;
      return;
    }
  }
}
