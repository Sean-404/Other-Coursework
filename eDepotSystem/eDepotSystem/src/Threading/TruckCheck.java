package Threading;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import eDepotSystem.Depot;
import eDepotSystem.Truck;
import eDepotSystem.Vehicle;

public class TruckCheck implements Runnable {
	private List<Truck> truck;
	private Integer delay;
	private static ArrayList<MoveDetails> move = new ArrayList<MoveDetails>();
	private volatile boolean exit = false;

	public TruckCheck(List<Truck> arrayTruck, Integer seconds) {
		this.truck = arrayTruck;
		setSeconds(seconds);
	}
	
	public static void addToBufferTruck(Vehicle vehicle, Depot depot, Date date) {
		move.add(new MoveDetails(vehicle, depot, date));
	}
	
	@Override
	public void run() {
		while (!exit) {
			try {
				//This creates a delay for when the program checks for the stuff below
				Thread.sleep(delay);
				synchronized (truck) {
					//This goes through the array of trucks
					Date currentDate = new Date();
					SimpleDateFormat format = new SimpleDateFormat("dd-MM-yyyy HH:mm");
					String currentDate1 = format.format(currentDate);
					currentDate = format.parse(currentDate1);
					for (MoveDetails s : move) {
						if(s.getDate() != null) {
							if(s.getDate().equals(currentDate)) {
								System.out.println("Moved Vehicle");
								s.getDepot().addTruckAsVehicle(s.getVehicle());
								stop();
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
	
	public void stop() {
		exit = true;
	}

	public synchronized void setSeconds(Integer seconds) {
		delay = seconds * 1000;
	}

	public Integer getSeconds() {
		return delay / 1000;
	}
}