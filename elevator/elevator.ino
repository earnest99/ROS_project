const int bt3_up = A0;
const int bt3_down = A1;
const int bt2_up = A2;
const int bt2_down = A3;
const int bt1_up = A4;
const int bt1_down = A5;
const int led3 = 7;
const int led2 = 4;
const int led1 = 1;
const int led12_1 = 2;
const int led12_2 = 3;
const int led23_1 = 5;
const int led23_2 = 6;
const int led3_up = 13;
const int led3_down = 12;
const int led2_up = 11;
const int led2_down = 10;
const int led1_up = 9;
const int led1_down = 8;

const int threshold = 500;
int elevator = 1;

//현재 층 led on
void here(){
  if (elevator == 2){
    digitalWrite(led2, HIGH);
  }
  else if (elevator == 3){
    digitalWrite(led3, HIGH);
  }
  else{
    digitalWrite(led1, HIGH);
  }
}
unsigned long startTime = 0;  

int move_up(int from) {
  if (from == 1) { // 1층에서 3층
    digitalWrite(led1, LOW);

    startTime = millis();  // 이동 시작 시간 기록

    while (millis() - startTime < 500) {
      
      if (digitalRead(bt2_up)) {
        digitalWrite(led2_up, HIGH);
        digitalWrite(led12_1, HIGH);
        delay(500);
        digitalWrite(led12_1, LOW);
        delay(500);
        digitalWrite(led12_2, HIGH);
        delay(500);
        digitalWrite(led12_2, LOW);
        delay(500);
        digitalWrite(led2, HIGH);
        delay(500);
        arrive(2);
        return move_up(2);
      }
    }

    digitalWrite(led12_1, HIGH);
    delay(500);
    digitalWrite(led12_1, LOW);

    startTime = millis();  // 이동 시작 시간 기록

    while (millis() - startTime < 500) {
      if (digitalRead(bt2_up)) {
        digitalWrite(led2_up, HIGH);
        digitalWrite(led12_2, HIGH);
        delay(500);
        digitalWrite(led12_2, LOW);
        delay(500);
        digitalWrite(led2, HIGH);
        delay(500);
        arrive(2);
        return move_up(2);
     }
    }

    digitalWrite(led12_2, HIGH);
    delay(500);
    digitalWrite(led12_2, LOW);
  

  startTime = millis();  // 이동 시작 시간 기록

  while (millis() - startTime < 500) {
    if (digitalRead(bt2_up)) {
      digitalWrite(led2_up, HIGH);
      digitalWrite(led2, HIGH);
      delay(500);
      arrive(2);
      return move_up(2);
    }
  }
    digitalWrite(led2, HIGH);
    delay(500);
    digitalWrite(led2, LOW);
    delay(500);
    digitalWrite(led23_1, HIGH);
    delay(500);
    digitalWrite(led23_1, LOW);
    delay(500);
    digitalWrite(led23_2, HIGH);
    delay(500);
    digitalWrite(led23_2, LOW);
    delay(500);
    digitalWrite(led3, HIGH);
  } else if (from == 2) { // 2층에서 3층
    digitalWrite(led2_up, LOW);
    digitalWrite(led2, LOW);
    delay(500);
    digitalWrite(led23_1, HIGH);
    delay(500);
    digitalWrite(led23_1, LOW);
    delay(500);
    digitalWrite(led23_2, HIGH);
    delay(500);
    digitalWrite(led23_2, LOW);
    delay(500);
    digitalWrite(led3, HIGH);
  }
  return 3; // 도착층
}

//엘베 내려가기

int move_down(int from) {
  if (from == 3) { // 3층에서 1층
    digitalWrite(led3, LOW);

    startTime = millis();  // 이동 시작 시간 기록

    while (millis() - startTime < 500) {
      if (digitalRead(bt2_down)) {
        digitalWrite(led2_down, HIGH);
        digitalWrite(led23_2, HIGH);
        delay(500);
        digitalWrite(led23_2, LOW);
        delay(500);
        digitalWrite(led23_1, HIGH);
        delay(500);
        digitalWrite(led23_1, LOW);
        delay(500);
        digitalWrite(led2, HIGH);
        delay(500);
        arrive(2);
        return move_down(2);
      }
    }

    digitalWrite(led23_2, HIGH);
    delay(500);
    digitalWrite(led23_2, LOW);

    startTime = millis();  // 이동 시작 시간 기록

    while (millis() - startTime < 500) {
      if (digitalRead(bt2_down)) {
        digitalWrite(led2_down, HIGH);
        digitalWrite(led23_1, HIGH);
        delay(500);
        digitalWrite(led23_1, LOW);
        delay(500);
        digitalWrite(led2, HIGH);
        delay(500);
        arrive(2);
        return move_down(2);
      }
    }

    digitalWrite(led23_1, HIGH);
    delay(500);
    digitalWrite(led23_1, LOW);

    startTime = millis();  // 이동 시작 시간 기록

    while (millis() - startTime < 500) {
      if (digitalRead(bt2_down)) {
        digitalWrite(led2_down, HIGH);
        digitalWrite(led2, HIGH);
        delay(500);
        arrive(2);
        return move_down(2);
      }
    }

    digitalWrite(led2, HIGH);
    delay(500);
    digitalWrite(led2, LOW);
    delay(500);
    digitalWrite(led12_2, HIGH);
    delay(500);
    digitalWrite(led12_2, LOW);
    delay(500);
    digitalWrite(led12_1, HIGH);
    delay(500);
    digitalWrite(led12_1, LOW);
    delay(500);
    digitalWrite(led1, HIGH);
  } else if (from == 2) { // 2층에서 1층
    digitalWrite(led2_down, LOW);
    digitalWrite(led2, LOW);
    delay(500);
    digitalWrite(led12_2, HIGH);
    delay(500);
    digitalWrite(led12_2, LOW);
    delay(500);
    digitalWrite(led12_1, HIGH);
    delay(500);
    digitalWrite(led12_1, LOW);
    delay(500);
    digitalWrite(led1, HIGH);
  }
  return 1; // 도착층
}

