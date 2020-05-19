package eDepotSystem;

import java.util.Date;

public class Truck extends Vehicle {
	
	private int cargoCapacity;
	
	public Truck(String make, String model, int weight, String regNo, Date moveDate, int cargoCapacity) {
		super(make, model, weight, regNo, moveDate);
		this.cargoCapacity = cargoCapacity;
	}
	
	@Override
	public String toString() {
		return "Make: " + make +
				" | Model: " + model +
				" | Weight: " + weight +
				" | Reg No: " + regNo + 
				" | Cargo Capacity: " + cargoCapacity  + "\n";
	}
	
//----------------------------------------GETTERS AND SETTERS-----------------------------------------------//
	
	public String getMake() {
		return make;
	}
	
	public String getModel() {
		return model;
	}
	
	public int getWeight() {
		return weight;
	}
	
	public String getRegNo() {
		return regNo;
	}
	
	public int getCargoCapacity() {
		return cargoCapacity;
	}
	
	public Date getMoveDate() {
		return moveDate;
	}
}



