package hotelRooms;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Scanner;

public class hotelRooms {
	private static Scanner input = new Scanner(System.in);
	
	//This creates an array list with the data type Room, which is a class made for this application.
	static ArrayList<Room> roomList = new ArrayList<Room>();
	
	static String filePath = "rooms.txt";

	public static void main(String[] args) throws FileNotFoundException {
		//This calls up the loadRooms method which is used to transfer the data from the rooms.txt file into the array list
		loadRooms();
		
		String choice = "";
		
		//This creates the menu which is the first thing the user will see, it will keep iterating until the user inputs Q to quit
		do {
			System.out.println("--Room Booking System--");
			System.out.println("\n--MAIN MENU--");
			System.out.println("1 - Reserve Room");
			System.out.println("2 - Cancel Room");
			System.out.println("3 - View Room Reservations");
			System.out.println("Q - Quit");
			System.out.println("Pick: ");
			choice = input.nextLine().toUpperCase();
			
			//This creates a switch which allows for multiple inputs from the user, where each input executes a different task such as reserving or cancelling a room
			switch (choice) {
			case "1": {
				reserveRoom();
				//The break command will terminate the switch and execute the reserveRoom method, then it will display the menu again
				break;
			}
			case "2": {
				cancelRoom();
				break;
			}
			case "3": {
				viewRoomReservations();
				break;
			}
			}
		//This iterates indefinitely while the user has not input "Q", once they do, the loop will terminate
		} while (!choice.equals("Q"));
		
		saveToFile();
		System.out.println("Saved data to file\n");
		
		System.out.println("--Goodbye--");
		
		System.exit(0);

	}
	
	public static void loadRooms() {
		//This assigns an empty memory address for the variable "file" as it has not become a scanner yet
		Scanner file = null;
		
		//The try command is used for exception handling, where it will catch any errors and attempt to fix them, without the program crashing
		//This is useful for external inputs such as keyboard inputs or reading from files, as the application will not crash
		try {
			//This creates a new file reader which reads the rooms.txt file and assigns it to the file variable
			file = new Scanner(new FileReader(filePath));
			
			//This while loop will iterate indefinitely while the text file has content in it, this is useful as files vary in content and size
			while (file.hasNext()) {
				//This creates an array with Strings and adds each line from the file to it
				String[] array = file.nextLine().split(" ");
				
				/*This is used to add a new object with the data from the file, where each value consists of the room number, type, price, whether it has a balcony or lounge, and the email if it exists
				The (array.length == 6) ? array[5] : "") code is used because there could be 6 items in each list for the email, but the program will crash if only 5 exist as it cannot read a 6th element that does not exist
				Therefore, it uses a ternary operator to check if the length is 6 and if it is, it will assign another value. If not, it will assign an empty space */
				roomList.add(new Room((Integer.valueOf(array[0])),array[1],(Double.valueOf(array[2])),Boolean.valueOf(array[3]),Boolean.valueOf(array[4]),(array.length == 6) ? array[5] : ""));
				
			}
		} 
		//This catches an exception which would otherwise crash the program, if the file does not exist, the user will be told the system cannot find the file specified
		catch (FileNotFoundException e) {
			//This prints the error message appropriate for the exception
			System.err.println(e.getMessage());
			
		} 
		//This is the last part of the try catch block that is executed
		finally {
			//This checks if the file does not exist as the program will crash if it tries to close a non-existent file
			if (file != null) {
                file.close();
			}
		}
	}
	
