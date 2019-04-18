from gpiozero import OutputDevice as stepper
from time import sleep
import time
import math


class Stepper:
    
    nextstep = 1

    def __init__(self, in1, in2, in3, in4):

        self.step_count = 1
        self.last_time = 0
        self.in_progress = False
        self.startup_check = True
        pinon = 1
        pinoff = 0

        self.phase1pinblue = stepper(in1)
        self.phase2pinpink = stepper(in2)
        self.phase3pinyellow = stepper(in3)
        self.phase4pinorange = stepper(in4)

        self.halfstep1 = [(self.phase1pinblue, pinon), (self.phase2pinpink, pinoff), (self.phase3pinyellow, pinoff), (self.phase4pinorange, pinoff)]
        self.halfstep2 = [(self.phase1pinblue, pinon), (self.phase2pinpink, pinon), (self.phase3pinyellow, pinoff), (self.phase4pinorange, pinoff)]
        self.halfstep3 = [(self.phase1pinblue, pinoff), (self.phase2pinpink, pinon), (self.phase3pinyellow, pinoff), (self.phase4pinorange, pinoff)]
        self.halfstep4 = [(self.phase1pinblue, pinoff), (self.phase2pinpink, pinon), (self.phase3pinyellow, pinon), (self.phase4pinorange, pinoff)]
        self.halfstep5 = [(self.phase1pinblue, pinoff), (self.phase2pinpink, pinoff), (self.phase3pinyellow, pinon), (self.phase4pinorange, pinoff)]
        self.halfstep6 = [(self.phase1pinblue, pinoff), (self.phase2pinpink, pinoff), (self.phase3pinyellow, pinon), (self.phase4pinorange, pinon)]
        self.halfstep7 = [(self.phase1pinblue, pinoff), (self.phase2pinpink, pinoff), (self.phase3pinyellow, pinoff), (self.phase4pinorange, pinon)]
        self.halfstep8 = [(self.phase1pinblue, pinon), (self.phase2pinpink, pinoff), (self.phase3pinyellow, pinoff), (self.phase4pinorange, pinon)]

        self.fullstep1 = [(self.phase1pinblue, pinon), (self.phase2pinpink, pinon), (self.phase3pinyellow, pinoff), (self.phase4pinorange, pinoff)]
        self.fullstep2 = [(self.phase1pinblue, pinoff), (self.phase2pinpink, pinon), (self.phase3pinyellow, pinon), (self.phase4pinorange, pinoff)]
        self.fullstep3 = [(self.phase1pinblue, pinoff), (self.phase2pinpink, pinoff), (self.phase3pinyellow, pinon), (self.phase4pinorange, pinon)]
        self.fullstep4 = [(self.phase1pinblue, pinon), (self.phase2pinpink, pinoff), (self.phase3pinyellow, pinoff), (self.phase4pinorange, pinon)]
        self.fullstep5 = [(self.phase1pinblue, pinon), (self.phase2pinpink, pinon), (self.phase3pinyellow, pinoff), (self.phase4pinorange, pinoff)]
        self.fullstep6 = [(self.phase1pinblue, pinoff), (self.phase2pinpink, pinon), (self.phase3pinyellow, pinon), (self.phase4pinorange, pinoff)]
        self.fullstep7 = [(self.phase1pinblue, pinoff), (self.phase2pinpink, pinoff), (self.phase3pinyellow, pinon), (self.phase4pinorange, pinon)]
        self.fullstep8 = [(self.phase1pinblue, pinon), (self.phase2pinpink, pinoff), (self.phase3pinyellow, pinoff), (self.phase4pinorange, pinon)]
    

    def motor_move(self, direction, method, number_of_steps, degrees, duration, delay = 0.002):
        #28byj-48 stepper motor
        # full step = 2048 steps per rotation  .175 deg per step
        # half step = 4096 steps per rotation  .0879 deg per step

        if number_of_steps is not None:
            if degrees is not None:
                raise Exception("Cannot supply both number of steps and degrees at the same time.")

        if degrees is not None:
            if number_of_steps is not None:
                raise Exception("Cannot supply both number of steps and degrees at the same time.")
            else:
                if method == "full":
                    number_of_steps = (degrees / 360) * 2048
                if method == "half":
                    number_of_steps = (degrees / 360) * 4096
                number_of_steps = math.ceil(number_of_steps)

        if duration is not None:
            calculated_delay = duration / (number_of_steps - 1)
            if calculated_delay < 0.002:
                delay = 0.002
                self.exceeded_delay = True
            else:
                delay = calculated_delay
                self.exceeded_delay = False

        elapsed_time = time.time() - self.last_time

        # if self.startup_check and self.in_progress:
        #     print("Movement was stopped before finish")
        #     self.startup_check = True

        if self.in_progress == False:
            print("Delay           :" + str(delay))
            print("Number of steps :" + str(number_of_steps))
            print("Method          :" + str(method))
            print("Direction       :" + str(direction))
            print("Degrees         :" + str(degrees))
            print("Duration        :" + str(duration))
            print("Step count      :" + str(self.step_count))
            print("Elapsed time    :" + str(elapsed_time))
            if self.exceeded_delay:
                print("Calc delay      :" + str(calculated_delay))
            self.in_progress = True

        if (self.step_count <= number_of_steps) and (elapsed_time > delay):

            if self.step_count == 1:
                self.start_time = time.time()

            self.step_count = self.step_count + 1

            self.last_time = time.time()

            if self.nextstep == 1:
                if method == "half":
                    step = self.halfstep1
                else:
                    step = self.fullstep1
                if direction == "forward":
                    self.nextstep = 2
                else:
                    self.nextstep = 8

            elif self.nextstep == 2:
                if method == "half":
                    step = self.halfstep2
                else:
                    step = self.fullstep2
                if direction == "forward":
                    self.nextstep = 3
                else:
                    self.nextstep = 1

            elif self.nextstep == 3:
                if method == "half":
                    step = self.halfstep3
                else:
                    step = self.fullstep3
                if direction == "forward":
                    self.nextstep = 4
                else:
                    self.nextstep = 2

            elif self.nextstep == 4:
                if method == "half":
                    step = self.halfstep4
                else:
                    step = self.fullstep4
                if direction == "forward":
                    self.nextstep = 5
                else:
                    self.nextstep = 3

            elif self.nextstep == 5:
                if method == "half":
                    step = self.halfstep5
                else:
                    step = self.fullstep5
                if direction == "forward":
                    self.nextstep = 6
                else:
                    self.nextstep = 4

            elif self.nextstep == 6:
                if method == "half":
                    step = self.halfstep6
                else:
                    step = self.fullstep6
                if direction == "forward":
                    self.nextstep = 7
                else:
                    self.nextstep = 5

            elif self.nextstep == 7:
                if method == "half":
                    step = self.halfstep7
                else:
                    step = self.fullstep7
                if direction == "forward":
                    self.nextstep = 8
                else:
                    self.nextstep = 6

            elif self.nextstep == 8:
                if method == "half":
                    step = self.halfstep8
                else:
                    step = self.fullstep8
                if direction == "forward":
                    self.nextstep = 1
                else:
                    self.nextstep = 7

            for pin in step:
                xpin = pin[0]
                value = pin[1]
                if value == True:
                    xpin.on()
                    # print("PIN : " + str(xpin) + "ON")
                else:
                    xpin.off()
                    # print("PIN : " + str(xpin) + "OFF")

        total_time = time.time() - self.start_time

        if self.step_count >= number_of_steps + 1:
            print("Actual time     :" + str(total_time))
            self.step_count = 1
            self.in_progress = False
            self.startup_check = True
            return [True, number_of_steps, self.step_count, calculated_delay, total_time]
        else:
            return [False, number_of_steps, self.step_count, calculated_delay, total_time]

    def main(self):

        result1 = True
        result2 = True
        while True:
            result1 = S1.motor_move("forward", "full", None, 45.0, 5.0, None)
            print(result1)
            result2 = S1.motor_move("forward", "full", None, 180.0, 10.0, None)



if __name__ == '__main__':
    S1 = Stepper(12,16,20,21)
    S2 = Stepper(6,13,19,26)
    S1.main()
