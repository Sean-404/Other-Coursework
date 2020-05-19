package eDepotSystem;

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.Serializable;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Date;
import java.util.List;
import java.util.Scanner;

import Threading.StatusCheck;
import Threading.TankerCheck;
import Threading.TruckCheck;
import eDepotSystem.WorkSchedule.ScheduleState;

public final class Depot implements Serializable {
	
	private static Scanner s;
	private String depotName;
	private boolean userAuthenticate;
	private List<Driver> arrayDrivers = Collections.synchronizedList(new ArrayList<Driver>());
	private List<WorkSchedule> arraySchedule = Collections.synchronizedList(new ArrayList<WorkSchedule>());
	private List<Truck> arrayTruck = Collections.synchronizedList(new ArrayList<Truck>());
	private List<Tanker> arrayTanker = Collections.synchronizedList(new ArrayList<Tanker>());
	public Driver userAccount;
	
	public Depot(String depotName) {
		userAuthenticate = false;
		this.depotName = depotName;
	}
	
	//This creates new threads to check the status of the schedule and for the move date of vehicles
	public void startCheck() {
		new Thread(new StatusCheck(arraySchedule, 10)).start();
	}
	
	public void startTruckCheck() {
		new Thread(new TruckCheck(arrayTruck, 10)).start();
	}
	
	public void startTankerCheck() {
		new Thread(new TankerCheck(arrayTanker, 10)).start();
	}
	
	public boolean getAuthenticate() {
		return userAuthenticate;
	}
		
//-----------------------------LOG ON FUNCTION -----------------------------------------
	public void logOn() throws NumberFormatException, ParseException {
		s = new Scanner(System.in);
		System.out.println("Enter your username:");
		String inputUsername = s.nextLine();
		System.out.println("Enter your password:");
		String inputPassword = s.nextLine();
		
		userAuthenticate = authenticateUser(inputUsername, inputPassword);
		
		if(userAuthenticate) {
			System.out.println("Login credentials authenticated.");
		} else {
			System.out.println("Login credentials incorrect.");
		}
		
	}
//-----------------------------LOG ON FUNCTION -----------------------------------------
	
//-----------------------------ADD DRIVER FUNCTION -----------------------------------------
	public void addDriver(String username, String password) {
		arrayDrivers.add(new Driver(username, password));
	}
	
	public void addManager(String username, String password) {
		arrayDrivers.add(new Manager(username, password));
	}
	
    public Driver getDriver(String driverName) {
        for (Driver driverAccount : arrayDrivers) {
            if ((driverAccount.getDriverName()).equals(driverName)) {
                return driverAccount;
            }
        }

        return null;
    }
    
    public void addNewDriver() {
    	
    	if (userAccount instanceof Manager) {
			 System.out.println("Specify Driver's Username :");
			 String driverUsername = s.nextLine();
			 System.out.println("Specify Driver's Password :");
			 String driverPassword = s.nextLine();
			 addDriver(driverUsername, driverPassword);
			
			} else {
			  System.out.println("You need to be a manager to add a new driver!");
			}
    }
    
 //-----------------------------ADD DRIVER FUNCTION -----------------------------------------    
    
 //-----------------------------USER AUTHENTICATE FUNCTION -----------------------------------------

    public boolean authenticateUser(String inputUsername, String inputPassword) {
        userAccount = getDriver(inputUsername);

        if (userAccount != null) {
            return userAccount.checkPassword(inputPassword);
        }
        else {
            return false;
        }
    }
 //-----------------------------USER AUTHENTICATE FUNCTION -----------------------------------------
    
    
 //------------------------------------- ADD SCHEDULE FUNCTION---------------------------------------
    
    //
	public void addSchedule(WorkSchedule schedule) {
		this.arraySchedule.add(schedule);
	}
	
	public void setupWorkSchedule() throws Exception {
		if (userAccount instanceof Manager) {
			System.out.println("Specify 4 digit Schedule ID: ");
			int scheduleID = Integer.valueOf(s.nextLine());
			System.out.println("Specify Client: ");
			String client = s.nextLine();
			System.out.println("Specify Start Date and Time (dd-mm-yyyy HH:mm): ");
			String startDate = s.nextLine();
			System.out.println("Specify End Date and Time (dd-mm-yyyy HH:mm): ");
			String endDate = s.nextLine();
			SimpleDateFormat format = new SimpleDateFormat("dd-MM-yyyy HH:mm");
			Date startDate1 = format.parse(startDate);
			Date endDate1 = format.parse(endDate);
			ScheduleState state = ScheduleState.PENDING;
			System.out.println("Specify Driver: ");
			String driverString = s.nextLine();
			Driver driver = getDriver(driverString);
			if(driver.isAvailable(startDate1, endDate1)) {
				System.out.println("Specify Vehicle Reg No: ");
				String vehicleString = s.nextLine();
				Vehicle vehicle = getVehicle(vehicleString);
				WorkSchedule schedule = new WorkSchedule(scheduleID, client, startDate1, endDate1, state, driver, vehicle);
				addSchedule(schedule);
				driver.addSchedule(schedule);
				vehicle.addSchedule(schedule);
				System.out.println("Job has been added to the Work Schedule!");
			}
			else {
				System.out.println("Schedule overlaps with an existing job!");
			}
		} else {
			System.out.println("You need to be a manager to setup the work schedule.");
		}
	}
	
