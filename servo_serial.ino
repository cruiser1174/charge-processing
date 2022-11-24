//www.elegoo.com
//2016.12.9


/*   The most common method of using 74CH595
 *   lctchPin->LOW : Begin transmitting signals.
 *   shiftOut(dataPin, clockPin, bitOrder, value)
 *   dataPin: the pin on which to output each bit. Allowed data types: int.
 *   clockPin: the pin to toggle once the dataPin has been set to the correct value. Allowed data types: int.
 *   bitOrder: which order to shift out the bits; either MSBFIRST or LSBFIRST. (Most Significant Bit First, or, Least Significant Bit First).
 *   value: the data to shift out. Allowed data types: byte. 
 *   lctchPin->HIch : The end of the transmission signal.
*/

#include <Servo.h>

Servo FS51;// create servo object to control a servo
// twelve servo objects can be created on most boards

int pos = 13;// variable to store the servo position

void setup() 
{
  FS51.attach(9);// attaches the servo on pin 9 to the servo object
  Serial.begin(9600);
  while (! Serial); // Wait untilSerial is ready - Leonardo
  Serial.println("Enter 'x' to sweep or 'o' to return to starting position");
}

void loop() 
{
  FS51.write(pos);
  if (Serial.available())//judge the serial if receive data
  {
    char ch = Serial.read();//Read serial data and save it in "ch"
    
    if (ch == 'x')  //If the data of "ch" is the character'run'
    {
      pos = 135;
      FS51.write(pos); 
      Serial.print("Sweep complete");
    }
    if (ch == 'o')
    {
      pos = 13;
      FS51.write(pos)
      ; 
    }
    if (ch == 'p')
    {
      pos = pos + 5;
      FS51.write(pos); 
    }
    if (ch == 'l')
    {
      pos = pos - 5;
      FS51.write(pos); 
    }
  }
}
