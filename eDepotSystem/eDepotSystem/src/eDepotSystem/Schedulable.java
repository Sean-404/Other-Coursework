package eDepotSystem;

import java.util.Date;
import java.util.ArrayList;

public interface Schedulable {
	public Boolean isAvailable(Date startDate, Date endDate);
	public void addSchedule(WorkSchedule schedule);
	public ArrayList<WorkSchedule> getSchedule();
}
