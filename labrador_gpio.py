import os, sys, time

pin_map = {
    36: "A28",
    33: "B0",
    35: "B1",
    37: "B2",
    12: "B8",
    31: "B10",
    32: "B13",
    28: "B14",
    29: "B15",
    27: "B16",
    7:  "B18",
    26: "B19",
    11: "C0",
    13: "C1",
    15: "C4",
    22: "C5",
    18: "C6",
    24: "C23",
    21: "C24",
    16: "D30",
    3:  "E3",
    5:  "E2",
}

class GPIO:
    def __init__(self, pin, direction="out") -> None:
        if direction not in ["out", "in"]:
            print(f"Invalid direction: {direction}")
            return
        self.direction = direction
        self.pin = pin
        self.num = GPIO.get_num(pin)
        if not self.num:
            return
        GPIO.sys_cmd(f"echo {self.num} > /sys/class/gpio/export")
        GPIO.sys_cmd(f"echo {self.direction} > /sys/class/gpio/gpio{self.num}/direction")

    def write(self, value):
        if self.direction != "out":
            print(f"Error: cannot write when direction is {self.direction}")
        else:
            GPIO.sys_cmd(f"echo {value} > /sys/class/gpio/gpio{self.num}/value")

    def read(self):
        if self.direction != "in":
            print(f"Error: cannot read when direction is {self.direction}")
        else:
            GPIO.sys_cmd(f"cat /sys/class/gpio/gpio{self.num}/value")

    def sys_cmd(cmd):
        print("Will run: ", cmd)
        # test if running on a labrador; if yes, run the command
        os.system(f"[ $(uname -m) = aarch64 ] && {cmd}")

    def get_offset(group):
        group_ascii = ord(group)
        assert group_ascii in range(ord("A"), ord("E")+1)
        return 32 * (group_ascii - ord("A"))

    def get_num(pin):
        group = dict.get(pin_map, pin)
        if not group:
            print(f"Invalid pin {pin}")
            return
        offset = GPIO.get_offset(group[0])
        group_n = int(group[1:])
        return offset + group_n


if __name__ == "__main__":
    print("Test step: ")
    assert GPIO.get_num(3) == 131 # 128 + 3 (GPIOE3)
    assert GPIO.get_num(5) == 130 # 128 + 2 (GPIOE2)
    assert GPIO.get_num(15) == 68 # 64 + 4 (GPIOC4)
    assert GPIO.get_num(1) == None # this is a VCC pin
    assert GPIO.get_num(39) == None # this is a GND pin

    print("Instantiate step: ")
    leds = [
        GPIO(3, "out"),
        GPIO(5, "out"),
        GPIO(15, "out"),
    ]

    print("Use step: ")
    while True:
        for led in leds:
            led.write(1)
            time.sleep(1)
            led.write(0)
