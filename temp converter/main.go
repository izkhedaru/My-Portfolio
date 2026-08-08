package main

import "fmt"

func main() {
	var farenheit float64
	fmt.Println("Enter temp (farenheit): ")
	fmt.Scanf("%f", &farenheit)

	celcius := (farenheit - 32) * 5 / 9
	fmt.Printf("Temp in celcius: %.2f\n", celcius)
}
