#include <stdio.h>
#include <string.h>
#include <FreeRTOS.h>
#include <task.h>
#include <bl_uart.h>
#include "bl_gpio.h"
#include "system.h"
#include <bl_rtc.h>

#define COUNT (1000000)

void TaskTime(void *pvParameters)
{
    uint32_t sum;
    
    bl_rtc_init();
    
    while (1) {
        uint32_t t0 = bl_rtc_get_timestamp_ms();
        for (uint32_t i=0 ; i<COUNT ; i++) {
          sum += bl_rtc_get_timestamp_ms();
        }
        uint32_t t1 = bl_rtc_get_timestamp_ms();
        
        printf("%u timestamps in %u ms\n", COUNT, t1-t0);
    }
    printf("sum = %u\n", sum);
}

void bfl_main(void)
{
    system_init();
    bl_uart_init(0, 16, 7, 255, 255, 9600);
    printf("booted\n");
    xTaskCreate(TaskTime, "Time", 1024, NULL, 1, NULL);
    vTaskStartScheduler();
}