	public boolean scanForOverlap(Date date) {
		for(WorkSchedule schedule : this.arraySchedule) {
			if(date.after(schedule.getStartDate())
					&& date.before(schedule.getEndDate()))
				return true;
		}
		return false;
	}
	
	public void viewWorkSchedule() throws NumberFormatException, ParseException {
		System.out.println(arraySchedule.toString());
	}
	
//------------------------------------- ADD SCHEDULE FUNCTION---------------------------------------
	
	
//---------------------------------------- ADD VEHICLE FUNCTION ------------------------------------
	
	
	// calls Truck array to add new Truck to the list
	public void addNewTruck(Truck newTruck) {
		this.arrayTruck.add(newTruck);
	}
	
	// calls Tanker array to add new Tanker to the list
	public void addNewTank(Tanker newTank) {
		this.arrayTanker.add(newTank);
	}
	
	// method to add vehicle
	public void addVehicle() throws Exception {
		
		//ensures only managers can add vehicles
		if (userAccount instanceof Manager) {
			 System.out.println("Specify Type of vehicle [Truck or Tanker] :");
			 String type = s.nextLine();
			 
			 //if type is "Truck" call getTruck() that ask for Truck details
			 	if (type.equals("Truck")) {
			 	 Truck newTruck = getTruck();
			 	 addNewTruck(newTruck);
			 	 //else call getTank() to input Tanker details
			    } else if (type.contentEquals("Tanker")) {
			   	Tanker newTank = getTank();
			  	addNewTank(newTank);
			    } else {
			    	//if type is neither vehicle is not appropriate for Depot
			    	System.out.println("Vehicle type not appropriate");
			    	addVehicle();
			    }
			} else {
			  System.out.println("You need to be a manager to add a new vehicle");
			}
	}

	//gets Tank details
	public Tanker getTank() {
		System.out.println("Specify Make :");
		String make = s.nextLine();
		System.out.println("Specify Model :");
		String newModel = s.nextLine();
		System.out.println("Specify Weight :");
		int newWeight = Integer.valueOf(s.nextLine());
		System.out.println("Specify RegNo :");
		String newRegNo = s.nextLine();
		
		//prevents existing tanks with the same RegNo from being added
		for(int i = 0; i < arrayTanker.size(); i++) {
			if(arrayTanker.get(i).getRegNo().equals(newRegNo)) {
				System.out.println("Vehicle already exists");
				getTank();
			}
		}
		
		System.out.println("Specify Liquid Capacity :");
		int newLiquidCapacity = Integer.valueOf(s.nextLine());
		System.out.println("Specify Liquid Type :");
		String newLiquidType = s.nextLine();
		Date newMoveDate = null;
		
		//adds details of new registered Tanker to the array list
		return new Tanker(make, newModel, newWeight, newRegNo, newMoveDate, newLiquidCapacity, newLiquidType);
	}
	
	//gets Truck details
	public Truck getTruck() throws ParseException {
		System.out.println("Specify Make :");
		String make = s.nextLine();
		System.out.println("Specify Model :");
		String newModel = s.nextLine();
		System.out.println("Specify Weight :");
		int newWeight = Integer.valueOf(s.nextLine());
		System.out.println("Specify RegNo :");
		String newRegNo = s.nextLine();
		
		//prevents existing trucks with the same RegNo from being added
		for(int i = 0; i < arrayTruck.size(); i++) {
			if(arrayTruck.get(i).getRegNo().equals(newRegNo)) {
				System.out.println("Vehicle already exists");
				getTruck();
			}
		}
		
		System.out.println("Specify Cargo Capacity :");
		int newCargoCapacity = Integer.valueOf(s.nextLine());
		Date newMoveDate = null;
		
		//adds details of new registered Truck to the array list
		return new Truck(make, newModel, newWeight, newRegNo, newMoveDate, newCargoCapacity); 
	}

//---------------------------------------- ADD VEHICLE FUNCTION ------------------------------------
	
	//---------------------------------------- REMOVE VEHICLE FUNCTION ------------------------------------
	
	//allows removing added vehicles from Truck and Tanker array lists
 	public void removeVehicle() {
 		if(userAccount instanceof Manager) {
 			System.out.println(arrayTruck.toString());
 			System.out.println(arrayTanker.toString());
 			
 			//removes vehicles by RegNo
 			System.out.println("Select Vehicle to Remove by RegNo :");
 			String regNoInput = s.nextLine();
 			Vehicle selectedVehicle = getVehicle(regNoInput);
 			if(selectedVehicle instanceof Truck) {
 				getRemoveTruck(regNoInput);
 			}
 			if(selectedVehicle instanceof Tanker) {
 				getRemoveTanker(regNoInput);
 			}
 		} else {
 			
 			//ensures only managers can remove vehicles from the system
 			System.out.println("You need to be a manager to remove a vehicle!");
 		}
	} 
 	
