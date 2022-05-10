import Jetson.GPIO as GPIO
import time 

# start of codes to be initialized for servo motor and HCSR-04 in global area
servo_pin      = 22 # pin number assigned to the servo 
sensor_TRIG_pin= 23 # pin number assigned to the TRIG pin of sensor 
sensor_ECHO_pin= 24 # pin number assigned to the ECHO pin of sensor

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(servo_pin,GPIO.OUT)
GPIO.setup(sensor_TRIG_pin,GPIO.OUT)
GPIO.setup(sensor_ECHO_pin,GPIO.IN)

servo_motor= GPIO.PWM(servo_pin,50) # set frequency to 50 Hz
servo_motor.start(2.5) #starting duty cycle
# end of codes to be initialized for servo motor and HCSR-04 in global area

def turnCamera(motor_angle_variable):    #IMPORTANT_NOTE: NOT PROPER WITHOUT MULTITHREADING! THIS CASE THERE WILL BE A DELAY!
    #in servo: 1ms pulse    => 0 degree,    5% duty cycle(in 50Hz freq)   
    #          1.5ms pulse  => 90 degree,   7.5% duty cycle(in 50Hz freq)
    #          2ms pulse    => 180 degree,  10% duty cycle(in 50Hz freq)
    servo_motor.ChangeDutyCycle(5+motor_angle_variable/2)

def getSensorData(): # in the main code, make this funct work in a while loop
    GPIO.output(sensor_TRIG_pin,False)
    time.sleep(0.00001)
    GPIO.output(sensor_TRIG_pin,True)
    time.sleep(0.00001)
    GPIO.output(sensor_TRIG_pin,False)
    while GPIO.input(sensor_ECHO_pin) == 0:
        sensor_pulse_start=time.time()
    while GPIO.input(sensor_ECHO_pin) == 0:
        sensor_pulse_end=time.time()  
    sensor_pulse_duration = sensor_pulse_end - sensor_pulse_start
    sensor_measured_distance = sensor_pulse_duration *17150
    sensor_measured_distance = round(sensor_measured_distance,2)
    if sensor_measured_distance > 31.5:
        print("Distance:",sensor_measured_distance-0.5,"cm")
        #no_problem
    else:
        print("Distance:",sensor_measured_distance-0.5,"cm")
        print("Anomalous!!")
        #send notification!!!
        #print anomalous on UI
    return sensor_measured_distance #it is a shared variable bw py and JS used in firebase

#main area 
random_angle_for_test= 5
turnCamera(random_angle_for_test)
random_distance_for_test=getSensorData()
