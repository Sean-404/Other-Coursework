package Sys;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Date;
import java.util.List;
import java.util.Scanner;

import Threading.TankerCheck;
import Threading.TruckCheck;
import eDepotSystem.Depot;
import eDepotSystem.Tanker;
import eDepotSystem.Truck;
import eDepotSystem.Vehicle;
import eDepotSystem.WorkSchedule.ScheduleState;

public class DepotSystem {
	
	//this is the filepath for the serialisation file, it may need to be changed for other machines
	private static final String PATH = "C:\\Eclipse Projects\\eDepotSystem\\eDepotSystem\\src\\eDepotSystem";

	private static final Scanner S = new Scanner(System.in);
	
	//This creates a collection for serialisation
	private List<Depot> arrayDepot = Collections.synchronizedList(new ArrayList<Depot>());
	private Depot depot;
	private int depotInt;
	
	public DepotSystem() throws ParseException {
		
		arrayDepot.add(new Depot("Liverpool"));
		arrayDepot.add(new Depot("Manchester"));
		arrayDepot.add(new Depot("Leeds"));
		arrayDepot.get(0).addManager("Glyn", "_Glyn");
		arrayDepot.get(0).addDriver("Bob", "123");
		arrayDepot.get(0).addTanker("Ford", "Tanky", 1000, "AR15 JMU", null, 100, "Oil");
		arrayDepot.get(0).addTruck("Vauxhall", "Trucky", 1000, "LU20 POO", null, 150);
		//SimpleDateFormat format = new SimpleDateFormat("dd-MM-yyyy HH:mm");
		//Driver driver = arrayDepot.get(0).getDriver("Bob");
		//Vehicle vehicle = arrayDepot.get(0).getVehicle("AR15 JMU");
		//WorkSchedule sched = new WorkSchedule(1234, "Dave", format.parse("10-04-2020 09:00"), format.parse("12-04-2020 17:00"), ScheduleState.PENDING, driver, vehicle);
		//arrayDepot.get(0).addSchedule(sched);
		arrayDepot.get(1).addManager("Sorren", "_Sorren");
		arrayDepot.get(1).addTanker("Ferrari", "Tank", 500, "PU20 LNG", null, 50, "Chemicals");
		arrayDepot.get(2).addManager("Kirsty", "_Kirsty");
		arrayDepot.get(2).addTruck("Lamborghini", "Truck", 2000, "TF18 SJU", null, 200) ; 
		
	
		deSerialize();
		for (Depot s : arrayDepot) {
			s.startCheck();
		}
	}
	
	private void deSerialize() {
		ObjectInputStream ois;

		try {
			ois = new ObjectInputStream(new FileInputStream(PATH + "depots.ser"));

			arrayDepot = (List<Depot>)ois.readObject();

			ois.close();
		}
		catch (Exception e) {
			System.out.println(e.getMessage());
		}
	}

	private void serialize() {
		ObjectOutputStream oos;

		try {
			oos = new ObjectOutputStream(new FileOutputStream(PATH + "depots.ser"));
			oos.writeObject(arrayDepot);

			// ToDo : Finally ?
			oos.close();
		}
		catch (Exception e) {
			System.out.println(e.getMessage());
		}
	}
	
    public Depot getDepot(String selectedDepot) {
        for (Depot depot : arrayDepot) {
            if ((depot.getDepotName()).equals(selectedDepot)) {
                return depot;
            }
        }
        return null;
    }
	
//--------------------------------------LOG ON----------------------------------------------------------------//
    
	private void logOn() throws Exception {
		System.out.println(arrayDepot.toString());
		System.out.println("Choose a Depot Location (e.g. Liverpool = 1, Manchester = 2 etc.): ");
		depotInt = Integer.valueOf(S.nextLine());
		depotInt -= 1;
		depot = arrayDepot.get(depotInt);
		depot.logOn();
		if(depot.getAuthenticate()) {
			mainMenu();
		}
		else {
			System.out.println("Access Denied.");
		}
	}
	
	public void entryMenu() throws Exception {
		String choice = "";

		do {
			System.out.println("-- ENTRY MENU --");
			System.out.println("1 - Login");
			System.out.println("2 - Quit");
			System.out.print("Pick : ");

			choice = S.nextLine().toUpperCase();

			switch (choice) {
				case "1" : {
					logOn();
					break;
				}
			}

		} while (!choice.equals("2"));
		
		serialize();
		System.out.println("Bye Bye :)");
		S.close();
	}

	public void mainMenu() throws Exception {
		String choice = "";
		do {
			System.out.println("\nWelcome to the Depot System!");
			System.out.println("1 - View work schedule");
			System.out.println("2 - View list of vehicles");
			System.out.println("3 - Setup work schedule");
			System.out.println("4 - Move vehicle");
			System.out.println("5 - Add vehicle");
			System.out.println("6 - Remove vehicle");
			System.out.println("7 - Add driver");
			System.out.println("8 - Log out");
			System.out.print("Pick : ");

			choice = S.nextLine();
		
			switch (choice) {
				case "1" : {
					depot.viewWorkSchedule();
					break;
				}
				case "2":  {
					depot.viewVehicles();
					break;
				}
				case "3" : {
					depot.setupWorkSchedule();
					break;
				}
				case "4" : {
					if(depot.checkIfManager()) {
						Vehicle selectedVehicle = depot.displayVehicleMenu();
						System.out.println(arrayDepot.toString());
						System.out.println("Select Depot to Move Vehicle (e.g. Liverpool = 1, Manchester = 2 etc.): ");
						int depotChoice = Integer.valueOf(S.nextLine());
						depotChoice-=1;
						Depot selectedDepot = arrayDepot.get(depotChoice);
						
						System.out.println("Specify Move Date & Time for Vehicle [dd-mm-yyyy HH:MM] :");
						String moveDate = S.nextLine();
						SimpleDateFormat format = new SimpleDateFormat("dd-MM-yyyy HH:mm");
						Date moveDate1 = format.parse(moveDate);
						System.out.println("Vehicle will be moved to " + selectedDepot + " at date: " + moveDate1);
				
						if(selectedVehicle instanceof Tanker) {
							String regNo = ((Tanker) selectedVehicle).getRegNo();
							arrayDepot.get(depotInt).getRemoveTanker(regNo);
							TankerCheck.addToBufferTanker(selectedVehicle, selectedDepot, moveDate1);
							depot.startTankerCheck();
						}
						else if(selectedVehicle instanceof Truck) {
							String regNo = ((Truck) selectedVehicle).getRegNo();
							arrayDepot.get(depotInt).getRemoveTruck(regNo);
							TruckCheck.addToBufferTruck(selectedVehicle, selectedDepot, moveDate1);
							depot.startTruckCheck();
						}
					}
					else {
						System.out.println("You need to be a manager to move a vehicle!");
					}
					break;
				}
				case "5" : {
					depot.addVehicle();
					System.out.println("Vehicle Added!");
					break;
				}
				case "6" : {
					depot.removeVehicle();
					System.out.println("Vehicle Removed!");
					break;
				}
				case "7" : {
					depot.addNewDriver();
					System.out.println("Driver Added!");
					break;
				}
				
			}
		} while (!choice.equals("8"));
	}
}
