package eDepotSystem;

import java.io.Serializable;
//import java.time.LocalDate;
import java.util.ArrayList;
import java.util.Date;


public abstract class Vehicle implements Serializable {
	
	protected String make; //These attributes are protected so that only this class and any sub-classes can use them
	protected String model;
	protected int weight;
	protected String regNo;
	protected Date moveDate;

	protected ArrayList<WorkSchedule> arraySchedule = new ArrayList<WorkSchedule>();
	
	public Vehicle(String make, String model, int weight, String regNo, Date moveDate) {
		this.make = make;
		this.model = model;
		this.weight = weight;
		this.regNo = regNo;
		this.moveDate = moveDate;
	}
	
//----------------------------------------CHECKS IF THE VEHICLE IS AVAILABLE-------------------------------------//
	
	public boolean isAvailable() {
		for(WorkSchedule schedule : this.arraySchedule) {
			if(schedule.getScheduleState() == eDepotSystem.WorkSchedule.ScheduleState.PENDING) {
				return false;
			}
			if(schedule.getScheduleState() == eDepotSystem.WorkSchedule.ScheduleState.ACTIVE) {
				return false;
			}
		}
		return true;
	}
	
	public void setSchedule(WorkSchedule workSchedule) {
		addSchedule(workSchedule);
		workSchedule.setVehicle(this);
	}
	
	public void addSchedule(WorkSchedule schedule) {
		this.arraySchedule.add(schedule);
	}
	
//------------------------------------GETTERS AND SETTERS----------------------------------------------------//
	
	public ArrayList<WorkSchedule> getSchedule(){
		return arraySchedule;
	}
	
	public String getRegNo() {
		return regNo;
	}
	
	public Date getMoveDate() {
		return moveDate;
	}

	public String getMake() {
		return make;
	}
	
	public String getModel() {
		return model;
	}
	
	public int getWeight() {
		return weight;
	}

}
