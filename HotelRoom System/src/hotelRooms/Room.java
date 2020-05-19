package hotelRooms;

public class Room {
	//These specify the attributes of the class, along with their data types
	private int roomNum;
	private String roomType;
	private double roomPrice;
	private boolean hasBalcony;
	private boolean hasLounge;
	private String email;

	//This is the constructor which initialises all of the attributes of the class. The program will create a constructor automatically if one is not already made
	public Room(int roomNum, String roomType, double roomPrice, boolean hasBalcony, boolean hasLounge, String email) {
		this.roomNum = roomNum;
		this.roomType = roomType;
		this.roomPrice = roomPrice;
		this.hasBalcony = hasBalcony;
		this.hasLounge = hasLounge;
		this.email = email;
	}
	
	//This finds any matches for the rooms based on the user's input, and returns a boolean value, indicating if a match has been found
	//The method passes the inputs as parameters to find a match
	public boolean findMatch(String roomTypeInput, double maxPrice, boolean roomBalcony, boolean roomLounge, String email) {
		if (roomTypeInput.equals(roomType) && maxPrice>=roomPrice && (roomBalcony==hasBalcony) && (roomLounge==hasLounge)) {
			return true;
		} else {
			return false;
		}
	}
	
	//This uses a ternary operator to check if the room is reserved, which returns true if it is, and false if it's not.
	public boolean isReserved() {
		return !((email.equals("") || email.equals("free")) ? true : false);
	}
	
	//This is essentially all of the getter methods in one method, which is used to display all of the rooms to the user
	public String showRoom() {
		return getRoomNum() + " " + getRoomType() + " " + getRoomPrice() + " " + getHasBalcony() + " " + getHasLounge() + " " + getEmail();
	}

	//These methods are the getters and setters for the data in the class
	public int getRoomNum() {
		return roomNum;
	}

	public String getRoomType() {
		return roomType;
	}

	public double getRoomPrice() {
		return roomPrice;
	}

	public boolean getHasBalcony() {
		return hasBalcony;
	}

	public boolean getHasLounge() {
		return hasLounge;
	}

	public String getEmail() {
		return email;
	}

	public void setEmail(String email) {
		this.email = email;
	}

}