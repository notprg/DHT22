import gpio
from bsp import board

pin = D16

def wakeUp(dataPin) -> bool:   # OK 
    sleep(50, MICROS)
    gpio.mode(dataPin, INPUT) 
    print("D26: ", gpio.get(dataPin)) #Valore iniziale, HIGH

    gpio.mode(dataPin, OUTPUT) #Setto il pin in output
    gpio.low(dataPin) #imposto il segnale a low per 1 millis
    print("D26: ", gpio.get(dataPin))
    sleep(25, MILLIS)
    # gpio.toggle(dataPin)

    gpio.mode(dataPin, INPUT) #libero il bus. dataPin dovrebbe tornare ad 1
    print("D26: ", gpio.get(dataPin))
    sleep(30, MICROS)

def DHT22isAwake(dataPin) -> bool: 

    if(gpio.get(dataPin) != 0):
        #raise Exception("Error in response signal (NOT LOW)")
        print("Error in response signal (NOT LOW)")
    sleep(80, MICROS)

    if(gpio.get(dataPin) != 1):
        #raise Exception("Error in response signal (NOT HIGH)")
        print("Error in response signal (NOT HIGH)")
    sleep(80, MICROS)
    return True

def getBit(dataPin) -> int: #Sia nel caso di ricezione di 0 che di 1 i primi 50 micros sono di segnale low
    
    if(gpio.get(dataPin) != 0):
        # raise Exception("Error during receiving bit...")
        print("Error during receiving bit...")
    sleep(50, MICROS)

    sleep(28, MICROS)
    if(gpio.get(dataPin) == 0):
        return 0
    else:
        return 1

def read(dataPin) -> (int, int, int, int, int):
    hum_int = nextByte(dataPin),
    hum_dec = nextByte(dataPin),
    temp_int = nextByte(dataPin),
    temp_dec = nextByte(dataPin),
    checksum = nextByte(dataPin)
    return(hum_int, hum_dec, temp_int, temp_dec, checksum)

def nextByte(dataPin) -> int:
    byte = 0x00
    for i in range(0,8):
        bit_i = getBit(dataPin)
        byte = byte | (bit_i << (7 - i))
    return byte

while True:

    wakeUp(pin)
    if(DHT22isAwake(pin)):
        (hi, hd, ti, td, c) = read(pin)
        if(hi + hd + ti + td != c):
            print("Errore di lettura, Checksum incongruente...")
        else:
            print("Humidity: ", hi, ".", hd, "%")
            print("Temperature: ", ti, ".", td)
    else: 
        print("Failed...")
    sleep(2000)
    