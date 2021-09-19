#include <Servo.h>

Servo myservo;
#define MR_Ctrl 13
#define MR_PWM 11
#define ML_Ctrl 12
#define ML_PWM 3
#define S_Down 90
#define S_Up 0
#define Sub_Arr_Size 4

int inputarray[4][4] = {{10,10,20,20},{20,20,60,30},{60,30,20,10},{30,20,50,20}};
int **pos;

void turn(int direction, int time){      //1 for left (ccw), 2 for right (cw)

    if (direction == 1)
    {
        digitalWrite(ML_Ctrl, HIGH);
        analogWrite(ML_PWM, 200);
        digitalWrite(MR_Ctrl, HIGH);
        analogWrite(MR_PWM, 200);
        delay(600);
        analogWrite(ML_PWM, 0);
        analogWrite(MR_PWM, 0);
        delay(500);
        digitalWrite(ML_Ctrl, LOW);
        analogWrite(ML_PWM, 200);
        digitalWrite(MR_Ctrl, HIGH);
        analogWrite(MR_PWM, 200);
        delay(time);
        analogWrite(ML_PWM, 0);
        analogWrite(MR_PWM, 0);
        delay(500);
        digitalWrite(ML_Ctrl, LOW);
        analogWrite(ML_PWM, 200);
        digitalWrite(MR_Ctrl, LOW);
        analogWrite(MR_PWM, 200);
        delay(600);
        analogWrite(ML_PWM, 0);
        analogWrite(MR_PWM, 0);
        delay(500);
    }
    else if (direction == 2)
    {
        digitalWrite(ML_Ctrl, HIGH);
        analogWrite(ML_PWM, 200);
        digitalWrite(MR_Ctrl, HIGH);
        analogWrite(MR_PWM, 200);
        delay(600);
        analogWrite(ML_PWM, 0);
        analogWrite(MR_PWM, 0);
        delay(500);
        digitalWrite(ML_Ctrl, HIGH);
        analogWrite(ML_PWM, 200);
        digitalWrite(MR_Ctrl, LOW);
        analogWrite(MR_PWM, 200);
        delay(time);
        analogWrite(ML_PWM, 0);
        analogWrite(MR_PWM, 0);
        delay(500);
        digitalWrite(ML_Ctrl, LOW);
        analogWrite(ML_PWM, 200);
        digitalWrite(MR_Ctrl, LOW);
        analogWrite(MR_PWM, 200);
        delay(600);
        analogWrite(ML_PWM, 0);
        analogWrite(MR_PWM, 0);
        delay(500);
    }
    return;
}

void drive(int direction, int time){        //1 for fwd, 0 for bkwd
    if (direction == 1)
    {
        digitalWrite(ML_Ctrl, HIGH);
        analogWrite(ML_PWM, 200);
        digitalWrite(MR_Ctrl, HIGH);
        analogWrite(MR_PWM, 200);
        delay(time);
        analogWrite(ML_PWM, 0);
        analogWrite(MR_PWM, 0);
        delay(100);
    }
    else if (direction == 0)
    {
        digitalWrite(ML_Ctrl, LOW);
        analogWrite(ML_PWM, 200);
        digitalWrite(MR_Ctrl, LOW);
        analogWrite(MR_PWM, 200);
        delay(time);
        analogWrite(ML_PWM, 0);
        analogWrite(MR_PWM, 0);
        delay(100);
    }
    
    
}


void setup(){
    myservo.attach(8);
    pinMode(ML_Ctrl, OUTPUT);
    pinMode(ML_PWM, OUTPUT);
    pinMode(MR_Ctrl, OUTPUT);
    pinMode(MR_PWM, OUTPUT);

}

