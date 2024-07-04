from machine import Pin


class AGM():
    # led pin
    PIN_RGB_LED = 1
    PIN_BUZZER = 2

    #buttons
    PIN_BTN_BACK = 0
    PIN_BTN_DEC = 37
    PIN_BTN_INC = 38
    PIN_BTN_ENTER = 39

    #shift register pins
    PIN_SHIFT_IN = 8
    PIN_SHIFT_OUT = 3
    PIN_SHIFT_IN_CLK = 16
    PIN_SHIFT_OUT_CLK = 46
    PIN_SHIFT_UPDATE = 45

    #pin battery manager
    PIN_BAT_FAULT = 48
    PIN_BAT_PROCHOT = 47
    
    def __init__(self):

        self.shift_out_data = [0, 0, 0, 0, 0, 0, 0, 0]
        self.pin_shift_in = Pin(self.PIN_SHIFT_IN, Pin.IN)
        self.pin_shift_out = Pin(self.PIN_SHIFT_OUT, Pin.OUT)
        self.pin_shift_in_clk = Pin(self.PIN_SHIFT_IN_CLK, Pin.OUT)
        self.pin_shift_out_clk = Pin(self.PIN_SHIFT_OUT_CLK, Pin.OUT)
        self.pin_shift_update = Pin(self.PIN_SHIFT_UPDATE, Pin.OUT)

    def enable_5v(self, v: bool):
        self.shift_out_data[0] = v
        self.write()

    def reset_pd_cntr(self, v: bool):
        self.shift_out_data[1] = v
        self.write()

    def select_disp_dc(self, v: bool):
        self.shift_out_data[2] = v
        self.write()

    def reset_disp(self, v: bool):
        self.shift_out_data[3] = v
        self.write()

    def set_disp_bs(self, v: bool):
        self.shift_out_data[4] = v
        self.write()

    def reset_lora(self, v: bool):
        self.shift_out_data[5] = v
        self.write()

    def reset_gps(self, v: bool):
        self.shift_out_data[6] = v
        self.write()

    def reset_cp2102(self, v: bool):
        self.shift_out_data[7] = v
        self.write()

    def write(self):
        if len(self.shift_out_data) != 8:
            raise SystemError("shift out data length must be equal to 8")
        self.pin_shift_out_clk.value(0)
        self.pin_shift_update.value(0)
        for i in self.shift_out_data:
            self.shift_out_data.value(i)
            self.pin_shift_out_clk.value(1)
            self.pin_shift_out_clk.value(0)
        self.pin_shift_update.value(1)
        self.pin_shift_update.value(0)

    def get_bat_chr_ok(self):
        return self.read(0)
    
    def get_gps_goe_fence(self):
        return self.read(1)
    
    def get_gps_fix(self):
        return self.read(2)
    
    def get_disp_busy(self):
        return self.read(3)
    
    def get_lora_dio1(self):
        return self.read(4)
    
    def get_lora_dio2(self):
        return self.read(5)
    
    def get_lora_dio3(self):
        return self.read(6)

    def get_lora_busy(self):
        return self.read(7)

    def read(self, bit_index:int):
        self.pin_shift_in_clk.value(0)
        self.pin_shift_update.value(1)
        self.pin_shift_update.value(0)
        for _ in range(bit_index):
            self.pin_shift_in_clk.value(1)
            self.pin_shift_in_clk.value(0)

        return self.pin_shift_in.value()