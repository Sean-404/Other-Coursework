package eDepotSystem;
import java.io.Serializable;
import java.text.SimpleDateFormat;
import java.time.DateTimeException;
import java.util.Date;

public class WorkSchedule implements Serializable {
	
	private int scheduleID;
	private String client;
	private Date startDate;
	private Date endDate;
	private ScheduleState state;
	private Vehicle vehicle;
	private Driver driver;
	
	@Override
	public String toString() {
		SimpleDateFormat format = new SimpleDateFormat("dd-MM-yyyy HH:mm");
		return "Schedule ID: "+scheduleID+
				" | Client:" + client+
				" | Start Date: " + format.format(startDate)+
				" | End Date: " + format.format(endDate) +
				" | State: " + state + "\n";
	}
	
	public static enum ScheduleState
	{
		PENDING, ACTIVE, ARCHIVED
	}

	public WorkSchedule(int scheduleID, String client, Date startDate, Date endDate, ScheduleState state, Driver driver, Vehicle vehicle) {
		this.scheduleID = scheduleID;
		this.client = client;
		this.startDate = startDate;
		this.endDate = endDate;
		this.state = state;
		this.driver = driver;
		this.vehicle = vehicle;
	}
	
	// This method will update the current state of the schedule
	
	public void updateState() {
	// The state of the work schedule should be updated if it is invalid
		Date currentDate = new Date();
		if ( this.state != ScheduleState.ACTIVE
				&& this.startDate.before(currentDate)
				&& this.endDate.after(currentDate))
			setScheduleState(ScheduleState.ACTIVE);
		else if (this.state != ScheduleState.ARCHIVED
				&& this.endDate.before(currentDate))
			setScheduleState(ScheduleState.ARCHIVED);
		else if (this.state != ScheduleState.PENDING
				&& this.endDate.after(currentDate) )
			setScheduleState(ScheduleState.PENDING);
	}
	
// GETTERS AND SETTERS
	
	public int getID() {
		return this.scheduleID;
	}
	
	public String getClient() {
		return this.client;	
	}
	
	public void setClient (String client) {
		this.client = client;
	}
	
	public Date getStartDate () {
		return this.startDate;
	}
	
	public void setStartDate (Date startDate) {
		this.startDate = startDate;
	}
	
	public Date getEndDate() {
		return this.endDate;
	}
	
	public void setEndDate(Date endDate) throws DateTimeException {
		if ( this.startDate == null )
			throw new DateTimeException ("The start date has not yet been set!");
			
		if (!endDate.after((this.startDate) ))
			throw new DateTimeException ("The end date must be after the start date!");
		
		// These date/time exceptions will display a suitable error message
		
		this.endDate = endDate;
	}
	
	public ScheduleState getScheduleState() {
		return this.state;
	}
	
	public void setScheduleState (ScheduleState state) {
		
		this.state = state;
		
		if (this.driver != null)
			this.driver.setSchedule(this);
		
		if (this.vehicle != null)
			this.vehicle.setSchedule(this);
	}
	
	public Vehicle getVehicle() {
		return this.vehicle;
	}
	
	public void setVehicle (Vehicle vehicle) {
		this.vehicle = vehicle;
	}
	
	public Driver getDriver() {
		return this.driver;
	}
	
	public void setDriver (Driver driver) {
		this.driver = driver;
	}
	
	public boolean isComplete() {
		return !this.client.isEmpty() && this.startDate != null
					&& this.endDate != null && this.vehicle != null
					&& this.driver != null;
	}

}