//place at 0,0 facing x axis, with pen up
void loop(){
    delay(100);
    myservo.write(S_Down);
    delay(100);

    int arraysize = 45;

    //int inarray[45][4] = {{481, 129, 696, 436}, {476, 476, 903, 400}, {861, 674, 961, 399}, {230, 409, 466, 137}, {186, 706, 444, 746}, {330, 293, 474, 127}, {522, 737, 723, 697}, {39, 518, 107, 694}, {590, 730, 811, 684}, {243, 719, 457, 752}, {57, 414, 232, 408}, {671, 399, 898, 391}, {482, 129, 672, 400}, {1, 421, 80, 626}, {112, 699, 310, 730}, {17, 415, 233, 407}, {11, 419, 200, 445}, {491, 750, 674, 712}, {204, 440, 374, 244}, {854, 676, 904, 539}, {679, 705, 850, 671}, {108, 694, 299, 724}, {642, 68, 744, 50}, {558, 93, 634, 70}, {742, 428, 958, 389}, {590, 8, 677, 25}, {681, 26, 744, 46}, {522, 4, 582, 7}, {452, 751, 561, 730}, {500, 118, 559, 93}, {856, 669, 904, 538}, {815, 684, 860, 674}, {476, 753, 566, 734}, {475, 6, 547, 4}, {605, 10, 662, 21}, {776, 692, 836, 679}, {455, 590, 492, 601}, {468, 133, 502, 118}, {201, 444, 229, 413}, {827, 675, 864, 668}, {669, 707, 732, 695}, {470, 596, 501, 587}, {474, 6, 474, 475}, {874, 391, 957, 389}, {370, 734, 463, 748}};
    int inarray[4][4] = {{100, 100, 200, 200},{200, 200, 600, 300},{600, 300, 200, 100}, {300, 200, 500, 200}};
    int **arr = (int **)malloc(arraysize * sizeof(int *));
    for (int i=0; i<arraysize; i++)
        arr[i] = (int *)malloc(Sub_Arr_Size * sizeof(int));

    for (int i = 0; i <  arraysize; i++){
        for (int j = 0; j < Sub_Arr_Size; j++){
            arr[i][j] = inarray[i][j] / 10;
        }
    }


    float initialAngle = atan(arr[0][0]/arr[0][1]);       //go to first point
    float initialMagniture = hypot(arr[0][0],arr[0][1]);
    int initialangtime = abs((int)(2000*initialAngle/3.1415));
    int initialdrivetime = abs((int)(initialMagniture*50));
    myservo.write(S_Up);
    delay(2000);
    turn(1, initialangtime); //since we are at origin and facing +x, angle will always be >=0
    drive(1, initialdrivetime);
    turn(2, initialangtime);
    for (int i = 0; i < arraysize; i++)
    {
        int deltax = arr[i][2] - arr[i][0];
        int deltay = arr[i][3] - arr[i][1];
        float magnitude = hypot(deltax, deltay);
        float angle = atan(deltay/deltax);
        int angtime = abs((int)(2000*angle/3.1415));
        int drivetime = abs((int)(magnitude*50));
        if (angle >= 0)      //turn to direction and drive
        {
            turn(1, angtime);
        }
        else if (angle < 0)
        {
            turn(2, angtime);
        }
        
        myservo.write(S_Down);
        delay(1000);
        drive(1, drivetime);
        myservo.write(S_Up);
        delay(1000);
        if (angle < 0)      //turn back to horizontal
        {
            turn(1, angtime);
        }
        else if (angle >= 0)
        {
            turn(2, angtime);
        }

        //if not last point, go to next point
        if (i < (arraysize-1)){
            int deltax2 = arr[i+1][0] - arr[i][2];
            int deltay2 = arr[i+1][1] - arr[i][3];
            float magnitude2 = hypot(deltax2, deltay2);
            float angle2 = atan(deltay2/deltax2);
            int angtime2 = abs((int)(2000*angle2/3.1415));
            int drivetime2 = abs((int)(magnitude2*50));
            if (angle >= 0) //turn to direction and drive
            {
                turn(1, angtime);
            }
            else if (angle < 0)
            {
                turn(2, angtime);
            }

            drive(1, drivetime2);

            if (angle >= 0) //turn to direction and drive
            {
                turn(1, angtime);
            }
            else if (angle < 0)
            {
                turn(2, angtime);
            }
        }
    }
    while (true)
    {
        analogWrite(ML_PWM, 0);
        analogWrite(MR_PWM, 0);
    }
  
}