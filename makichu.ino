#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// Set the LCD address (change to 0x27 if 0x3F does not work)
LiquidCrystal_I2C lcd(0x3F, 16, 2);

void setup() {
  // Initialize the LCD
  lcd.begin();
  lcd.backlight(); // Turn on the backlight
  lcd.setCursor(0, 0);  
  lcd.print("Waiting..."); // Initial message on the LCD

  // Initialize serial communication  
  Serial.begin(9600);
}

void loop() {
  // Check if there is any serial data available
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n'); // Read data until newline character
    lcd.clear(); // Clear the LCD
    
    // Display the front and rear plate on the LCD
    if (data.startsWith("F:") && data.indexOf("R:") != -1) {
      lcd.setCursor(0, 0); // First line for front plate
      lcd.print(data.substring(0, 8)); // Display "F:<front>"
      lcd.setCursor(0, 1); // Second line for rear plate
      lcd.print(data.substring(data.indexOf("R:"))); // Display "R:<rear>"
    } else {
      lcd.setCursor(0, 0);
      lcd.print(data); // Display True, False, or Error
    }

    delay(2000); // Wait for 2 seconds to avoid flickering
  }
}
