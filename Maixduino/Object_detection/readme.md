
## Run custom model into Maixduino board

    1. Erase the board
    2. Flash with firmware
    3. Send all files to the sd card and run test file
    4. Without sd card -> Flash with the custom model and put the appropiate address
    5. Change below code to
    
    task = kpu.load("/sd/custom_model.kmodel")
    task = kpu.load(0x500000)
