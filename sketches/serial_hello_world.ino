#include <LiquidCrystal.h>
 
LiquidCrystal lcd(8, 9, 4, 5, 6, 7);           // select the pins used on the LCD panel

char inChar;
String inStr;

void setup(){
   lcd.begin(16, 2);               // start the library
   lcd.setCursor(0,0);             // set the LCD cursor   position 
   //lcd.print("Hello IOT World");  // print a simple message on the LCD

  // initialize serial port at a baud rate of 115200 bps
  Serial.begin(115200);
  delay(100);
   lcd.print("Waiting 4 Cmd");  // print a simple message on the LCD
}

// define some values used by the panel and buttons
int lcd_key     = 0;
int adc_key_in  = 0;
 
#define btnRIGHT  0
#define btnUP     1
#define btnDOWN   2
#define btnLEFT   3
#define btnSELECT 4
#define btnNONE   5
 
int read_LCD_buttons(){               // read the buttons
    adc_key_in = analogRead(0);       // read the value from the sensor 
 
    // my buttons when read are centered at these valies: 0, 144, 329, 504, 741
    // we add approx 50 to those values and check to see if we are close
    // We make this the 1st option for speed reasons since it will be the most likely result
 
    if (adc_key_in > 1000) return btnNONE; 
 
    // For V1.1 us this threshold
    if (adc_key_in < 50)   return btnRIGHT;  
    if (adc_key_in < 250)  return btnUP; 
    if (adc_key_in < 450)  return btnDOWN; 
    if (adc_key_in < 650)  return btnLEFT; 
    if (adc_key_in < 970)  return btnSELECT;  
 
   // For V1.0 comment the other threshold and use the one below:
   /*
     if (adc_key_in < 50)   return btnRIGHT;  
     if (adc_key_in < 195)  return btnUP; 
     if (adc_key_in < 380)  return btnDOWN; 
     if (adc_key_in < 555)  return btnLEFT; 
     if (adc_key_in < 790)  return btnSELECT;   
   */
 
    return adc_key_in;                // when all others fail, return this.
}
 


void loop() {
  // put your main code here, to run repeatedly:
   lcd.setCursor(13,1);             // move cursor to second line "1" and 9 spaces over
   lcd.print(millis()/1000);       // display seconds elapsed since power-up
 
   lcd.setCursor(0,1);             // move to the begining of the second line
   lcd_key = read_LCD_buttons();   // read the buttons

String flush_s=
lcd.print("%13s", " ");
   switch (lcd_key){               // depending on which button was pushed, we perform an action

       case btnRIGHT:{             //  push button "RIGHT" and show the word on the screen
            
            lcd.print("RIGHT ");
            break;
       }
       case btnLEFT:{
             lcd.print("LEFT   "); //  push button "LEFT" and show the word on the screen
             break;
       }    
       case btnUP:{
             lcd.print("UP    ");  //  push button "UP" and show the word on the screen
             break;
       }
       case btnDOWN:{
             lcd.print("DOWN  ");  //  push button "DOWN" and show the word on the screen
             break;
       }
       case btnSELECT:{
             lcd.print("SELECT");  //  push button "SELECT" and show the word on the screen
             break;
       }
       case btnNONE:{
          //   lcd.print("NONE  ");  //  No action  will show "None" on the screen
             break;
       }
       default:{
             lcd.print(adc_key_in);  //  No action  will show "None" on the screen
             break;
       }
   }

/* Serial code begins */
  inChar = '\3';
  //inStr[0] = '\3';
  
  while (Serial.available()) {
    
    lcd.setCursor(0,1);             // move to the begining of the second line
    lcd.print("%13s", " ");
    // get the new byte:
    //inChar = (char)Serial.read();
    inStr = Serial.readString();
    
  if (inStr.charAt(0) == '1') { // compare received data
    lcd.print("Serial Hi ");  //  No action  will show "None" on the screen
  } else if (inStr.charAt(0) == '0') {
    lcd.print("Serial low");  //  No action  will show "None" on the screen
  }
  else {
    lcd.print(inStr);
  }
  Serial.print("Got it");

  }
  
  //Serial.print("inChar= ");Serial.println(inChar);
  //char byteParsed = parseResponse(inChar);
  

  //delay(10);  // added for serial..

}
