#include "Parallel_park.h"


pthread_mutex_t mutex_activate;

pthread_cond_t condvar;


//Global shared variables, mutex protected
int activate = 0;                  //Indicates if it is safe to move forward
int temp_dist = MIN_DISTANCE;  //Minimum distance allowed before car should stop moving in reverse

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
        if(dist < MIN_DISTANCE){
            pthread_mutex_lock(&mutex_activate);
            activate = 1;
            pthread_cond_broadcast(&condvar);
            pthread_mutex_unlock(&mutex_activate);
        }
        else{
            pthread_mutex_lock(&mutex_activate);
            activate = 0;
            pthread_cond_broadcast(&condvar);
            pthread_mutex_unlock(&mutex_activate);
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

}


//Recieves directions from vision detection protocol on which direction the drone should move
//based on alignment
void *vision(){

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
    pthread_t f1, ir, vision;
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
    /*pthread_mutex_init(&mutex_peds, &attr);
    pthread_mutex_init(&mutex_peds_back, &attr);
    pthread_mutex_init(&mutex_open_found, &attr);
    pthread_mutex_init(&mutex_distance, &attr);*/
    pthread_mutexattr_destroy(&attr);

    //Create conditional variable attributes
    pthread_condattr_t condattr1;
	pthread_condattr_init(&condattr1);
	pthread_cond_init(&condvar, &condattr1);
    /*pthread_cond_init(&condvar_peds_back, &condattr1);
    pthread_cond_init(&condvar_spot, &condattr1);
	pthread_cond_init(&condvar_open_found, &condattr1);

*/

    //Phase I: User controlled car with safety halt features
    pthread_create(&f1, &a_attr, dist_detect, (void *) &IO_forward);
    pthread_join(f1, NULL);

    stop(&zsocket);
    return 0;
}