 	//removes vehicle by RegNo
 	public void removeVehicleByRegNo(String regNo) {
 		Vehicle selectedVehicle = getVehicle(regNo);
 		//if chosen vehicle is Truck , remove vehicle from Truck array list
 		if(selectedVehicle instanceof Truck) {
 			getRemoveTruck(regNo);
 		}
 		//if chosen vehicle is Tanker , remove vehicle from Tanker  array list
 		if(selectedVehicle instanceof Tanker) {
 			getRemoveTanker(regNo);
 		}
 	}
 	
 	//removes selected truck from Truck array list
 	public void getRemoveTruck(String regNo) {
 		//goes through array list to spot the selected Truck by RegNo
 		for (int i = arrayTruck.size() - 1; i >=0; --i) {
 		    final Truck tr = arrayTruck.get(i);
 		    //if specified RegNo matches existing RegNo from array list , remove vehicle
 		    if (tr.regNo.equals(regNo)) {
 		      arrayTruck.remove(i);
 		      return;
 		    } else {   	
 		    	//if specified RegNo does not match any RegNo from array list, it does not exist
 		    	System.out.println("Vehicle does not exist");
 		    	removeVehicle();
 		    }
 		}
 	}
 	
 	//removes selected truck from Truck array list
 	public void getRemoveTanker(String regNo) {
 		//goes through array list to spot the selected Tanker by RegNo
 		for (int i = arrayTanker.size() - 1; i >=0; --i) {
 		    final Tanker ta = arrayTanker.get(i);
 		 //if specified RegNo matches existing RegNo from array list , remove vehicle
 		    if (ta.regNo.equals(regNo)) {
 		      arrayTanker.remove(i);
 		      return;
 		    } else {
 		    	//if specified RegNo does not match any RegNo from array list, it does not exist
 		    	System.out.println("Vehicle does not exist");
 		    	removeVehicle();
 		    }
 		}
    }
 	//---------------------------------------- REMOVE VEHICLE FUNCTION ------------------------------------
 	
 	
 	//----------------------------------------MOVE VEHICLE FUNCTION ---------------------------------------
 	
	public Vehicle displayVehicleMenu() throws NumberFormatException, ParseException {
		//displays list of available vehicles
		System.out.println(arrayTruck.toString());
		System.out.println(arrayTanker.toString());
		System.out.println("Select Vehicle by RegNo :");
		String regNoInput = s.nextLine();
		
		Vehicle selectedVehicle = getVehicle(regNoInput);
		System.out.println(selectedVehicle);
		
		//if specified vehicle exists or available , return chosen vehicle
		if(selectedVehicle.isAvailable()) {
			return selectedVehicle;
		}
		return null;
	}
	
	//displays list of existing vehicles
	public void viewVehicles() {
		System.out.println(arrayTruck.toString());
		System.out.println(arrayTanker.toString());
	}
	
    public Vehicle getVehicle(String regNo) {
        for (Vehicle vehicle : arrayTanker) {
            if ((vehicle.getRegNo()).equals(regNo)) {
                return vehicle;
            }
        }
        
        for (Vehicle vehicle : arrayTruck) {
            if ((vehicle.getRegNo()).equals(regNo)) {
                return vehicle;
            }
        }
        return null;
    }
	//------------------------------------ MOVE VEHICLE FUNCTION ------------------------------------
    
	@Override
	public String toString() {
		return "Depot: " + depotName + "\n";
	}

	public void addTanker(String make, String model, int weight, String regNo, Date moveDate, int liquidCapacity, String liquidType) {
		arrayTanker.add(new Tanker(make, model, weight, regNo, moveDate, liquidCapacity, liquidType));
	}
	
	public void addTankerAsVehicle(Vehicle vehicle) {
		for(int i = 0; i < arrayTanker.size(); i++) {
			if(!(arrayTanker.get(i).getRegNo().equals(vehicle.getRegNo()))) {
				arrayTanker.add(new Tanker(vehicle.getMake(), vehicle.getModel(), vehicle.getWeight(), vehicle.getRegNo(), null, ((Tanker) vehicle).getLiquidCapacity(), ((Tanker) vehicle).getLiquidType()));
			}
		}
	}
	
	public void addTruck(String make, String model, int weight, String regNo, Date moveDate, int cargoCapacity) {
		arrayTruck.add(new Truck(make, model, weight, regNo, moveDate, cargoCapacity));
	}
	
	public void addTruckAsVehicle(Vehicle vehicle) {
		for(int i = 0; i < arrayTruck.size(); i++) {
			if(!(arrayTruck.get(i).getRegNo().equals(vehicle.getRegNo()))) {
				arrayTruck.add(new Truck(vehicle.getMake(), vehicle.getModel(), vehicle.getWeight(), vehicle.getRegNo(), null, ((Truck) vehicle).getCargoCapacity()));
			}
		}
	}

	public String getDepotName() {
		return depotName;
	}

	public boolean checkIfManager() {
		if(userAccount instanceof Manager) {
			return true;
		}
		else {
			return false;
		}
		
	}

}