//현재 층으로 엘베 부르기
void come(int floor){
  // 아래층에서 호출할 때
  if (elevator > floor){
    int h = elevator - floor;
    if(h == 1){ //1개의 층 이동
      digitalWrite(led3, LOW);
      delay(500);
      digitalWrite(led23_2, HIGH);
      delay(500);
      digitalWrite(led23_2, LOW);
      delay(500);
      digitalWrite(led23_1, HIGH);
      delay(500);
      digitalWrite(led23_1, LOW);
      delay(500);
      digitalWrite(led2, HIGH);
    }
    else if (h == 2){
      move_down(3); //2개의 층 이동
    }
   delay(500);
  }
  //윗층에서 호출할 때
  else if (elevator < floor){
    int h = floor - elevator;
    if(h == 1){ //1개의 층 이동
    digitalWrite(led1, LOW);
    delay(500);
    digitalWrite(led12_1, HIGH);
    delay(500);
    digitalWrite(led12_1, LOW);
    delay(500);
    digitalWrite(led12_2, HIGH);
    delay(500);
    digitalWrite(led12_2, LOW);
    delay(500);
    digitalWrite(led2, HIGH);
    }
    else if (h == 2){
      move_up(1); //2개의 층 이동
    }
   delay(2000);
  }
  elevator = floor; //도착 층을 현재 층으로 업데이트
  
}

void arrive(int n){
  switch(n){
    case 1:
      delay(300);
      digitalWrite(led1, LOW);
      delay(300);
      digitalWrite(led1, HIGH);
      delay(300);
      digitalWrite(led1, LOW);
      delay(300);
      digitalWrite(led1, HIGH);
      delay(300);
      break;
    case 2:
      delay(300);
      digitalWrite(led2, LOW);
      delay(300);
      digitalWrite(led2, HIGH);
      delay(300);
      digitalWrite(led2, LOW);
      delay(300);
      digitalWrite(led2, HIGH);
      delay(300);
      break;
    case 3:
      delay(300);
      digitalWrite(led3, LOW);
      delay(300);
      digitalWrite(led3, HIGH);
      delay(300);
      digitalWrite(led3, LOW);
      delay(300);
      digitalWrite(led3, HIGH);
      delay(300);
      break;
  }
}

void setup() {
  //버튼
  pinMode(bt3_up, INPUT);
  pinMode(bt3_down, INPUT);
  pinMode(bt2_up, INPUT);
  pinMode(bt2_down, INPUT);
  pinMode(bt1_up, INPUT);
  pinMode(bt1_down, INPUT);
  //초록 현재 층
  pinMode(led3, OUTPUT);
  pinMode(led2, OUTPUT);
  pinMode(led1, OUTPUT);
  //노랑 엘베움직임
  pinMode(led12_1, OUTPUT);
  pinMode(led12_2, OUTPUT);
  pinMode(led23_1, OUTPUT);
  pinMode(led23_2, OUTPUT);
  //파랑 버튼led
  pinMode(led3_up, OUTPUT);
  pinMode(led3_down, OUTPUT);
  pinMode(led2_up, OUTPUT);
  pinMode(led2_down, OUTPUT);
  pinMode(led1_up, OUTPUT);
  pinMode(led1_down, OUTPUT);
}

void loop() {
  here(); //현재 위치 led on
  if (analogRead(bt1_up) > threshold) {
    
    digitalWrite(led1_up, HIGH);
    delay(100);

    come(1); //1층 호출
    //깜빡임
    arrive(1);
    digitalWrite(led1_up, LOW);

    elevator = move_up(elevator);
    
  } 
  else if (analogRead(bt1_down) > threshold) {
    
    digitalWrite(led1_down, HIGH);
    delay(100);

    come(1); //1층 호출

    digitalWrite(led1_down, LOW);
  }

  else if (analogRead(bt2_up) > threshold) {
    
    digitalWrite(led2_up, HIGH);
    delay(100);

    come(2); //2층 호출
    //깜빡임
    arrive(2);
    digitalWrite(led2_up, LOW);

    elevator = move_up(elevator);
    
  } 
  else if (analogRead(bt2_down) > threshold) {
    
    digitalWrite(led2_down, HIGH);
    delay(100);

    come(2); //2층 호출
    //깜빡임
    arrive(2);
    digitalWrite(led2_down, LOW);
    
    elevator = move_down(elevator);
    
  } 
  

  else if (analogRead(bt3_up) > threshold) {
    
    digitalWrite(led3_up, HIGH);
    delay(100);
    
    come(3); //3층 호출

    digitalWrite(led3_up, LOW);

    }
  
  else if (analogRead(bt3_down) > threshold) {
    
    digitalWrite(led3_down, HIGH);
    delay(100);

    come(3); //3층 호출
    //깜빡임
    arrive(3);
    digitalWrite(led3_down, LOW);
    elevator = move_down(elevator);
    
  } 
}
