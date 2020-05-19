package eDepotSystem;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.Date;

public class Driver implements Serializable {
	
	protected String username; //These attributes are protected so that only this class and any sub-classes can use them
	protected String password;
	protected ArrayList<WorkSchedule> arraySchedule = new ArrayList<WorkSchedule>();
	
	public Driver(String username, String password) {
		this.username = username;
		this.password = password;
	}
	
//--------------------------------CHECKS IF THE PASSWORD IS CORRECT------------------------------//
	
	public boolean checkPassword(String inputPassword) {
		if(password.equals(inputPassword)) {
			return true;
		} else {
			return false;
		}
	}
	
//------------------------------------CHECKS IF THE DRIVER IS AVAILABLE---------------------------------//
	
	public boolean isAvailable(Date startDate, Date endDate) {
		for(WorkSchedule s:arraySchedule) {
			if((s.getStartDate().before(startDate)) && (s.getEndDate().after(startDate))) {
				return false;
			}
			if((s.getStartDate().before(endDate)) && (s.getEndDate().after(endDate))) {
				return false;
			}
			if((s.getStartDate().after(startDate)) && (s.getEndDate().before(endDate))) {
				return false;
			}
		} return true;
	}
	
	public String getDriverName() {
		return username;
	}
	
	public void setSchedule(WorkSchedule workSchedule) {
		addSchedule(workSchedule);
		workSchedule.setDriver(this);
	}
	
	public void addSchedule(WorkSchedule schedule) {
		this.arraySchedule.add(schedule);
	}
	
	public ArrayList<WorkSchedule> getSchedule() {
		return arraySchedule;
	}

}