    // Display the data on the LCD
    if (data.startsWith("Front:")) {
      // Front plate detected
      lcd.setCursor(0, 0);
      lcd.print("Front Plate:");
      lcd.setCursor(0, 1);
      lcd.print(data.substring(7));  // Display the plate number
    } else if (data.startsWith("Rear:")) {
      // Rear plate detected
      lcd.setCursor(0, 0);
      lcd.print("Rear Plate:");
      lcd.setCursor(0, 1);
      lcd.print(data.substring(6));  // Display the plate number
    } else if (data.startsWith("Match:")) {
      // Match status
      lcd.setCursor(0, 0);
      lcd.print("Plates Match:");
      lcd.setCursor(0, 1);
      lcd.print(data.substring(7));  // Display "True" or "False"
    } else if (data.startsWith("Error")) {
      // Error message
      lcd.setCursor(0, 0);
      lcd.print("Error Detected!");
      lcd.setCursor(0, 1);
      lcd.print("Retry Plates");
    }

    delay(2000);  // Display each message for 2 seconds
  }
}