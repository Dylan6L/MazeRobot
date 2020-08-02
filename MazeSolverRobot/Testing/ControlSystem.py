import time

# left side
encoder1 = 0
encoder2 = 0

# right side
encoder3 = 0
encoder4 = 0

pwmR = 0
pwmL = 0

while True:
    time.sleep(1)
    
    lenconder = encoder1 + encoder2
    rencoder = encoder3 + encoder4

    error = lenconder - rencoder
