package Threading;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import eDepotSystem.Driver;
import eDepotSystem.Vehicle;
import eDepotSystem.WorkSchedule;

public class StatusCheck implements Runnable {
	private List<WorkSchedule> schedule;
	private Integer delay;

	public StatusCheck(List<WorkSchedule> arraySchedule, Integer seconds) {
		this.schedule = arraySchedule;
		setSeconds(seconds);
	}
	
	@Override
	public void run() {
		while (true) {
			try {
				//This creates a delay for when the program checks for the stuff below
				Thread.sleep(delay);
				synchronized (schedule) {
					Date currentDate = new Date();
					//This goes through the work schedule
					for (WorkSchedule s : schedule) {
						//This checks if the current date is during the work schedule, it becomes active
						if(s.getStartDate().before(currentDate) && (s.getEndDate().before(currentDate))){
							s.updateState();
							Driver driver = s.getDriver();
							ArrayList<WorkSchedule> driverSchedule = driver.getSchedule();
							for(int i = 0; i < driverSchedule.size(); i++ ) {
								if(driverSchedule.get(i).getID() == s.getID()) {
									driverSchedule.get(i).updateState();
								}
							}
							Vehicle vehicle = s.getVehicle();
							ArrayList<WorkSchedule> vehicleSchedule = vehicle.getSchedule();
							for(int i = 0; i < vehicleSchedule.size(); i++) {
								if(vehicleSchedule.get(i).getID() == s.getID()) {
									vehicleSchedule.get(i).updateState();
								}
							}
						}
						//This checks if the current date is after the work schedule, it becomes archived
						if(s.getStartDate().before(currentDate) && (s.getEndDate().before(currentDate))){
							s.updateState();
							Driver driver = s.getDriver();
							ArrayList<WorkSchedule> driverSchedule = driver.getSchedule();
							for(int i = 0; i < driverSchedule.size(); i++ ) {
								if(driverSchedule.get(i).getID() == s.getID()) {
									driverSchedule.get(i).updateState();
								}
							}
							Vehicle vehicle = s.getVehicle();
							ArrayList<WorkSchedule> vehicleSchedule = vehicle.getSchedule();
							for(int i = 0; i < vehicleSchedule.size(); i++) {
								if(vehicleSchedule.get(i).getID() == s.getID()) {
									vehicleSchedule.get(i).updateState();
								}
							}
						}
					}
					
				}
			}
			catch (Exception e) {
				e.printStackTrace();
			}
		}
	}

	public synchronized void setSeconds(Integer seconds) {
		delay = seconds * 1000;
	}

	public Integer getSeconds() {
		return delay / 1000;
	}
	
}