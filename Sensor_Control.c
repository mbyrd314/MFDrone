#include "Sensor_Control.h"
#include "ir_align.c"


pthread_mutex_t mutex_distance;
pthread_mutex_t mutex_orientation;

pthread_cond_t condvar;
pthread_cond_t condvar_orientation;


//Global shared variables, mutex protected
int distance = 0;                  //Indicates if the drone is within range for activation to be initialized
int orientation = 0;              // Indicates if drone is in the correct rotational orientation
int temp_dist = MAX_DISTANCE;  //Maximum distance before actuation will be triggered
int temp_min_dist = MIN_DISTANCE //Minimum distance needed to be maintained between payload and refueling drone

//Runs distance protocols for ultrasonic sensors based on sensor location.
void *dist_detect(void *zgpio){
    printf("Beginning distance detection protocol \n");
    double dist = 2000;
    struct gpio_pins *p_gpio = (struct gpio_pins *) zgpio;
    double prev_state = 0;                               //Last distance read by sensor

    sensor_init(p_gpio);
    printf("Initialization complete\n");

    while(1){
        dist = distance(p_gpio);

        if (dist < 1) {
            dist = prev_state;
        }

        usleep(100000);
        printf("dist: %f\n sensor: %d\n", dist, p_gpio->checker);

        //writes to shared variable if distance is unsafe in front of car
        if(dist < MAX_DISTANCE){
            pthread_mutex_lock(&mutex_distance);
            distance = 1;
            pthread_cond_broadcast(&condvar);
            pthread_mutex_unlock(&mutex_distance);
        }
        else{
            pthread_mutex_lock(&mutex_distance);
            distance = 0;
            pthread_cond_broadcast(&condvar);
            pthread_mutex_unlock(&mutex_distance);
        }
        prev_state = dist;
    }
    return NULL;
}

// TODO: Change from reading from android to sending to android app
//Reads in user input from Android App. Determines which sensors need to be checked for safety
void *User(void *p_socket){
    int BLT_client[2];
    init_BLT_sock(BLT_client);
    char message[1024];
    while(1){

    }
    BLT_end(BLT_client);
}

//Runs IR detection protocol and adjusts drone as necessary
void *ir_detect(){

    int a_size = 4;
    int pinout[] = {2,3,4,17};
    int ir_status[a_size];
    long i;
    int allstate;

   // initialize IR sensors
    initialize_ir(pinout, a_size); 
   
   // Determine if IR sensors are aligned or not
    while(True) {
        allstate = read_ir(pinout,a_size,ir_status);

       //  printf("%d\n", allstate);
 
        if (allstate == a_size){
            printf("YOU GOT A MATCH! CONGRATS!!!!\n");
            printf("Begin actuation");
            pthread_mutex_lock(&mutex_orientation);
            orientation = 1;
            pthread_cond_broadcast(&condvar_orientation);
            pthread_mutex_unlock(&mutex_orientation);    
        }
        else if(i%100 == 0){
             print_state(ir_status, a_size);
             printf("Rotate clockwise")
        }
       i++;
   }
   return 0
       
}

void *actuation_protocol(){
    pthread_mutex_lock(&mutex_orientation)
    while(!orientation){
        pthread_cond_wait(&condvar_orientation, &mutex_orientation);
     }

    pthread_mutex_lock(&mutex_distance);
    while(!distance){
        pthread_cond_wait(&condvar, &mutex_distance);
     }
     
     printf("ACTUATION WILL BEGIN NOW")
     //TODO: Add protocol here to send this as a message to a different raspberry pi wirelessly 
     return 0;
     
        
}

//Recieves directions from vision detection protocol on which direction the drone should move
//based on alignment
void *vision(){
// TODO: Recieves information from a ZMQ socket in the form of a string that tells which direction the drone should move
// This program will be the subscriber
// Vision python program will be the publisher
// Directions include left, right, forward, backward, up, down.
}

int main(){
    //Set main thread priority higher than all other threads
    pthread_t mainid = pthread_self();
    struct sched_param schedule_paramMain;
    schedule_paramMain.sched_priority = 99;
    pthread_setschedparam(mainid,SCHED_FIFO, &schedule_paramMain);
    //initialize sockets and io structs
    static struct zmq_socket zsocket;
    struct gpio_pins IO_forward;

    void *start_park;

    //Pin initialization of ultrasonic sensors
    IO_forward.trigger = 66;
    IO_forward.echo = 67;
    IO_forward.checker = 1;  

    //initialize socket
    init_socket(&zsocket);

    //create threads
    pthread_t f1, ir, vision, actuation;
    pthread_attr_t a_attr;
    struct sched_param schedule_paramA;
    pthread_attr_init(&a_attr);
    pthread_attr_setinheritsched(&a_attr, PTHREAD_EXPLICIT_SCHED);
    pthread_attr_setschedpolicy(&a_attr, SCHED_RR);
    pthread_attr_setschedparam(&a_attr, &schedule_paramA);

    //Create mutexes and conditional variables
    pthread_mutexattr_t attr;

	// This solves a known problem with locking and unlocking a fast, nonrecursive mutex too often
	pthread_mutexattr_settype(&attr, PTHREAD_MUTEX_RECURSIVE_NP);
    pthread_mutex_init(&mutex_activate, &attr);
    pthread_mutex_init(&mutex_orientation, &attr);
    /*pthread_mutex_init(&mutex_peds_back, &attr);
    pthread_mutex_init(&mutex_open_found, &attr);
    pthread_mutex_init(&mutex_distance, &attr);*/
    pthread_mutexattr_destroy(&attr);

    //Create conditional variable attributes
    pthread_condattr_t condattr1;
	pthread_condattr_init(&condattr1);
	pthread_cond_init(&condvar, &condattr1);
    pthread_cond_init(&condvar_orientation &condattr1);
    /*pthread_cond_init(&condvar_spot, &condattr1);
	pthread_cond_init(&condvar_open_found, &condattr1);

*/

    //Phase I: User controlled car with safety halt features
    pthread_create(&f1, &a_attr, dist_detect, (void *) &IO_forward);
    pthread_create(&ir, &a_attr, ir_align,  NULL);
    pthread_create(&actuation, &a_attr,actuation_protocol, NULL);
    pthread_join(actuation, NULL);
    pthread_cancel(ir);
    pthread_cancel(f1);

    stop(&zsocket);
    return 0;
}