	public static void reserveRoom() throws FileNotFoundException {
		viewRoomReservations();
		
		String roomTypeInput = "";
		
		do {
			System.out.print("Enter room type (Single, Double or Suite): ");
			roomTypeInput = input.nextLine();
			
		} 
		//This creates a do while loop which will iterate until the user inputs Single, Double or Suite
		while (!(roomTypeInput.equals("Single") || roomTypeInput.equals("Double") || roomTypeInput.equals("Suite")));
		
		Double maxPrice = 0.0;
		
		do {
			try {
				System.out.print("Enter max room price: £ ");
				String userInput = input.nextLine();
				//This converts the user's input to a double
				maxPrice = Double.valueOf(userInput);
				
				break;
				
			} 
			//This catches an exception if the user does not enter a value that can be converted to a double
			catch (NumberFormatException e) {
				
				System.out.println("Room price must be an Int or Double");
			}
			
		} while (true);
		
		String roomBalconyInput = "";
		
		do {
			//This asks the user if they want a balcony in their room and converts it to an uppercase value
			System.out.print("Room with balcony? [Y/N] ");
			roomBalconyInput = input.nextLine().toUpperCase();
			
		} 
		//This asks the user to enter an input that must be Y or N, otherwise it will ask them again
		while (!(roomBalconyInput.equals("Y") || roomBalconyInput.equals("N")));
		
		//This converts the user's input to a boolean value
		boolean roomBalcony = Boolean.parseBoolean(roomBalconyInput.equals("Y") ? "true" : "false");
		
		String roomLoungeInput = "";
		
		do {
			System.out.print("Room with lounge? [Y/N] ");
			roomLoungeInput = input.nextLine().toUpperCase();
			
		} while (!(roomLoungeInput.equals("Y") || roomLoungeInput.equals("N")));
		
		//This code follows the same practise as the balcony code
		boolean roomLounge = Boolean.parseBoolean(roomLoungeInput.equals("Y") ? "true" : "false");
		
		String email = "";
		System.out.print("Enter email: ");
		email = input.nextLine();
		
		System.out.print("\n");
		
		Scanner file = new Scanner(new FileReader(filePath));
		
		//This is an array list that will be used to show the user the rooms that have matched their requirements
		ArrayList<String> suitableRooms = new ArrayList<String>();
		
		//This will increment by 1 for each match found for the user
		int matchFound = 0;
		
		//This is a for loop which iterates a number of times equal to the length of the room list. the variable r is used to call up the class methods
		for (Room r : roomList) {
			
			//This converts each line from the text file to a string and assigns it to the lineFromFile variable
			String lineFromFile = file.nextLine().toString();
			
			//This calls up the isReserved() method in the Room class to check if the room is already reserved. If it is, the code will not execute
			if (!(r.isReserved())) {
				
				//This calls up the isReserved() method in the Room class to check if the user's inputs match the values in the roomList class array list
				if (r.findMatch(roomTypeInput, maxPrice, roomBalcony, roomLounge, email)==true) {
					
					//This appends the line from the text file to the array list and increments the counter by 1
					suitableRooms.add(lineFromFile);
					matchFound += 1;
					
					System.out.println("Found a match (" + matchFound + "): " + lineFromFile);
				}
			}
		}
		//This creates a ternary operation that checks that at least 1 match was found. If not, the user will be told that no rooms were found
		System.out.println(matchFound >= 1 ? "" : "No room found!\n");
		
		String roomChoice = "";
		
		while (matchFound >= 1) {
			try {
				
				System.out.println("Which room would you like? [Use 1, 2, 3 etc.]: ");
				
				//This gets the user's input and converts it to an integer and decreases it by 1 since arrays start at 0
				Integer userChoice = (Integer.valueOf(input.nextLine()) - 1);
				roomChoice = suitableRooms.get(userChoice);
				
				break;
				
			} 
			//This creates an exception catch which will tell the user if they try to input a value that cannot be indexed by the array list
			catch (IndexOutOfBoundsException e) {
				
				System.out.println("Index does not exist. Try again.");
			}
		}
		
		for (Room r : roomList) {
			
			if (matchFound>=1) {
				
				//This checks if the room number from roomList is equal to the first 3 values of the room choice (the room number in the file)
				if (r.getRoomNum()==Integer.valueOf(roomChoice.substring(0, 3))) {
					
					//This calls up the class method setEmail with the parameter email, which the user entered before
					r.setEmail(email);
					
					System.out.println("Room reserved\n");
				}
			}
		}
		
		//This closes the file as file manipulation is no longer needed
		file.close();
	}

	public static void cancelRoom() {
		
		//This gets the user's email which will be removed from the array list, therefore the room reservation will be cancelled
		System.out.println("Enter the email that you reserved: ");
		String email = input.nextLine();
		
		for (Room r : roomList) {
			//This checks if the room is reserved the user's input is equal to the email in roomList
			if (r.isReserved() && email.equals(r.getEmail())) {
				
				//The email has been erased and set to a blank space
				r.setEmail("");
				
				System.out.println("Successfully cancelled room\n");
			}
		}
	}
	
	public static void viewRoomReservations() {
		for (Room r : roomList) {
			
			//This displays all of the available rooms and omits the rooms that have been reserved as the guests will not need to see them
			if ((r.getEmail().equals("")) || (r.getEmail().equals("free"))) {
				
				//This calls up the showRoom class method, which essentially uses all of the getter methods in one
				System.out.println(r.showRoom());
				
			}
		}
		System.out.println("");
	}
	
	public static void saveToFile() throws FileNotFoundException {
		//This creates a print writer which is used to write the contents back to the text file
		PrintWriter pw = new PrintWriter(filePath);
		
		for (Room r : roomList) {
			
			//This calls up the showRoom class method and writes it to the room.txt file
			pw.println(r.showRoom());
		}
		
		//This closes the print writer as it is no longer needed
		pw.close();
	}
}
